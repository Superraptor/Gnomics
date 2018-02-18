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
#   JSTOR.
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
    jstor_unit_tests("Q199507")
    
# Return JSTOR topic ID.
def get_jstor_topic_id(anat, user=None):
    jstor_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["jstor", "jstor id", "jstor identifier", "jstor topic", "jstor topic id", "jstor topic identifier"] and ident["identifier"] not in jstor_array:
            jstor_array.append(ident["identifier"])
            
    if jstor_array:
        return jstor_array
            
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]:
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "jstor topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in jstor_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "JSTOR Topic ID", language = None, source = "Wikidata")
                                jstor_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if jstor_array:
        return jstor_array
    
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession", "wikipedia article"]) and ident["language"].lower() == "en":
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "jstor topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in jstor_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "JSTOR Topic ID", language = None, source = "Wikidata")
                                jstor_array.append(x["mainsnak"]["datavalue"]["value"])
    if jstor_array:        
        return jstor_array
    
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["uberon", "uberon id", "uberon identifier"]:
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "jstor topic id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in jstor_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "JSTOR Topic ID", language = None, source = "Wikidata")
                                jstor_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return jstor_array
    
#   UNIT TESTS
def jstor_unit_tests(wikidata_accession):
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    
    print("Getting JSTOR Topic ID from Wikidata Accession (%s):" % wikidata_accession)
    for jstor in get_jstor_topic_id(wikidata_anat):
        print("- %s" % jstor)
    
#   MAIN
if __name__ == "__main__": main()