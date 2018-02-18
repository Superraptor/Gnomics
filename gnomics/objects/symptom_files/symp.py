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
#   Get Symptom (SYMP) Ontology.
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
import gnomics.objects.symptom

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    symp_unit_tests()
    
#   Get SYMP ID.
def get_symp_id(symptom):
    symp_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(symptom.identifiers, ["symp", "symp id", "symp identifier", "symptom ontology", "symptom ontology id", "symptom ontology identifier"]):
        if iden["identifier"] not in symp_array:
            symp_array.append(iden["identifier"])
    return symp_array

#   UNIT TESTS
def symp_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()