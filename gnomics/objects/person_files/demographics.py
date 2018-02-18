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
#   Parse demographic data.
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
import gnomics.objects.person

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    demo_array = [
        "38-year-old male",
        "52-year-old male",
        "26-year-old female",
        "64-year-old male"
    ]
    demographic_unit_tests(demo_array)

def parse_demographics(raw_string):
    demographics = {}
    demographics["age"] = age(raw_string)
    demographics["phenotypic_sex"] = phenotypic_sex(raw_string)
    return demographics
    
#   Get age (life stage) from integer or string.
#
#   This only includes life stages in humans.
#   If plain integer, years is assumed as the
#   unit.
def age(raw_string):
    if len(raw_string) > 0:
        if isinstance(raw_string, int):
            raw_age = str(raw_string) + "-year-old"
        raw_age = str(raw_string)

        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(raw_age) + "&ontology=hsapdv"
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()

            age_list = []
            age_id_array = []
            found = False
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "HsapDv" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in age_id_array:
                            age_temp = {
                                'identifier': new_id,
                                'identifier_type': "HSAPDV ID",
                                'source': "Ontology Lookup Service",
                                'taxon': "Homo sapiens",
                                'name': doc["label"]
                            }
                            age_list.append(age_temp)
                            age_id_array.append(new_id)
                            found = True
                        if found:
                            break

            return age_list[0]
    else:
        return
    
#   Get phenotypic sex from a string.
def phenotypic_sex(raw_string):
    split_string = raw_string.split(" ")
    
    for raw_sex in split_string:
        if raw_sex.lower() == "m" or raw_sex.lower() == "male" or raw_sex.lower() == "man" or raw_sex.lower() == "boy":
            raw_sex = "male"
        elif raw_sex.lower() == "f" or raw_sex.lower() == "w" or raw_sex.lower() == "female" or raw_sex.lower() == "woman" or raw_sex.lower() == "girl":
            raw_sex = "female"
        elif raw_sex.lower() == "pseudohermaphrodite":
            raw_sex = "pseudohermaphrodite"
        elif raw_sex.lower() == "hermaphrodite":
            raw_sex = "hermaphrodite"

        url = "https://www.ebi.ac.uk/ols/api/ontologies"
        ext = "/pato/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FPATO_0001894/children"
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()

            sex_list = []
            sex_id_array = []
            for term in decoded["_embedded"]["terms"]:
                if term["label"].lower() == raw_sex.lower():
                    new_id = term["obo_id"]
                    new_term = term["label"]
                    new_def = term["description"]
                    sex_temp = {
                        'identifier': new_id,
                        'name': new_term,
                        'taxon': "Homo sapiens",
                        'identifier_type': "PATO ID",
                        'source': "Ontology Lookup Service"
                    }
                    sex_list.append(sex_temp)
                    sex_id_array.append(new_id)

            if sex_list:
                return sex_list[0]
            
#   UNIT TESTS
def demographic_unit_tests(demographic_info):
    for x in demographic_info:
        print("\nGetting info from string '%s':" % x)
        print("- Age: %s" % str(age(x)))
        print("- Phenotypic Sex: %s" % str(phenotypic_sex(x)))

#   MAIN
if __name__ == "__main__": main()