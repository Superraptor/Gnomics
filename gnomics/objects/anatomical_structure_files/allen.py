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
#   Allen Brain Atlas ID.
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
    allen_unit_tests()
    
# Return Allen Brain Atlas ID.
def get_allen_brain_atlas_id(anat, user=None):
    allen_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["allen brain atlas id", "allen brain atlas identifier", "allen brain atlas"]):
        if iden["identifier"] not in allen_array:
            allen_array.append(iden["identifier"])
    return allen_array
    
#   UNIT TESTS
def allen_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()