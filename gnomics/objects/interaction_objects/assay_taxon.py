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
from chembl_webresource_client.new_client import new_client
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    assay_taxa_unit_tests("1000", "CHEMBL767559")
    
# Returns assay cross references.
def get_taxa(assay):
    taxa_array = []
    for ident in assay.identifiers:
        if ident["identifier_type"].lower() == "aid" or ident["identifier_type"].lower() == "pubchem aid":
            for sub_assay in gnomics.objects.assay.Assay.pubchem_assay(assay):
                for xref in sub_assay["PC_AssayContainer"][0]["assay"]["descr"]["xref"]:
                    if "taxonomy" in xref["xref"]:
                        temp_taxon = gnomics.objects.taxon.Taxon(identifier=xref["xref"]["taxonomy"], identifier_type="NCBI Taxonomy ID", language=None, source="PubChem")
                        taxa_array.append(temp_taxon)
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            for sub_assay in gnomics.objects.assay.Assay.chembl_assay(assay):
                print("NOT FUNCTIONAL.")
    return taxa_array

#   UNIT TESTS
def assay_taxa_unit_tests(pubchem_aid, chembl_id):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    print("Getting taxa from PubChem AID (%s)..." % pubchem_aid)
    for res_assay in get_taxa(pubchem_assay):
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Taxonomy ID":
                print("- %s" % ident["identifier"])
    chembl_assay = gnomics.objects.assay.Assay(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
    print("Getting taxa from ChEMBL ID (%s)..." % chembl_id)
    for res_assay in get_taxa(chembl_assay):
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "NCBI Taxonomy ID":
                print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()