#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
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
import pubchempy as pubchem
import json
import requests

#   MAIN
def main():
    aids_unit_tests("1000", "29", "", "")
    
# Returns PubChem assay from AID.
def get_pubchem_assay(assay):
    assay_obj_array = []
    for assay_obj in assay.assay_objects:
        if 'object_type' in assay_obj:
            if assay_obj['object_type'].lower() in ['pubchem assay', 'pubchem']:
                assay_obj_array.append(assay_obj['object'])
    
    if assay_obj_array:
        return assay_obj_array
    
    for aid in get_aids(assay):
        base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
        ext = "assay/aid/" + str(aid) + "/JSON"

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = json.loads(r.text)      
        pubchem_assay = decoded

        assay.assay_objects.append({
            'object': pubchem_assay,
            'object_type': "PubChem Assay"
        })
        assay_obj_array.append(pubchem_assay)
        
    return assay_obj_array
    
#   Get AIDs.
def get_aids(assay, user=None):
    aid_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["pubchem", "pubchem aid", "pubchem assay id", "pubchem assay identifier"]):
        if iden["identifier"] not in aid_array:
            aid_array.append(iden["identifier"])
            
    if aid_array:
        return aid_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["oidd", "oidd bioassay", "oidd id", "oidd identifier", "oidd bioassay id", "oidd bioassay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for obj in gnomics.objects.assay.Assay.oidd_bioassay(assay, user=user):
                temp_aid = obj["primaryTopic"]["exactMatch"]["_about"].split("AID")[1]
                aid_array.append(temp_aid)
                gnomics.objects.assay.Assay.add_identifier(assay, identifier=temp_aid, identifier_type="PubChem AID", language=None, source="OpenPHACTS")
            
    return aid_array

#   UNIT TESTS
def aids_unit_tests(pubchem_aid, bioassay_id, openphacts_app_id, openphacts_app_key):
    assay = gnomics.objects.assay.Assay(identifier = pubchem_aid, identifier_type = "PubChem AID", language = None, source = "PubChem")
    print(get_pubchem_assay(assay))
    
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    bio_assay = gnomics.objects.assay.Assay(identifier = bioassay_id, identifier_type = "OIDD Bioassay ID", source = "OIDD")
    print("\nGetting PubChem AIDs from OIDD Bioassay ID (%s):" % bioassay_id)
    for iden in get_aids(bio_assay, user = user):
        print("- %s" % iden)

#   MAIN
if __name__ == "__main__": main()