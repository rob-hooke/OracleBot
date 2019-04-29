# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:27:36 2019

@author: Boby Robert

"""
import nltk
import numpy as np
import random
import string
import warnings
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



f = open('endgame.txt','r', errors = 'ignore')
raw = f.read()

raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lem = nltk.stem.WordNetLemmatizer()

def lemToken(tokens):
    return [lem.lemmatize(token) for token in tokens]


punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def lemNormalizeText(text):
    return lemToken(nltk.word_tokenize(text.lower().translate(punct_dict)))

greeting_ip = ["hello","hi","hey","whats up"]

greeting_res =["hey","hi there", "how you doing?","hey how re you?"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greeting_ip:
            return random.choice(greeting_res)


def response(user_input):
    oracle_response = ' '
    sent_tokens.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=lemNormalizeText, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1],tfidf)
    idx = vals.argsort()[0][2]
    flat = vals.flatten()
    flat.sort()
    res_tfidf = flat[-2]
    
    if (res_tfidf == 0):
        oracle_response = oracle_response + "Sorry! I cant answer that!"
        return oracle_response
    else:
        oracle_response = oracle_response + sent_tokens[idx]
        return oracle_response
   

flag = True
print("Oracle : Hello , I'm Oracle. How may I help you?")

while(flag):
    user_input = input()
    user_input = user_input.lower()
    if (user_input != 'bye'):
        if(greeting(user_input) != None):
            print("Oracle : " + greeting(user_input))
        else:
            print("Oracle : " + response(user_input))
            sent_tokens.remove(user_input)
        
    else:
        flag = False
        print("Oracle: Bye")
    
    