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
#   Get MMDB (Molecular Modeling Database) ID.
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

#   Other imports.
import pubchempy as pubchem
import json
import requests

#   MAIN
def main():
    mmdb_unit_tests("36462")
    
# Get MMDB IDs.
def get_mmdb(com):
    mmdb_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "mmdb" or ident["identifier_type"].lower() == "mmdb id" or ident["identifier_type"].lower() == "mmdb identifier" or ident["identifier_type"].lower() == "mmdbid":
            if ident["identifier"] not in mmdb_array:
                mmdb_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/MMDBID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.index(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for result in decoded["InformationList"]["Information"]:
                mms = result["MMDBID"]
                for mm in mms:
                    if mm not in mmdb_array:
                        com.identifiers.append({
                            'identifier': mm,
                            'language': None,
                            'identifier_type': "MMDB ID",
                            'source': "MMDB"
                        })
                        mmdb_array.append(mm)
    return mmdb_array

#   UNIT TESTS
def mmdb_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting MMDB IDs from PubChem CID (%s):" % pubchem_cid)
    for mm in get_mmdb(pubchem_com):
        print("- %s" % str(mm))
    
#   MAIN
if __name__ == "__main__": main()