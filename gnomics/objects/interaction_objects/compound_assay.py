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

#   MAIN
def main():
    aids_unit_tests("6918092")

def get_assays(compound):
    aid_array = []
    assay_array = []
    for ident in compound.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            aid_array_from_pubchem = gnomics.objects.compound.Compound.pubchem_compound(compound).aids
            for aid in aid_array_from_pubchem:
                if aid not in aid_array:
                    temp_assay = gnomics.objects.assay.Assay(identifier = aid, identifier_type = "PubChem AID", source = "PubChem")
                    assay_array.append(temp_assay)
                    aid_array.append(aid)
    return assay_array

#   UNIT TESTS
def aids_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting assays (PubChem AIDs) from compound (PubChem CID) (%s):" % pubchem_cid)
    for assay in assays(pubchem_com):
        for iden in assay.identifiers:
            print("- %s" % str(iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()