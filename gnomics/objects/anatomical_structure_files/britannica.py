#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Encyclopædia Britannica Online.
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
    britannica_unit_tests("Q199507")
    
# Return Encyclopædia Britannica Online ID.
def get_encyclopedia_britannica_online_id(anat):
    britannica_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "encyclopedia britannica online id" or ident["identifier_type"].lower() == "encyclopedia britannica online identifier":
            britannica_array.append(ident["identifier"])
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
                    if en_prop_name.lower() == "encyclopædia britannica online id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Encyclopædia Britannica Online ID", language = None, source = "Wikidata")
                            britannica_array.append(x["mainsnak"]["datavalue"]["value"])
    if britannica_array:
        return britannica_array
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
                    if en_prop_name.lower() == "encyclopædia britannica online id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Encyclopædia Britannica Online ID", language = None, source = "Wikidata")
                            britannica_array.append(x["mainsnak"]["datavalue"]["value"])
    if britannica_array:        
        return britannica_array
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
                    if en_prop_name.lower() == "encyclopædia britannica online id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Encyclopædia Britannica Online ID", language = None, source = "Wikidata")
                            britannica_array.append(x["mainsnak"]["datavalue"]["value"])
    return britannica_array
    
#   UNIT TESTS
def britannica_unit_tests(wikidata_accession):
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    print("Getting Encyclopedia Britannica Online ID from Wikidata Accession (%s):" % wikidata_accession)
    for brit in get_encyclopedia_britannica_online_id(wikidata_anat):
        print("- %s" % brit)
    
#   MAIN
if __name__ == "__main__": main()