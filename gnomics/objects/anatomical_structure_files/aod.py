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
#   Get AOD (Alcohol and Other Drug Thesaurus).
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
    aod_unit_tests("21", "50801", "")

# Return AOD.
def get_aod(anat, user=None, source="umls"):
    
    aod_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["alcohol and other drug", "alcohol and other drug id", "alcohol and other drug identifier", "aod", "aod id", "aod identifier"]):
        if iden["identifier"] not in aod_array:
            aod_array.append(iden["identifier"])
            
    if aod_array:
        return aod_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier", "neu"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            if source.lower() in ["umls", "all"]:

                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + str(iden["identifier"])

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

                            # AOD ID.
                            if rep["rootSource"] == "AOD" and rep["ui"] not in aod_array:
                                aod_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="AOD ID", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break

    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            if source.lower() in ["umls", "all"]:

                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + str(iden["identifier"])

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

                            # AOD ID.
                            if rep["rootSource"] == "AOD" and rep["ui"] not in aod_array:
                                aod_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="AOD ID", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break
            
    return aod_array
    
#   UNIT TESTS
def aod_unit_tests(neu_id, uwda_id, umls_api_key):
            
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("Getting AOD IDs from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    aod_array = get_aod(neu_anat, user=user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for aod in aod_array:
        print("\t- %s" % str(aod))
        
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
    print("\nGetting AOD IDs from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    aod_array = get_aod(uwda_anat, user=user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for aod in aod_array:
        print("\t- %s" % str(aod))
    
#   MAIN
if __name__ == "__main__": main()