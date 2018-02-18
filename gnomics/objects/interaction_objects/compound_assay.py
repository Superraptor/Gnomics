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
#   Get assays from compound.
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
import gnomics.objects.assay
import gnomics.objects.compound

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    compound_assay_unit_tests("6918092")

def get_assays(compound, user=None):
    aid_array = []
    assay_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(compound.identifiers, ["pubchem cid", "pubchem", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(compound):
                for aid in sub_com.aids:
                    if str(aid) not in aid_array:
                        temp_assay = gnomics.objects.assay.Assay(identifier = str(aid), identifier_type = "PubChem AID", source = "PubChem")
                        assay_array.append(temp_assay)
                        aid_array.append(str(aid))
                    
    return assay_array

#   UNIT TESTS
def compound_assay_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting assays (PubChem AIDs) from compound (PubChem CID) (%s):" % pubchem_cid)
    start = timeit.timeit()
    all_assays = get_assays(pubchem_com)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for assay in all_assays:
        for iden in assay.identifiers:
            print("- %s" % str(iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()