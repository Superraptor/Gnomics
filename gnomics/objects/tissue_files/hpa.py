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
#   HPA (Human Protein Atlas).
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    hpa_unit_tests()
    
# Return HPA accession.
def get_hpa_accession(tissue, user=None):
    hpa_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["hpa", "hpa accession", "hpa id", "hpa identifier", "human protein atlas", "human protein atlas accession", "human protein atlas id", "human protein atlas identifier"]):
        if iden["identifier"] not in hpa_array:
            hpa_array.append(iden["identifier"])
    return hpa_array
    
#   UNIT TESTS
def hpa_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()