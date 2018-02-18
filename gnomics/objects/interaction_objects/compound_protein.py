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
#   Get protein from compound.
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
import gnomics.objects.protein

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    compound_protein_unit_tests("3540")

def get_protein(compound, user=None):
    protein_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(compound.identifiers, ["pubchem cid", "pubchem", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(iden["identifier"]) + "/xrefs/MMDBID,ProteinGI/JSON/"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                for info in decoded["InformationList"]["Information"]:
                    if "MMDBID" in info:
                        for mmdbid in info["MMDBID"]:
                            temp_prot = gnomics.objects.protein.Protein(identifier=str(mmdbid), identifier_type="MMDB ID", language=None, source="PubChem")
                            protein_array.append(temp_prot)
                    if "ProteinGI" in info:
                        for protein_gi in info["ProteinGI"]:
                            temp_prot = gnomics.objects.protein.Protein(identifier=str(protein_gi), identifier_type="NCBI Protein GI", language=None, source="PubChem")
                            protein_array.append(temp_prot)
                    
    return protein_array

#   UNIT TESTS
def compound_protein_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting protein from compound (PubChem CID) (%s):" % pubchem_cid)
    
    start = timeit.timeit()
    all_proteins = get_protein(pubchem_com)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for protein in all_proteins:
        for iden in protein.identifiers:
            print("- %s" % str(iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()