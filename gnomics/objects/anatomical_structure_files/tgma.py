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
#   TGMA ID.
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
    tgma_unit_tests()
    
# Return TGMA ID.
def get_tgma_id(anat, user=None):
    tgma_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["tgma", "tgma id", "tgma identifier"]):
        if iden["identifier"] not in tgma_array:
            tgma_array.append(iden["identifier"])
    return tgma_array
    
#   UNIT TESTS
def tgma_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()