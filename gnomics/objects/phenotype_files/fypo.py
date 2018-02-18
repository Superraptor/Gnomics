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
#   Convert to Fission Yeast Phenotype Ontology (FYPO).
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
    fypo_unit_tests()

#   Get FYPO ID.
def get_fypo_id(phen, user=None):
    fypo_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["fypo", "fypo id", "fypo identifier"]:
            if ident["identifier"] not in fypo_id_array:
                fypo_id_array.append(ident["identifier"])
    return fypo_id_array
        
#   UNIT TESTS
def fypo_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()