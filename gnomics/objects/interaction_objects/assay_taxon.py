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
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get taxa from assays.
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
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    assay_taxa_unit_tests("1000", "CHEMBL806641")
    
# Returns assay taxon.
def get_taxon(assay):
    taxa_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["pubchem", "pubchem aid", "pubchem assay id", "pubchem assay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_assay in gnomics.objects.assay.Assay.pubchem_assay(assay):
                for xref in sub_assay["PC_AssayContainer"][0]["assay"]["descr"]["xref"]:
                    if "taxonomy" in xref["xref"]:
                        temp_taxon = gnomics.objects.taxon.Taxon(identifier=xref["xref"]["taxonomy"], identifier_type="NCBI Taxonomy ID", language=None, source="PubChem")
                        taxa_array.append(temp_taxon)
                        
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
                tax_id = decoded["assay_tax_id"]
                
                if tax_id is not None:
                    temp_taxon = gnomics.objects.taxon.Taxon(identifier=tax_id, identifier_type="NCBI Taxonomy ID", language=None, source="ChEMBL", name=decoded["assay_organism"])
                    taxa_array.append(temp_taxon)
            
    return taxa_array

#   UNIT TESTS
def assay_taxa_unit_tests(pubchem_aid, chembl_id):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    print("Getting taxa from PubChem AID (%s)..." % pubchem_aid)
    
    start = timeit.timeit()
    all_taxa = get_taxon(pubchem_assay)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for res_assay in all_taxa:
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Taxonomy ID":
                print("- %s" % ident["identifier"])
                
    chembl_assay = gnomics.objects.assay.Assay(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
    print("\nGetting taxa from ChEMBL ID (%s)..." % chembl_id)
    for res_assay in get_taxon(chembl_assay):
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Taxonomy ID":
                print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()