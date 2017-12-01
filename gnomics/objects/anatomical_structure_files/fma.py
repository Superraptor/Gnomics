#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get FMA.
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
    fma_unit_tests("21", "50801", "Q199507", "")

#   Return FMA ID.
def get_fma_id(anat, user = None, source = "umls"):
    fma_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "fma id" or ident["identifier_type"].lower() == "fma identifier":
            fma_array.append(ident["identifier"])
    if fma_array:
        return fma_array
    anat_array = []
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "fma id" or iden["identifier_type"].lower() == "fma identifier" or iden["identifier_type"].lower() == "foundational model of anatomy id":
            anat_array.append(iden["identifier"])
    if anat_array:
        return anat_array
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # FMA ID.
                            if rep["rootSource"] == "FMA":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="FMA ID", language=None, source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # CCPSS ID.
                            if rep["rootSource"] == "FMA":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="FMA ID", language=None, source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        if iden["identifier_type"].lower() == "wikidata" or iden["identifier_type"].lower() == "wikidata id" or iden["identifier_type"].lower() == "wikidata identifier" or iden["identifier_type"].lower() == "wikidata accession":
            anat_array = []
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
                    if en_prop_name.lower() == "foundational model of anatomy id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Foundational Model of Anatomy ID", language = None, source = "Wikidata")
                            anat_array.append(x["mainsnak"]["datavalue"]["value"])
                return anat_array
        elif (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"].lower() == "en":
            anat_array = []
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
                    if en_prop_name.lower() == "foundational model of anatomy id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Foundational Model of Anatomy ID", language = None, source = "Wikidata")
                            anat_array.append(x["mainsnak"]["datavalue"]["value"])
                return anat_array
        elif ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            anat_array = []
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
                    if en_prop_name.lower() == "foundational model of anatomy id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Foundational Model of Anatomy ID", language = None, source = "Wikidata")
                            anat_array.append(x["mainsnak"]["datavalue"]["value"])
                return anat_array
            
#   UNIT TESTS
def fma_unit_tests(neu_id, uwda_id, wikidata_accession, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("Getting FMA ID from NEU ID (%s):" % neu_id)
    for fma in get_fma_id(neu_anat, user = user):
        print("- " + str(fma))
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
    print("\nGetting FMA ID from UWDA ID (%s):" % uwda_id)
    for fma in get_fma_id(uwda_anat, user = user):
        print("- " + str(fma))
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    print("\nGetting FMA ID from Wikidata Accession (%s):" % wikidata_accession)
    for fma in get_fma_id(wikidata_anat):
        print("- %s" % fma)
    
#   MAIN
if __name__ == "__main__": main()