#
#
#
#
#

#
#   IMPORT SOURCES:
#
#

#
#   Get CALOHA identifiers.
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    caloha_unit_tests("TS-0171", "", "")

#   Get CALOHA object.
def get_caloha_obj(tissue, user = None):
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "caloha" or ident["identifier_type"].lower() == "caloha id" or ident["identifier_type"].lower() == "caloha identifier":
            base = "https://beta.openphacts.org/2.1/"
            ext = "tissue?uri=ftp%3A%2F%2Fftp.nextprot.org%2Fpub%2Fcurrent_release%2Fcontrolled_vocabularies%2Fcaloha.obo%23" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            tissue.tissue_objects.append({
                'object': decoded["result"],
                'object_type': "CALOHA Object"
            })
            return decoded["result"]
    
#   Get CALOHA identifier.
def get_caloha_id(tissue):
    caloha_array = []
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "caloha" or ident["identifier_type"].lower() == "caloha id" or ident["identifier_type"].lower() == "caloha identifier":
            caloha_array.append(ident["identifier"])
    return caloha_array

#   UNIT TESTS
def caloha_unit_tests(caloha_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    caloha_tissue = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    get_caloha_obj(caloha_tissue, user = user)
        
#   MAIN
if __name__ == "__main__": main()