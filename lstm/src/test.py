# test a model weights with input sentences


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
import generate_wordVec as gv
import nltk
from train import one_hot
from train import get_sentence
from textblob import TextBlob as tb

coreWords = ['mexico', 'immigration','war', 'isis', 'obama', 'democrats', 'replublicans']

def recalc_model_params(filepathname, modelToLoad, minLen):
    print os.system('pwd')
    vmodel = gs.models.Word2Vec.load(modelToLoad)
    text = open(filepathname).read().lower().replace('\n',' ')
    text = gv.clean_1(text)
    text = text.replace("."," ")
    parsedWords = text.split(" ")
    wordCoding = {}
    parsedWords = text.split(" ")
    wordCoding = {}
    codedWord = {}
    codeNum = 1
    vecValues={}
    codedVector = []
    for word in parsedWords:
        if not word in wordCoding:
            wordCoding[word] = codeNum
            codedWord[codeNum] = word
            codeNum += 1
	    vecValues[word] = vmodel[word]
        codedVector.append(wordCoding[word])
    print('corpus length:', len(wordCoding))
    print('Vectorization...')


    input_dim = 300
    lstm_hdim = 500
    bridge_dim = 1000
    dense_dim = 1500

    sd_len = minLen

    batch_size = 128
    sd_size = int(len(codedVector) / sd_len)

    x_D = []# np.zeros((sc_size * sc_len, sc_len))
    y_D = []# np.zeros((sc_size * sc_len, len(wordCoding)))
    i_D = []
    v_D = []
    for idx in range(0, sd_size - 1):
        for iidx in range(0, sd_len - 1):
            indexD = codedVector[idx * sd_len + iidx + 0:(idx + 1) * sd_len + iidx]
            i_D.append(indexD)

            vectorValD = [vecValues[myWord] for myWord in parsedWords[idx * sd_len + iidx + 0:(idx + 1) * sd_len + iidx]]
            x_D.append(vectorValD)
            y_D.append(one_hot(codedVector[(idx + 1) * sd_len + iidx],wordCoding))
    	    v_D.append(vecValues[parsedWords[(idx + 1) * sd_len + iidx]])
    x_D = np.asarray(x_D)
    y_D = np.asarray(y_D)
    i_D = np.asarray(i_D)
    v_D = np.asarray(v_D)

    layerNames = [
        'tdd1',
        'bn1',
        'lstm1',
        'bn2',
        'lstm2',
        'bn3',
        'lstm3',
        'bn4',
        'dropout1',
        'dense1',
        'denseelu1',
        'dropout2',
        'dense2',
        'densesm1',
    ]

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
    modelParameters = [x_D, y_D, model, sd_len, i_D, codedWord, vmodel, vecValues]
    print('Done')
    sys.stdout.flush()
    return modelParameters


def parse_message(msg):
    pmsg=[]
    for w in msg.split(' '):
        if len(w)==0:
            continue
        if w[-1].isalpha():
            pmsg.append(w)
        else:
            pmsg.append(w[:-1])
            if w[-1]=='.':
                pmsg.append('[dot]')
            elif w[-1]==',':
                pmsg.append('[comma]')
    return pmsg


def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))

def load_model_for_testing(filepathname, modelToLoad):
    modelParameters = recalc_model_params(filepathname, modelToLoad, 5)
    return modelParameters

def generate_word_code(codedWord):
    return dict((v,k) for k,v in codedWord.iteritems())

def generate_sentence_wordVector(sent, wordCodes, vLen = 5, debug=False):
    words = parse_message(sent)
    lent = vLen
    words
    sentVec = []
    for w in words:
        if wordCodes.get(w.lower()) is not None:
            sentVec.append(wordCodes.get(w.lower()))
        else:
            if debug==True:
                print 'Missing word from vocab: ', w
    i=0
    while len(sentVec)<vLen+1:
        w = coreWords[i]
        sentVec.append(wordCodes.get(w.lower()))
        i+=1

    return np.array([sentVec[:lent]])

def generate_vmodel_sentence(sentVec, vmodel, codedWord):
    vecsentence = []
    for vcode in sentVec[0]:
        vecsentence.append(vmodel[codedWord[vcode]])
    vecsentence = np.reshape(vecsentence, (1, len(vecsentence), 300))
    return vecsentence


def generate_response(modelParameters, weightsFile, msg, diversity=0.3, vLen=5, debug=False):
    x_D, y_D, model, sd_len, i_D, codedWord, vmodel,vecValues = modelParameters[0], modelParameters[1], modelParameters[2], modelParameters[3], modelParameters[4], modelParameters[5], modelParameters[6], modelParameters[7]
    model.load_weights(weightsFile)
    wordCodes = generate_word_code(codedWord)
    sentVec = generate_sentence_wordVector(msg,wordCodes, vLen)
    sentence = sentVec
    if debug==True:
        print len(sentVec[0])
        print sentVec[0]
        print [codedWord[i] for i in sentVec[0]]
    sentOutput = ''
    outputSentenceWordLength=random.choice(range(50,100))
    for iteration in range(0,outputSentenceWordLength):
        vecsentence = []
        vecsentence = generate_vmodel_sentence(sentence,vmodel, codedWord)
        preds = model.predict({'input':vecsentence}, verbose=0)['output1'][0]
        next_index = sample(preds, diversity)
        if next_index in codedWord:
            next_char = codedWord[next_index]
            if debug==True:
                print next_index, '>> ', next_char,
            sentence = np.append(sentence[0][1:], [next_index]).reshape(np.asarray(sentence).shape)
            sentOutput += next_char + ' '
            if debug==True:
                print '   -->  ', [codedWord[i] for i in sentence[0]]

    return sentOutput


def generate_sentences_responses(sentOutput, debug=False):
    sol = ''
    maxLen= random.choice(range(3,5))
    candSet = sentOutput.split(' [dot] ')[2:]
    if debug==True:
        print candSet
    sentLen=0
    for sent in candSet:
        if sentLen==maxLen:
            break
        senWords = sent.split(' ')

        if len(senWords)<3:
            continue
        for word in senWords:
            try:
                if word[0]=='[' and word[-1]==']':
                    if word=='[comma]':
                        sol+=','
                    elif word=='[dot]':
                        sol+='. '

                else:
                    if senWords.index(word)==0:
                        sol+=' '+word.title()
                    else:
                        sol+=' '+word
            except Exception as e:
                print e
        sol+='.'
        sentLen+=1
    return sol

def process_message(msg, modelParameters, weightsFile, diversity=0.3, vLen=5, debug=False):
    print 'You: ', msg
    print ''
    sentOutput = generate_response(modelParameters,weightsFile, msg, diversity, vLen, debug)
    resp = generate_sentences_responses(sentOutput)
    print '\nBOT sentences... ', sentOutput
    if debug==True:
        candSet = sentOutput.split(' [dot] ')
        for i in candSet:
            print i
        print 
    if tb(msg).sentiment[0]<=-0.5:
        resp='Relax and listen...'+resp
    return resp

def key_select(msg):
    sol=[]
    for w,posp in tb(msg).tags:
        if posp in ['NN','NNP', 'NNS', 'JJ']:
            sol.append(w)
    return ' '.join(sol)
