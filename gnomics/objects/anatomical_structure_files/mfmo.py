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
#   MFMO ID.
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
    mfmo_unit_tests()
    
# Return MFMO ID.
def get_mfmo_id(anat, user=None):
    mfmo_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["mfmo", "mfmo id", "mfmo identifier"]):
        if iden["identifier"] not in mfmo_array:
            mfmo_array.append(iden["identifier"])
    return mfmo_array
    
#   UNIT TESTS
def ceph_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()