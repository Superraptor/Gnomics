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
#   Freebase.
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
    freebase_unit_tests("Q228537")
    
# Return Freebase ID.
def get_freebase_id(anat, user=None):
    fr_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["freebase", "freebase id", "freebase identifier"] and ident["identifier"] not in fr_array:
            fr_array.append(ident["identifier"])
            
    if fr_array:
        return fr_array
            
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

                    if en_prop_name.lower() == "freebase id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in fr_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Freebase ID", language = None, source = "Wikidata")
                                fr_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if fr_array:
        return fr_array
    
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

                    if en_prop_name.lower() == "freebase id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in fr_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Freebase ID", language = None, source = "Wikidata")
                                fr_array.append(x["mainsnak"]["datavalue"]["value"])
    if fr_array:        
        return fr_array
    
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

                    if en_prop_name.lower() == "freebase id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in fr_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Freebase ID", language = None, source = "Wikidata")
                                fr_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return fr_array
    
#   UNIT TESTS
def freebase_unit_tests(wikidata_accession):
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    
    print("Getting Freebase ID from Wikidata Accession (%s):" % wikidata_accession)
    for fr in get_freebase_id(wikidata_anat):
        print("- %s" % fr)
    
#   MAIN
if __name__ == "__main__": main()