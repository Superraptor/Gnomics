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
#   Get Quora Topic ID.
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
    quora_unit_tests()

#   Get Quora Topic ID.
def get_quora_topic_id(dis):
    dis_array = []
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["quora", "quora id", "quora identifier", "quora topic", "quora topic id", "quora topic identifier"]:
            if ident["identifier"] not in dis_array:
                dis_array.append(ident["identifier"])
                
    if dis_array:
        return dis_array
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
            for stuff in gnomics.objects.disease.Disease.wikidata(dis):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "quora topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in dis_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=x["mainsnak"]["datavalue"]["value"], identifier_type="Quora Topic ID", language=None, source="Wikidata")
                                dis_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if dis_array:
        return dis_array
    
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"].lower() == "en":
            for stuff in gnomics.objects.disease.Disease.wikidata(dis):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "quora topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in dis_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=x["mainsnak"]["datavalue"]["value"], identifier_type="Quora Topic ID", language=None, source="Wikidata")
                                dis_array.append(x["mainsnak"]["datavalue"]["value"])
    if dis_array:        
        return dis_array
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            gnomics.objects.disease.Disease.wikipedia_accession(dis, language = "en")
            for stuff in gnomics.objects.disease.Disease.wikidata(dis):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "quora topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in dis_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=x["mainsnak"]["datavalue"]["value"], identifier_type="Quora Topic ID", language=None, source="Wikidata")
                                dis_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return dis_array

#   UNIT TESTS
def quora_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()