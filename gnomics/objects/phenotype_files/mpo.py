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
#   Convert to Microbial Phenotype Ontology (MPO).
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
    mpo_unit_tests()

#   Get MPO ID.
def get_mpo_id(phen, user=None):
    mpo_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["mpo", "mpo id", "mpo identifier"]:
            if ident["identifier"] not in mpo_id_array:
                mpo_id_array.append(ident["identifier"])
    return mpo_id_array
        
#   UNIT TESTS
def mpo_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()