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
import gnomics.objects.symptom

#   Other imports.
from wikidata.client import Client
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    wiki_unit_tests()
    
#   Get Wikidata accession.
def get_wikidata_accession(symptom):
    wiki_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(symptom.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in wiki_array:
            wiki_array.append(iden["identifier"])
    return wiki_array
            
#   Get Wikidata object.
def get_wikidata_object(symptom):
    wikidata_obj_array = []
    for symp_obj in symptom.symptom_objects:
        if 'object_type' in symp_obj:
            if symp_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(symp_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in [get_wikidata_accession(symptom)]:
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.symptom.Symptom.add_object(taxon, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   UNIT TESTS
def wiki_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()