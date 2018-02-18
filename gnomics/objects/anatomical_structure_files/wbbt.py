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
#   WBBT ID.
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
    wbbt_unit_tests()
    
# Return WBBT ID.
def get_wbbt_id(anat, user=None):
    wbbt_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wb-bt", "wb-bt id", "wb-bt identifier", "wbbt", "wbbt id", "wbbt identifier"]):
        if iden["identifier"] not in wbbt_array:
            wbbt_array.append(iden["identifier"])
    return wbbt_array
    
#   UNIT TESTS
def wbbt_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()