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
#   Get CPM (Medical Entities Dictionary).
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
    cpm_unit_tests("21", "50801", "")

# Return CPM.
def get_cpm(anat, user=None, source="umls"):
    
    cpm_array = []
    
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["cpm", "cpm code", "cpm id", "cpm identifier", "med", "med code", "med id", "med identifier"] and iden["identifier"] not in cpm_array:
            cpm_array.append(iden["identifier"])
            
    if cpm_array:
        return cpm_array
    
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["neu id", "neu identifier", "neu", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]:
    
            if source.lower() in ["umls", "all"]:

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
                    
                    with open("sample_2.txt", "a", encoding="utf8") as f:
                        f.write(str(items))
                    
                    for rep in json_data:
                        if rep["ui"] != "NONE":

                            # CPM ID.
                            if rep["rootSource"] == "CPM" and rep["ui"] not in cpm_array:
                                cpm_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CPM ID", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break
            
        elif iden["identifier_type"].lower() in ["uwda id", "uwda identifier", "uwda"]:
    
            if source.lower() in ["umls", "all"]:

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
                    
                    with open("sample_2.txt", "a", encoding="utf8") as f:
                        f.write(str(items))
                    
                    for rep in json_data:
                        if rep["ui"] != "NONE":

                            # CPM ID.
                            if rep["rootSource"] == "CPM" and rep["ui"] not in cpm_array:
                                cpm_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CPM ID", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break
            
        elif iden["identifier_type"].lower() in ["rcd", "rcd id", "rcd identifier", "read code", "read code clinical terms version 3", "read code ctv3", "read code, clinical terms version 3", "read code, ctv3"]:
    
            if source == "umls":

                anat_array = []

                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/RCD/" + iden["identifier"]

                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] != "NONE":

                            # CPM ID.
                            if rep["rootSource"] == "CPM" and rep["ui"] not in cpm_array:
                                cpm_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CPM ID", language=None, source="UMLS Metathesaurus", name=rep["name"])

                    if not json_data:
                        break
            
        elif iden["identifier_type"].lower() in ["alcohol and other drug", "alcohol and other drug id", "alcohol and other drug identifier", "aod", "aod id", "aod identifier"]:
    
            if source == "umls":

                anat_array = []

                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/AOD/" + iden["identifier"]

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

                            # CPM ID.
                            if rep["rootSource"] == "CPM" and rep["ui"] not in cpm_array:
                                cpm_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CPM ID", language=None, source="UMLS Metathesaurus", name=rep["name"])

                    if not json_data:
                        break
            
    return cpm_array
    
#   UNIT TESTS
def cpm_unit_tests(neu_id, uwda_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("Getting CPM ID from NEU ID (%s):" % neu_id)
    for cpm in get_cpm(neu_anat, user = user):
        print("- " + str(cpm))
        
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
    print("\nGetting CPM ID from UWDA ID (%s):" % uwda_id)
    for cpm in get_cpm(uwda_anat, user = user):
        print("- " + str(cpm))
    
#   MAIN
if __name__ == "__main__": main()