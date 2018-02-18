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
#   Get Vertebrate Taxonomy Ontology (VTO).
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
    vto_unit_tests()
    
#   Get VTO identifiers.
def get_vto_id(taxon):
    vto_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(taxon.identifiers, ["vto", "vto id", "vto identifier"]):
        if iden["identifier"] not in vto_array:
            vto_array.append(iden["identifier"])
    return vto_array

#   UNIT TESTS
def vto_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()