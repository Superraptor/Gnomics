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
#   Get references from assays.
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
import gnomics.objects.reference

#   Other imports.
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    assay_reference_unit_tests("CHEMBL767559")
    
# Returns assay references.
def get_references(assay):
    ref_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl assay", "chembl assay id", "chembl assay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_assay in gnomics.objects.assay.Assay.chembl_assay(assay):
                if sub_assay["document_chembl_id"] not in ref_array:
                    temp_ref = gnomics.objects.reference.Reference(identifier = sub_assay["document_chembl_id"], identifier_type = "ChEMBL ID", source = "ChEMBL")
                    ref_array.append(temp_ref)
            
    return ref_array

#   UNIT TESTS
def assay_reference_unit_tests(chembl_id):
    chembl_assay = gnomics.objects.assay.Assay(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
    print("Getting references from ChEMBL ID (%s)..." % chembl_id)
    
    start = timeit.timeit()
    all_refs = get_references(chembl_assay)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for res_assay in all_refs:
        for ident in res_assay.identifiers:
            print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()