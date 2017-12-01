#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get PSY (Thesaurus of Psychological Index Terms).
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
    psy_unit_tests("21", "50801", "")

# Return PSY.
def get_psy(anat, user = None, source = "umls"):
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
                            # PSY ID.
                            if rep["rootSource"] == "PSY":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="PSY ID", language=None, source="UMLS Metathesaurus")
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
                            # PSY ID.
                            if rep["rootSource"] == "PSY":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="PSY ID", language=None, source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
#   UNIT TESTS
def psy_unit_tests(neu_id, uwda_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("Getting PSY ID from NEU ID (%s):" % neu_id)
    for psy in get_psy(neu_anat, user = user):
        print("- " + str(psy))
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
    print("\nGetting PSY ID from UWDA ID (%s):" % uwda_id)
    for psy in get_psy(uwda_anat, user = user):
        print("- " + str(psy))
    
#   MAIN
if __name__ == "__main__": main()