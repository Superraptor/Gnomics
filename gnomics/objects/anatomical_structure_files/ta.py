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
#   Terminologica Anatomica (TA) 98.
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
    ta_unit_tests("Q228537")
    
# Return TA98 ID.
def get_ta98_id(anat, user=None):
    ta_array = []
    
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["ta98 id", "ta98 identifier", "ta98", "terminologia anatomica", "terminologia anatomica 1998", "terminologia anatomica 98 id"]:
            ta_array.append(ident["identifier"])
            
    if ta_array:
        return ta_array
            
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
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

                    if en_prop_name.lower() == "terminologia anatomica 98 id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Terminologia Anatomica 98 ID", language = None, source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if ta_array:
        return ta_array

    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"].lower() == "en":
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

                    if en_prop_name.lower() == "ta98 latin term":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "TA98 Latin Term", language = "la", source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
    if ta_array:        
        return ta_array
    
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

                    if en_prop_name.lower() == "ta98 latin term":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "TA98 Latin Term", language = "la", source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return ta_array
    
# Return TA98 Latin Term.
def get_ta98_latin_term(anat, user=None):
    ta_array = []
    
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["ta98 latin term", "terminologia anatomica 98 latin term", "terminologia anatomica 1998 latin term"]:
            ta_array.append(ident["identifier"])
            
    if ta_array:
        return ta_array
            
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
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

                    if en_prop_name.lower() == "ta98 latin term":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "TA98 Latin Term", language = "la", source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if ta_array:
        return ta_array
    
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"].lower() == "en":
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

                    if en_prop_name.lower() == "ta98 latin term":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "TA98 Latin Term", language = "la", source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
    if ta_array:        
        return ta_array
    
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

                    if en_prop_name.lower() == "ta98 latin term":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "TA98 Latin Term", language = "la", source = "Wikidata")
                            ta_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return ta_array
    
#   UNIT TESTS
def ta_unit_tests(wikidata_accession):
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    
    print("Getting TA 98 identifier from Wikidata Accession (%s):" % wikidata_accession)
    for ta in get_ta98_id(wikidata_anat):
        print("- %s" % ta)
        
    print("\nGetting TA 98 Latin term from Wikidata Accession (%s):" % wikidata_accession)
    for ta in get_ta98_latin_term(wikidata_anat):
        print("- %s" % ta)
    
#   MAIN
if __name__ == "__main__": main()