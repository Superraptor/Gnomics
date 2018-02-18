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
#   Convert to FlyBase Controlled Vocabulary (FB-CV).
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
    fbcv_unit_tests()

#   Get FB-CV ID.
def get_fbcv_id(phen, user=None):
    fbcv_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["fbcv", "fbcv id", "fbcv identifier", "fb-cv", "fb-cv id", "fb-cv identifier"]:
            if ident["identifier"] not in fbcv_id_array:
                fbcv_id_array.append(ident["identifier"])     
    return fbcv_id_array
        
#   UNIT TESTS
def fbcv_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()