#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get genes from assays.
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
import gnomics.objects.compound
import gnomics.objects.gene

#   Other imports.
from bioservices import *
from chembl_webresource_client.new_client import new_client
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    assay_gene_unit_tests("1000")
    
# Returns assay cross references.
def get_genes(assay, user=None):
    gene_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["pubchem aid", "pubchem", "pubchem assay id", "pubchem assay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])

            for sub_assay in gnomics.objects.assay.Assay.pubchem_assay(assay):
                for xref in sub_assay["PC_AssayContainer"][0]["assay"]["descr"]["xref"]:
                    if "gene" in xref["xref"]:
                        temp_gene = gnomics.objects.gene.Gene(identifier=xref["xref"]["gene"], identifier_type="NCBI Gene ID", language=None, source="PubChem")
                        gene_array.append(temp_gene)
            
    return gene_array

#   UNIT TESTS
def assay_gene_unit_tests(pubchem_aid):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    print("Getting genes from PubChem AID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    all_genes = get_genes(pubchem_assay)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for res_assay in all_genes:
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Gene ID":
                print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()