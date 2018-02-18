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
#   Get CCPSS.
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
    ccpss_unit_tests("21", "50801", "")

# Return CCPSS.
def get_ccpss(anat, user=None, source="umls"):
    
    ccpss_array = []
    
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["ccpss", "ccpss id", "ccpss identifier"] and iden["identifier"] not in ccpss_array:
            ccpss_array.append(iden["identifier"])
            
    if ccpss_array:
        return ccpss_array
    
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]:
    
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
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":

                            # CCPSS ID.
                            if rep["rootSource"] == "CCPSS" and rep["ui"] not in ccpss_array:
                                ccpss_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CCPSS ID", language=None, source="UMLS Metathesaurus")

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
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":

                            # CCPSS ID.
                            if rep["rootSource"] == "CCPSS" and rep["ui"] not in ccpss_array:
                                ccpss_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="CCPSS ID", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break

    return ccpss_array
    
#   UNIT TESTS
def ccpss_unit_tests(neu_id, uwda_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
        
    print("Getting CCPSS ID from NEU ID (%s):" % neu_id)
    for ccpss in get_ccpss(neu_anat, user = user):
        print("- " + str(ccpss))
        
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
        
    print("\nGetting CCPSS ID from UWDA ID (%s):" % uwda_id)
    for ccpss in get_ccpss(uwda_anat, user = user):
        print("- " + str(ccpss))
    
#   MAIN
if __name__ == "__main__": main()