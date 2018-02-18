#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#

#
#   Get ChEMBL identifiers.
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
from chembl_webresource_client.new_client import new_client
import json
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    chembl_unit_tests("BTO:0001418", "TS-0171", "UBERON:0002185")
    
#   Get ChEMBL identifier.
def get_chembl_id(tissue, user = None):
    chembl_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl tissue", "chembl tissue id", "chembl tissue identifier"]):
        if iden["identifier"] not in chembl_array:
            chembl_array.append(iden["identifier"])
    
    if chembl_array:
        return chembl_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["bto", "bto id", "bto identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if "_" in proc_id:
                proc_id = proc_id.replace("_", ":")
            
            tissue = new_client.tissue
            res = tissue.filter(bto_id=proc_id)
            
            for sub_res in res:
                if sub_res["tissue_chembl_id"] not in chembl_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["tissue_chembl_id"], identifier_type="ChEMBL ID", source="ChEMBL", name=sub_res["pref_name"])
                    chembl_array.append(res["tissue_chembl_id"])
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["caloha", "caloha id", "caloha identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            tissue = new_client.tissue
            res = tissue.filter(bto_id=proc_id)
            
            for sub_res in res:
                if sub_res["tissue_chembl_id"] not in chembl_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["tissue_chembl_id"], identifier_type="ChEMBL ID", source="ChEMBL", name=sub_res["pref_name"])
                    chembl_array.append(res["tissue_chembl_id"])
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if "_" in proc_id:
                proc_id = proc_id.replace("_", ":")
                
            tissue = new_client.tissue
            res = tissue.filter(bto_id=proc_id)
            
            for sub_res in res:
                if sub_res["tissue_chembl_id"] not in chembl_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["tissue_chembl_id"], identifier_type="ChEMBL ID", source="ChEMBL", name=sub_res["pref_name"])
                    chembl_array.append(res["tissue_chembl_id"])
    
    return chembl_array

#   UNIT TESTS
def chembl_unit_tests(bto_id, caloha_id, uberon_id):
    bto_tiss = gnomics.objects.tissue.Tissue(identifier = bto_id, identifier_type = "BTO ID", source = "ChEMBL")
    print("\nGetting ChEMBL IDs from BTO ID (%s):" % bto_id)
    for chembl in get_chembl_id(bto_tiss):
        print("- %s" % chembl)
        
#   MAIN
if __name__ == "__main__": main()