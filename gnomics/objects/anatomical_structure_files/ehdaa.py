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
#   EHDAA (Human Developmental Anatomy Ontology, Abstract).
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
    ehdaa_unit_tests()

# Return EHDAA ID.
def get_ehdaa_id(anat, user=None):
    ehdaa_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["ehdaa", "ehdaa id", "ehdaa identifier", "ehdaa1", "ehdaa1 id", "ehdaa1 identifier"]):
        if iden["identifier"] not in ehdaa_array:
            ehdaa_array.append(iden["identifier"])
    return ehdaa_array
    
# Return EHDAA2 ID.
def get_ehdaa2_id(anat, user=None):
    ehdaa2_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["ehdaa", "ehdaa id", "ehdaa identifier", "ehdaa1", "ehdaa1 id", "ehdaa1 identifier"]):
        if iden["identifier"] not in ehdaa2_array:
            ehdaa2_array.append(iden["identifier"])
    return ehdaa2_array
    
#   UNIT TESTS
def ehdaa_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()