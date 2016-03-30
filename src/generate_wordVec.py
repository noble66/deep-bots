# -*- coding: UTF-8 -*-
# [USE] : python generate_word2Vec.py <source_text_file> <output_word2vec_model_name>

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


def clean_1(text):
    text = text.replace(" - ", ", ")
    text = text.replace(" t ", " to ")
    text = text.replace(" st. louis ", " st louis ")
    text = text.replace(" mr. ", " mister ")
    text = text.replace(" mrs. ", " mistress ")
    text = text.replace(" ms. ", " miss ")
    text = text.replace(" feb. ", " february ")
    text = text.replace(" dr. ", " doctor ")
    text = text.replace(" gen. ", " general ")
    text = text.replace(" gov. ", " governor ")
    text = text.replace(" sen. ", " senator ")
    text = text.replace(" sgt. ", " sergeant ")
    text = text.replace(" rev. ", " reverend ")
    text = text.replace(". no. ", ". number ")
    text = text.replace(" jr. ", " junior ")
    text = text.replace(". ", " [dot]. ")
    text = text.replace("! ", " [xcm]. ")
    text = text.replace("? ", " [q]. ")
    text = text.replace(", ", " [comma] ")
    text = text.replace(" $", " [dlr] ")
    text = text.replace(": ", " [cln] ")
    text = text.replace("; ", " [scln] ")
    text = text.replace("% ", " [pcnt] ")
    text = text.replace(". ", ".")
    text = text.replace("   ", " ")
    text = text.replace("  ", " ")
    text = text.replace("\"","")
    return text

def build_w2v(filepathname, modelName):
    modelName = sys.argv[2]
    print('Using text file to build model: ', filepathname)
    text = open(filepathname).read().lower().replace('\n',' ')
    text = clean_1(text)
    parsedWords = [words.split(' ') for words in [sentences for sentences in text.split('.')]]
    sstSgv = [1]
    sstCbm = [0, 1]
    sstHsv = [0]
    sstNeg = range(5, 20)
    sstWin = range(8, 12)

    #optimum w2v hyper-parameters
    model = gs.models.Word2Vec(parsedWords, size=300, min_count=1, iter=10, window=8, sg=1, hs=0, negative=5)
    print('Saving model: ', modelName)
    model.save(modelName)

if __name__ == '__main__':
    filepathname = sys.argv[1]
    modelName = sys.argv[2]
    build_w2v(filepathname, modelName)
