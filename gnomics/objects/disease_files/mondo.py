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
#   Get SNOMED.
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
import gnomics.objects.disease

#   Other imports.
import json
import requests

#   MAIN
def main():
    mondo_unit_tests()

#   Get MONDO IDs.
def get_mondo_id(dis, user = None):
    mondo_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(dis.identifiers, ["monarch disease ontology id", "monarch disease ontology identifier", "mondo id", "mondo identifier", "monarch disease ontology"]):
        if iden["identifier"] not in mondo_array:
            mondo_array.append(iden["identifier"])                  
    return mondo_array
    
#   UNIT TESTS
def mondo_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()