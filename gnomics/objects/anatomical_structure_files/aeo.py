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
#   Anatomical Entity Ontology (AEO).
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
    aeo_unit_tests()
    
# Return AEO ID.
def get_aeo_id(anat, user=None):
    aeo_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["aeo", "aeo id", "aeo identifier", "anatomical entity ontology id", "anatomical entity ontology identifier"]):
        if iden["identifier"] not in aeo_array:
            aeo_array.append(iden["identifier"])
    return aeo_array
    
#   UNIT TESTS
def aeo_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()