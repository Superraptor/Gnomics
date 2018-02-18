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
#   Get FMA identifiers.
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
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    fma_unit_tests("TS-0171", "", "")
    
#   Get FMA identifier.
def get_fma_id(tissue, user = None):
    fma_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["fma", "fma id", "fmaid", "fma identifier"]):
        if iden["identifier"] not in fma_array:
            fma_array.append(iden["identifier"])
            
    if fma_array:
        return fma_array
    
    ids_completed = []
    for ident in tissue.identifiers:
        if (ident["identifier_type"].lower() in ["caloha", "caloha id", "caloha identifier"]) and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            for xref in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user)["primaryTopic"]["hasDbXref"]:
                if "FMA" in xref:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref, identifier_type = "FMA ID", source = "OpenPHACTS")
                    fma_array.append(xref)
    
    return fma_array

#   UNIT TESTS
def fma_unit_tests(caloha_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    for fma in get_fma_id(caloha_tiss, user = user):
        print("- %s" % fma)
        
#   MAIN
if __name__ == "__main__": main()