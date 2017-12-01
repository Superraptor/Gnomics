#
#
#
#
#

#
#   IMPORT SOURCES:
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    ta_unit_tests("Q228537")
    
# Return TA98 ID.
def get_ta98_id(anat, user = None):
    ta_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "ta98 id" or ident["identifier_type"].lower() == "ta98 identifier" or ident["identifier_type"].lower() == "ta98" or ident["identifier_type"].lower() == "terminologia anatomica" or ident["identifier_type"].lower() == "terminologia anatomica 1998" or ident["identifier_type"].lower() == "terminologia anatomica 98 id":
            ta_array.append(ident["identifier"])
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
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
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"].lower() == "en":
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
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
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
def get_ta98_latin_term(anat, user = None):
    ta_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "ta98 latin term" or ident["identifier_type"].lower() == "terminologia anatomica 98 latin term" or ident["identifier_type"].lower() == "terminologia anatomica 1998 latin term":
            ta_array.append(ident["identifier"])
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
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
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"].lower() == "en":
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
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
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