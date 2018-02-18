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
#   Get Ensembl Protein ID.
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
import gnomics.objects.protein

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    ensembl_unit_tests()
    
# Returns Ensembl object.
def get_ensembl_protein(protein):
    ensembl_obj_array = []
    
    for prot_obj in protein.protein_objects:
        if prot_obj["object_type"].lower() in ["ensembl", "ensembl protein", "ensembl object", "ensembl protein object"]:
            ensembl_obj_array.append(prot_obj["object"])
    
    if ensembl_obj_array:
        return ensembl_obj_array
    
    for ensembl_id in get_ensembl_protein_id(protein):
        server = "https://rest.ensembl.org"
        ext = "/lookup/id/" + str(ensembl_id) + "?expand=1"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        
        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            new_ensembl_obj = {
                'object_type': decoded["object_type"],
                'db_type': decoded["db_type"],
                'length': decoded["length"],
                'id': decoded["id"],
                'species': decoded["species"],
                'end': decoded["end"],
                'start': decoded["start"]
            }
            temp_ensembl_obj = {
                'object': new_ensembl_obj,
                'object_type': "Ensembl Transcript"
            }
            gnomics.objects.protein.Protein.add_object(transcript, obj = new_ensembl_obj, object_type = "Ensembl Transcript")
            ensembl_obj_array.append(new_ensembl_obj)
        
    return ensembl_obj_array
    
#   Get Ensembl Protein ID.
def get_ensembl_protein_id(prot):
    ensembl_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl protein", "ensembl protein id", "ensembl protein identifier"]:
            ensembl_array.append(ident["identifier"])
    return ensembl_array
    
#   UNIT TESTS
def ensembl_unit_tests():
    print("NOT FUNCTIONAL.")
        
#   MAIN
if __name__ == "__main__": main()