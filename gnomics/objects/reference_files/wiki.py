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
#   Get Wikipedia, Wikidata.
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
import gnomics.objects.reference

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   Other imports.
from wikidata.client import Client

#   MAIN
def main():
    wiki_unit_tests()
    
#   Get Wikidata accession.
def get_wikidata_accession(ref):
    wiki_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in wiki_array:
            wiki_array.append(iden["identifier"])
    return wiki_array
            
#   Get Wikidata object.
def get_wikidata_object(ref):
    wikidata_obj_array = []
    for ref_obj in ref.reference_objects:
        if 'object_type' in ref_obj:
            if ref_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(ref_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in [get_wikidata_accession(ref)]:
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.reference.Reference.add_object(ref, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   UNIT TESTS
def wiki_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()