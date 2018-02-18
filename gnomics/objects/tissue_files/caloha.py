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
#   Get CALOHA identifiers.
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    caloha_unit_tests("TS-0171", "", "")

#   Get CALOHA object.
def get_caloha_obj(tissue, user=None):
    obj_array = []
    
    for tiss_obj in tissue.tissue_objects:
        if 'object_type' in tiss_obj:
            if tiss_obj['object_type'].lower() in ["caloha", "caloha id", "caloha identifier", "caloha object"]:
                obj_array.append(tiss_obj['object'])
            
    if obj_array:
        return obj_array
        
    for ident in get_caloha_id(tissue):
            
        base = "https://beta.openphacts.org/2.1/"
        ext = "tissue?uri=ftp%3A%2F%2Fftp.nextprot.org%2Fpub%2Fcurrent_release%2Fcontrolled_vocabularies%2Fcaloha.obo%23" + str(ident) + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
        
        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            decoded = json.loads(r.text)
            gnomics.objects.tissue.Tissue.add_object(tissue, obj = decoded["result"], object_type = "CALOHA Object")
            obj_array.append(decoded["result"])
            
    return obj_array
    
#   Get CALOHA identifier.
def get_caloha_id(tissue, user=None):
    caloha_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["caloha", "caloha id", "caloha identifier"]):
        if iden["identifier"] not in caloha_array:
            caloha_array.append(iden["identifier"])
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl tissue", "chembl tissue id", "chembl tissue identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            tissue_temp = new_client.tissue
            res = tissue_temp.filter(chembl_id=iden["identifier"])
            
            for sub_res in res:
                if sub_res["caloha_id"] not in caloha_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["caloha_id"], identifier_type="CALOHA ID", source="ChEMBL", name=sub_res["pref_name"])
                    caloha_array.append(sub_res["caloha_id"])
    
    return caloha_array

#   UNIT TESTS
def caloha_unit_tests(caloha_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    caloha_tissue = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    get_caloha_obj(caloha_tissue, user = user)
        
#   MAIN
if __name__ == "__main__": main()