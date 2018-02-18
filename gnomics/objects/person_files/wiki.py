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
#   Get Wikipedia information.
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
import gnomics.objects.person

#   Other imports.
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
import json
import requests

#   MAIN
def main():
    wiki_unit_tests()
    
#   Get Wikipedia accession (English).
def get_english_wikipedia_accession(person, user=None):
    wiki_array = []
    for ident in person.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "en":
            wiki_array.append(ident["identifier"])
    return wiki_array

#   Get Wikidata accession.
def get_wikidata_accession(person):
    person_array = []
    
    for ident in person.identifiers:
        if ident["identifier_type"].lower() in ["wikidata accession", "wikidata"]:
            person_array.append(ident["identifier"])
            
    if person_array:
        return person_array
            
    for ident in person.identifiers:
        if ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]:
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            for key, value in decoded["query"]["pages"].items():
                if "pageprops" in value:
                    wikidata_id = value["pageprops"]["wikibase_item"]
                    gnomics.objects.person.Person.add_identifier(person, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                    person_array.append(wikidata_id)
                    
                elif "pageid" in value:
                    wikidata_id = value["pageid"]
                    if "Q" in str(wikidata_id):
                        gnomics.objects.person.Person.add_identifier(person, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                        person_array.append(wikidata_id)
                    
    return person_array

#   Get Wikidata object.
def get_wikidata_object(person):
    wikidata_obj_array = []
    for per_obj in person.person_objects:
        if 'object_type' in per_obj:
            if per_obj['object_type'].lower() == 'wikidata object' or per_obj['object_type'].lower() == 'wikidata':
                wikidata_obj_array.append(per_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in get_wikidata_accession(person):
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.person.Person.add_object(person, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   UNIT TESTS
def wiki_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()