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
#   Convert to Flora Phenotype Ontology (FLOPO).
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
    flopo_unit_tests()

#   Get FLOPO ID.
def get_flopo_id(phen, user=None):
    flopo_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["flopo", "flopo id", "flopo identifier"]:
            if ident["identifier"] not in flopo_id_array:
                flopo_id_array.append(ident["identifier"])
    return flopo_id_array
        
#   UNIT TESTS
def flopo_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()