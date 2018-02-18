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
#   Convert to Mammalian Phenotype Ontology (MP).
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
import gnomics.objects.phenotype

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    mp_unit_tests()

#   Get MP ID.
def get_mp_id(phen, user=None):
    mp_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["mp", "mp id", "mp identifier"]:
            if ident["identifier"] not in mp_id_array:
                mp_id_array.append(ident["identifier"]) 
    return mp_id_array
        
#   UNIT TESTS
def mp_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()