#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#
#

#
#   Perform basic NLP-based functionalities.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

#   Import modules.
from gnomics.objects.user import User
import gnomics.objects.reference

#   Other imports.
from nltk.corpus import wordnet as wn
from word_forms.word_forms import get_word_forms
import json
import nltk
import requests
import time

#   MAIN
def main():
    words_unit_tests("29224256") #"CDK4 Gene Amplification")
    
#   Get word forms.
#
#   r = adverb
#   a = adjective
#   n = noun
#   v = verb
def word_forms(string):
    proc_word = get_words(string)
    word_dict = {}
    for wd in proc_word:
        word_dict[wd] = get_word_forms(wd)
    return word_dict
        
#   Word tokenize.
def word_tokenize(string):
    tokens = nltk.word_tokenize(string)
    return tokens

#   Sentence tokenize.
def sentence_tokenize(string):
    tokens = nltk.sent_tokenize(string)
    return tokens
    
#   Get words from string.
def get_words(string):
    words = word_tokenize(string)
    words = [word.lower() for word in words if word.isalpha()]
    return words

#   Normalize text.
def normalization(string):
    print("NOT FUNCTIONAL.")
    
def collocation(string):
    print("NOT FUNCTIONAL.")

#   Get lemmas.
def lemmatization(string):
    words = get_words(string)
    wnl = nltk.WordNetLemmatizer()
    return [wnl.lemmatize(t) for t in words]

def segmentation(string):
    print("NOT FUNCTIONAL.")
    
#   Obtain word stems.
def word_stems(string, stemmer="lancaster"):
    words = get_words(string)
    if stemmer == "lancaster":
        lancaster = nltk.LancasterStemmer()
        return [lancaster.stem(t) for t in words]
    elif stemmer == "porter":
        porter = nltk.PorterStemmer()
        return [porter.stem(t) for t in words]
    else:
        print("Stemmer '%' not recognized... Try using 'lancaster' or 'porter'.")

#   Tag parts of speech (POS).
def part_of_speech_tagger(string):
    print("NOT FUNCTIONAL.")

#   UNIT TESTS
def words_unit_tests(pmid): # word):
    ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    
    print(word_stems(gnomics.objects.reference.Reference.abstract(ref)))

#   MAIN
if __name__ == "__main__": main()