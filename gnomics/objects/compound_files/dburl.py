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
#   Get database home page URL.
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
    ext_db_url_unit_tests("36462")
    
# Get database home page URL.
def get_ext_db_url(com):
    db_url_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/DBURL/JSONP"
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
                db_urls = result["DBURL"]
                for db_url in db_urls:
                    if db_url not in db_url_array:
                        db_url_array.append(db_url)
    return db_url_array

# Get substance URL.
def get_substance_url(com):
    db_url_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/SBURL/JSONP"
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
                db_urls = result["SBURL"]
                for db_url in db_urls:
                    if db_url not in db_url_array:
                        db_url_array.append(db_url)
    return db_url_array

#   UNIT TESTS
def ext_db_url_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting external database home page URLs from PubChem CID (%s):" % pubchem_cid)
    for url in get_ext_db_url(pubchem_com):
        print("- %s" % str(url))
    print("\nGetting external database substance URLs from PubChem CID (%s):" % pubchem_cid)
    for url in get_substance_url(pubchem_com):
        print("- %s" % str(url))
    
#   MAIN
if __name__ == "__main__": main()