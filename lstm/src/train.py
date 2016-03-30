
# train the model, results stored as tb_weights WILL OVERWRITE now
# # [USE] : python train.py <source_text_file> <toUse_word2vec_model_name>


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
import generate_wordVec as gv



def one_hot(index, wordCoding):
    retVal = np.zeros((len(wordCoding)), dtype=np.bool)
    retVal[index] = 1
    return retVal

def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    return np.argmax(np.random.multinomial(1, a, 1))

# train the model, output generated text after each iteration
def get_sentence(wordVec, codedWord):
    sent = ''
    for wordVal in wordVec:
        sent += codedWord[wordVal] + ' '
    return sent

def calc_model_params(filepathname, modelToLoad):
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

    sd_len = 12

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
    return modelParameters

# modelParameters = [x_D, y_D, model, sd_len, i_D, codedWord, vmodel]
def iterate_train(filepathname, modelToLoad, rounds=30, nEpochs=5, debug=False):
    if debug==True:
    	rounds=2
    	nEpochs=1
    print('Building Model parameters...')
    sys.stdout.flush()
    modelParameters = calc_model_params(filepathname, modelToLoad)
    x_D, y_D, model, sd_len, i_D, codedWord, vmodel,vecValues = modelParameters[0], modelParameters[1], modelParameters[2], modelParameters[3], modelParameters[4], modelParameters[5], modelParameters[6], modelParameters[7]
    print('Begin Iterative Training...')
    print(rounds, 'rounds and ', nEpochs, ' epochs')
    sys.stdout.flush()
    for iteration in range(0, rounds):
        print()
        print('-' * rounds,'Round ',iteration)
        for j in range(1):
            model.fit({'input':x_D, 'output1':y_D}, nb_epoch=nEpochs)  # use min 5 epochs
            model.save_weights('tb-weights', overwrite=True)

        preds = model.predict({'input': x_D[:5000]}, verbose=0)
        train_accuracy = np.mean(np.equal(np.argmax(y_D[:5000], axis=-1), np.argmax(preds['output1'][:5000], axis=-1)))
        print('Training Accuracy right now: ',train_accuracy)

        seedSelector = np.random.randint(0,3)
        seedSrc = i_D
        seedLen = sd_len
        start_index = random.randint(0, len(seedSrc) - 1)

        for diversity in [0.1, 0.2, 0.3, 0.4, 0.5]:
            print()
            print('----- diversity:', diversity)

            sentence = seedSrc[start_index: start_index + 1]
            strSentence = get_sentence(sentence[0], codedWord)
            print('----- Generating with seed: "' + strSentence + '"')

            for i in range(200):
                vecsentence = []
                for vcode in sentence[0]:
                    vecsentence.append(vecValues[codedWord[vcode]])
                vecsentence = np.reshape(vecsentence, (1, len(vecsentence), 300))
                preds = model.predict({'input':vecsentence}, verbose=0)['output1'][0]
                next_index = sample(preds, diversity)
                if next_index in codedWord:
                    next_char = codedWord[next_index]
                    sentence = np.append(sentence[0][1:], [next_index]).reshape(np.asarray(sentence).shape)
                    # replace special symbols with punctuation
                    sys.stdout.write(next_char + ' ')
                    sys.stdout.flush()
            print()

if __name__ == '__main__':
    filepathname = sys.argv[1]
    modelToLoad = sys.argv[2]
    st = time.time()
    rounds = 20
    iterate_train(filepathname, modelToLoad, rounds)
    print('Elapsed: ', (time.time()-st)*1.0/60, ' mins')
