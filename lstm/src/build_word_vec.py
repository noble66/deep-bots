
from __future__ import print_function
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, TimeDistributedDense
from keras.layers.advanced_activations import ELU
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.datasets.data_utils import get_file
import gensim as gs
import numpy as np
import random
import os
import sys

def get_text(filepath):  
    text = open(filepath).read().lower()
    return text


def parse_text_words(text, bigrams=True):
    parsedWords = [words.split(' ') for words in [sentences for sentences in text.split('.')]]
    #parsedWords = text.split(" ")
    try:
	bigramParsedWords = gs.models.Phrases(parsedWords)
    except:
	bigramParsedWords = None
    return bigramParsedWords, parsedWords

def word_to_vec(bigramParsedWords, parsedWords, modelName=''):
    #print(modelName)
    if len(modelName)==0:
    	print('Please provide a model Name to save with..')
        return None
    sstSgv = [1]
    sstCbm = [0, 1]
    sstHsv = [0]
    sstNeg = range(5, 20)
    sstWin = range(8, 12)
    # optimize hyper parameters
    #optimum w2v hyper-parameters
    currModel = gs.models.Word2Vec(parsedWords, size=300, min_count=1, iter=10, window=8, sg=1, hs=0, negative=5)
    currModel.save(modelName+'.w2v')
    print ('Saved model: %s.w2v',modelName)
    return currModel


def process_text(filepath, modelName):
    #print(modelName)
    text = get_text(filepath)
    bigrams, parsedWords =  parse_text_words(text)
    w2vModel = word_to_vec(bigrams, parsedWords, modelName)
    if w2vModel==None:
	print ('Modeling failed..')
	return -1
    else:
        print ('Modeling Complete..')
	return 1

if __name__ == '__main__':
    print('Building Model')
    sys.stdout.flush()
    filepathname = sys.argv[1]
    modelName = sys.argv[2]
    print('Using file: ',filepathname)
    print('Model will be called ', modelName)
    #print (len(modelName))
    status = process_text(filepathname, modelName)
    
