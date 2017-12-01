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
import gnomics.objects.gene

#   Other imports.
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    assay_gene_unit_tests("1000")
    
# Returns assay cross references.
def get_genes(assay):
    gene_array = []
    for ident in assay.identifiers:
        if ident["identifier_type"].lower() == "aid" or ident["identifier_type"].lower() == "pubchem aid":
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
    for res_assay in get_genes(pubchem_assay):
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Gene ID":
                print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()