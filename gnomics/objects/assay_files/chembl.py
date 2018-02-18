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
#   Get bioassay records (AIDs).
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
import gnomics.objects.compound
import gnomics.objects.assay

#   Other imports.
from chembl_webresource_client.new_client import new_client
import json
import requests

#   MAIN
def main():
    chembl_unit_tests("CHEMBL767559")
    
# Returns ChEMBL assay from ChEMBL ID.
def get_chembl_assay(assay):
    assay_obj_array = []
    for assay_obj in assay.assay_objects:
        if 'object_type' in assay_obj:
            if assay_obj['object_type'].lower() in ['chembl assay', 'chembl']:
                assay_obj_array.append(assay_obj['object'])
    
    if assay_obj_array:
        return assay_obj_array
    
    for chembl_id in get_chembl_id(assay):
        assay_obj = new_client.assay
        result = assay_obj.filter(assay_chembl_id=chembl_id)
        assay.assay_objects.append({
            'object': result[0],
            'object_type': "ChEMBL Assay"
        })
        assay_obj_array.append(result[0])
        
    return assay_obj_array
    
#   Get ChEMBL ID.
def get_chembl_id(assay):
    chembl_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl assay", "chembl assay id", "chembl assay identifier"]):
        if iden["identifier"] not in chembl_array:
            chembl_array.append(iden["identifier"])
    return chembl_array

#   UNIT TESTS
def chembl_unit_tests(chembl_id):
    chembl_assay = gnomics.objects.assay.Assay(identifier = chembl_id, identifier_type = "ChEMBL ID", language = None, source = "ChEMBL")
    print(get_chembl_assay(chembl_assay))

#   MAIN
if __name__ == "__main__": main()