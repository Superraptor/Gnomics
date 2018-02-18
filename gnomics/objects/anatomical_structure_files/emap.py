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
#   EMAP/EMAPA ID.
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
    emap_unit_tests()
    
# Return EMAP ID.
def get_emap_id(anat, user=None):
    emap_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["emap", "emap id", "emap identifier"]):
        if iden["identifier"] not in emap_array:
            emap_array.append(iden["identifier"])   
    return emap_array

# Return EMAPA ID.
def get_emapa_id(anat, user=None):
    emapa_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["emapa", "emapa id", "emapa identifier"]):
        if iden["identifier"] not in emapa_array:
            emapa_array.append(iden["identifier"])
    return emapa_array
    
#   UNIT TESTS
def emap_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()