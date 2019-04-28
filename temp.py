# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:27:36 2019

@author: Boby Robert

"""
import nltk
import numpy as np
import random
import string

f = open('endgame.txt','r', errors = 'ignore')
raw = f.read()

raw = raw.lower()

nltk.download('punkt')
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lem = nltk.stem.WordNetLemmatizer()

def lemToken(tokens):
    return [lem.lemmatize(token) for token in tokens]

punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def lemNormalizeText(text):
    return(nltk.word_tokenize(text.lower().translate(punct_dict)))

greeting_ip = ["hello","hi","hey","whats up"]

greeting_res =["hey","hi there", "how you doing?","hey how re you?"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greeting_ip:
            return random.choice(greeting_res)


    