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
#   Get scientific name.
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
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    sci_name_unit_tests()
    
#   Get scientific name.
def get_scientific_name(taxon):
    sci_name_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(taxon.identifiers, ["scientific name", "binomial name", "binomial nomenclature", "binomen", "latin name"]):
        if iden["identifier"] not in sci_name_array:
            sci_name_array.append(iden["identifier"]) 
    return sci_name_array

#   UNIT TESTS
def sci_name_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()