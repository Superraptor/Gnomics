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
#   Get tissue from assays.
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
import gnomics.objects.assay
import gnomics.objects.taxon

#   Other imports.
from bioservices import *
from chembl_webresource_client.new_client import new_client
import json
import requests
import timeit

#   MAIN
def main():
    assay_tissue_unit_tests("CHEMBL806641")
    
# Returns assay tissue.
def get_tissue(assay):
    tissue_array = []
    ids_completed = []
                        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl assay", "chembl assay id", "chembl assay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            base = "https://www.ebi.ac.uk"
            ext = "/chembl/api/data/assay/" + iden["identifier"] + ".json"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
                
            else:
                decoded = json.loads(r.text)
                tissue_id = decoded["tissue_chembl_id"]
                
                if tissue_id is not None:
                    
                    temp_tissue = gnomics.objects.tissue.Tissue(identifier=tissue_id, identifier_type="ChEMBL Tissue ID", language=None, source="ChEMBL", name=decoded["assay_tissue"])
                    tissue_array.append(temp_tissue)
            
    return tissue_array

#   UNIT TESTS
def assay_tissue_unit_tests(chembl_id):
    chembl_assay = gnomics.objects.assay.Assay(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
    print("Getting tissue from ChEMBL ID (%s)..." % chembl_id)
    for res_assay in get_tissue(chembl_assay):
        for ident in res_assay.identifiers:
            print("- %s (%s)" % (ident["identifier"], ident["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()