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
#   FBbt ID.
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
    fbbt_unit_tests()
    
# Return FBbt ID.
def get_fbbt_id(anat, user=None):
    fbbt_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["drosophila gross anatomy ontology", "drosophila gross anatomy ontology id", "drosophila gross anatomy ontology identifier", "fb-bt", "fb-bt id", "fb-bt identifier", "fbbt", "fbbt id", "fbbt identifier"]):
        if iden["identifier"] not in fbbt_array:
            fbbt_array.append(iden["identifier"])
    return fbbt_array
    
#   UNIT TESTS
def fbbt_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()