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
#   Get references from a compound.
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
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests

#   MAIN
def main():
    compound_reference_unit_tests("36462")
    
# Get references from compound.
def get_references(com):
    ref_array = []
    ref_obj_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/PubMedID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                print("URL not found.")
            else:
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.index(")")
                except ValueError:
                    print("Input is not in a JSONP format.")
                    exit()
                res = str_r[l_index:r_index]
                decoded = json.loads(res)
                for pubmed_id in decoded["InformationList"]["Information"][0]["PubMedID"]:
                    temp_ref = gnomics.objects.reference.Reference(identifier = pubmed_id, identifier_type = "PubMed ID", source = "PubChem")
                    ref_array.append(temp_ref)
                    ref_obj_array.append(temp_ref)
                print(ref_array[0].identifiers)
    return ref_obj_array

#   UNIT TESTS
def compound_reference_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting references from PubChem CID (%s):" % pubchem_cid)
    for ref in get_references(pubchem_com):
        for iden in ref.identifiers:
            print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    
#   MAIN
if __name__ == "__main__": main()