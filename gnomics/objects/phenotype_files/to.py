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
#   Convert to Plant Trait Ontology (TO) (PTO).
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
    to_unit_tests()

#   Get TO ID.
def get_to_id(phen, user=None):
    to_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["to", "to id", "to identifier", "pto", "pto id", "pto identifier"]:
            if ident["identifier"] not in to_id_array:
                to_id_array.append(ident["identifier"])     
    return to_id_array
        
#   UNIT TESTS
def to_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()