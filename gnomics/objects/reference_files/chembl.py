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
#   Get ChEMBL document identifier.
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
import gnomics.objects.reference

#   Other imports.
from chembl_webresource_client.new_client import new_client
import json
import re
import requests

#   MAIN
def main():
    chembl_unit_tests("CHEMBL1128639")
    
#   Get ChEMBL document object.
def get_chembl_obj(ref):
    ref_obj_array = []
    for ref_obj in ref.reference_objects:
        if 'object_type' in ref_obj:
            if ref_obj['object_type'].lower() in ["chembl", "chembl document", "chembl document id", "chembl document identifier", "chembl id", "chembl identifier"]:
                ref_obj_array.append(ref_obj['object'])
    
    if ref_obj_array:
        return ref_obj_array
    
    for chembl_id in get_chembl_id(ref):
        document = new_client.document
        res = document.filter(document_chembl_id=chembl_id)
        gnomics.objects.reference.Reference.add_object(ref, obj = res[0], object_type = "ChEMBL Document")
        ref_obj_array.append(res[0])
        
    return ref_obj_array

#   Get ChEMBL ID.
def get_chembl_id(ref): 
    chembl_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl document", "chembl document id", "chembl document identifier"]):
        if iden["identifier"] not in chembl_array:
            chembl_array.append(iden["identifier"])
            
    return chembl_array
        
#   UNIT TESTS
def chembl_unit_tests(chembl_id):
    chembl_ref = gnomics.objects.reference.Reference(identifier = chembl_id, identifier_type = "ChEMBL ID", source = "ChEMBL")
    print(get_chembl_obj(chembl_ref))

#   MAIN
if __name__ == "__main__": main()