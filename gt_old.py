# -*- coding: UTF-8 -*-
'''Example script to generate text from Nietzsche's writings.

At least 20 epochs are required before the generated text
starts sounding coherent.

It is recommended to run this script on GPU, as recurrent
networks are quite computationally intensive.

If you try this script on new data, make sure your corpus
has at least ~100k characters. ~1M is better.
'''

from __future__ import print_function
from keras.models import Graph
from keras.layers.core import Dense, Activation, Dropout, TimeDistributedDense, Masking
from keras.layers.advanced_activations import ELU
from keras.layers.recurrent import LSTM
from keras.layers.normalization import BatchNormalization
from keras.layers.embeddings import Embedding
from keras.datasets.data_utils import get_file
from keras.preprocessing.sequence import pad_sequences
import gensim as gs
import numpy as np
import random
import os
import sys
import time, sys
import build_word_vec as bwv

def one_hot(index):
    retVal = np.zeros((len(wordCoding)), dtype=np.bool)
    retVal[index] = 1
    return retVal

def load_w2v_model(modelName):
    vmodel = gs.models.Word2Vec.load(modelName+'.w2v')
    return vmodel

def word_similarity(model, w1, w2):
    if w1 in model and w2 in model:
 	return model.similarity(w1,w2)
    else:
        return -1

def one_hot(index, wordCoding):
    retVal = np.zeros((len(wordCoding)), dtype=np.bool)
    retVal[index] = 1
    return retVal

def lstm_design_1(parsedWords, vmodel):
    wordCoding = {}
    codedWord = {}
    codeNum = 1
    codedVector = []
    for word in parsedWords:
        if not word in wordCoding:
            wordCoding[word] = codeNum
            codedWord[codeNum] = word
            codeNum += 1
        codedVector.append(wordCoding[word])
    print('corpus length:', len(wordCoding))
    print('Vectorization...')
    
    input_dim = 300
    lstm_hdim = 500
    bridge_dim = 1000
    dense_dim = 1500
    
    sd_len = 12
    
    batch_size = 128
    sd_size = int(len(codedVector) / sd_len)
    
    x_D = []# np.zeros((sc_size * sc_len, sc_len))
    y_D = []# np.zeros((sc_size * sc_len, len(wordCoding)))
    i_D = []

    for idx in range(0, sd_size - 1):
        for iidx in range(0, sd_len - 1):
            indexD = codedVector[idx * sd_len + iidx + 0:(idx + 1) * sd_len + iidx]
            i_D.append(indexD)
    
            vectorValD = [vmodel[myWord] for myWord in parsedWords[idx * sd_len + iidx + 0:(idx + 1) * sd_len + iidx] ]
            x_D.append(vectorValD)
            y_D.append(one_hot(codedVector[(idx + 1) * sd_len + iidx], wordCoding))
    
    x_D = np.asarray(x_D)
    y_D = np.asarray(y_D)
    i_D = np.asarray(i_D)

    layerNames = ['tdd1', 'bn1', 'lstm1', 'bn2', 'lstm2', 'bn3', 'lstm3', 'bn4', 'dropout1', 'dense1', 'denseelu1', 'dropout2', 'dense2', 'densesm1']

    print ('Stacking layers')
    sys.stdout.flush()
    # build the model: 2 stacked LSTM
    print('shapes: ' + str((x_D.shape)))
    print('Build model...')
    model = Graph()
    model.add_input(name='input', input_shape=(sd_len, input_dim))
    model.add_node(TimeDistributedDense(input_dim=input_dim, output_dim=lstm_hdim, input_length=sd_len), name=layerNames[0], input='input')
    model.add_node(BatchNormalization(), name=layerNames[1], input=layerNames[0])
    
    model.add_node(LSTM(input_dim=lstm_hdim, output_dim=lstm_hdim, return_sequences=True), name=layerNames[2] + 'left', input=layerNames[1])
    model.add_node(BatchNormalization(), name=layerNames[3] + 'left', input=layerNames[2] + 'left')
    
    model.add_node(LSTM(input_dim=lstm_hdim, output_dim=lstm_hdim, return_sequences=True, go_backwards=True), name=layerNames[2] + 'right', input=layerNames[1])
    model.add_node(BatchNormalization(), name=layerNames[3] + 'right', input=layerNames[2] + 'right')
    
    model.add_node(LSTM(input_dim=lstm_hdim, output_dim=lstm_hdim, return_sequences=False), name=layerNames[6] + 'left', input=layerNames[3] + 'left')
    
    model.add_node(LSTM(input_dim=lstm_hdim, output_dim=lstm_hdim, return_sequences=False, go_backwards=True), name=layerNames[6] + 'right', input=layerNames[3] + 'right')
    
    model.add_node(BatchNormalization(), name=layerNames[7], inputs=[layerNames[6] + 'left', layerNames[6] + 'right'])
    model.add_node(Dropout(0.2), name=layerNames[8], input=layerNames[7])
    
    model.add_node(Dense(input_dim=bridge_dim, output_dim=dense_dim), name=layerNames[9], input=layerNames[8])
    model.add_node(ELU(), name=layerNames[10], input=layerNames[9])
    model.add_node(Dropout(0.2), name=layerNames[11], input=layerNames[10])
    
    model.add_node(Dense(input_dim=dense_dim, output_dim=len(wordCoding)), name=layerNames[12], input=layerNames[11])
    model.add_node(Activation('softmax'), name=layerNames[13], input=layerNames[12])
    model.add_output(name='output1', input=layerNames[13])
    
    model.compile(optimizer='rmsprop', loss={'output1':'categorical_crossentropy'})
    return sd_len, i_D, model, codedWord


def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))

# train the model, output generated text after each iteration
def get_sentence(wordVec):
    sent = ''
    for wordVal in wordVec:
        sent += codedWord[wordVal] + ' '
    return sent


def train(sd_len, i_D, nnModel, vmodel, codedWord):
    #sd_len, i_D, nnModel = lstm_design_1(text, vmodel)
    seedLen = sd_len
    seedSrc = i_D
    outSentences = []
    while len(outSentences) < 100:
        start_index = random.randint(0, len(seedSrc) - 1)
        sentence = seedSrc[start_index: start_index + 1]
    
        sentOutput = ''
    
        for iteration in range(500):
            vecsentence = []
            for vcode in sentence[0]:
                vecsentence.append(vmodel[codedWord[vcode]])
            vecsentence = np.reshape(vecsentence, (1, len(vecsentence), 300))
            preds = nnModel.predict({'input':vecsentence}, verbose=0)['output1'][0]
            next_index = sample(preds, 0.2)
            if next_index in codedWord:
                next_char = codedWord[next_index]
                sentence = np.append(sentence[0][1:], [next_index]).reshape(np.asarray(sentence).shape)
                sentOutput += next_char + ' '
        print(sentOutput)
