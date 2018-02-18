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
#   Parse measurement-based words from text.
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

#   Other imports.
from nltk import word_tokenize
import json
import nltk
import requests
import string

#   MAIN
def main():
    measurements_unit_tests("15-year-old human stage")
    
#   Get measurement words.
#
#   UO = Units of Measurement
def get_measurements(raw_string):
    
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    new_string = raw_string.translate(translator)
    
    measure_list = []
    measure_id_array = []
    
    for word in word_tokenize(new_string):
    
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(word) + "&ontology=sio,uo"

        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            found = False
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "UO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in measure_id_array and word.lower() == doc["label"].lower():
                            measure_temp = {
                                'identifier': new_id,
                                'identifier_type': "UO ID",
                                'source': "Ontology Lookup Service",
                                'name': doc["label"]
                            }
                            measure_list.append(measure_temp)
                            measure_id_array.append(new_id)
                        
    return measure_list

#   UNIT TESTS
def measurements_unit_tests(test_string):
    print(get_measurements(test_string))

#   MAIN
if __name__ == "__main__": main()