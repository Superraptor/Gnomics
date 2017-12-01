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
#   Get assays from assay.
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

#   Other imports.
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    assay_assay_unit_tests("1000")
    
# Returns assay cross references.
def get_assays(assay):
    assay_array = []
    for ident in assay.identifiers:
        if ident["identifier_type"].lower() == "aid" or ident["identifier_type"].lower() == "pubchem aid":
            for sub_assay in gnomics.objects.assay.Assay.pubchem_assay(assay):
                for xref in sub_assay["PC_AssayContainer"][0]["assay"]["descr"]["xref"]:
                    if "aid" in xref["xref"]:
                        temp_assay = gnomics.objects.assay.Assay(identifier=xref["xref"]["aid"], identifier_type="PubChem AID", language=None, source="PubChem")
                        assay_array.append(temp_assay)
    return assay_array

#   UNIT TESTS
def assay_assay_unit_tests(pubchem_aid):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    print("Getting assays from PubChem AID (%s)..." % pubchem_aid)
    for res_assay in get_assays(pubchem_assay):
        for ident in res_assay.identifiers:
            if ident["identifier_type"] == "PubChem AID":
                print("- %s" % ident["identifier"])

#   MAIN
if __name__ == "__main__": main()