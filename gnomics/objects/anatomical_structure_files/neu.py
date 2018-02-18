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
#   NEU ID.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    neu_unit_tests()
    
# Return NEU ID.
def get_neu_id(anat, user=None):
    neu_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier"]):
        if iden["identifier"] not in neu_array:
            neu_array.append(iden["identifier"])
    return neu_array
    
#   UNIT TESTS
def neu_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()