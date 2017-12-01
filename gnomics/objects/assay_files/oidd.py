#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get Open Innovation Lilly Bioassay Records.
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    oidd_unit_tests("29", "", "")
    
#   Get OIDD assay object.
#
#   _format
#       json, tsv, ttl, xml, rdf, rdfjson, html
#   _callback
#       [string]
#   _metadata
#       execution, site, formats, views, all
def get_oidd_bioassay_obj(assay, user):
    for assay_obj in assay.assay_objects:
        if 'object_type' in assay_obj:
            if assay_obj['object_type'].lower() == 'oidd bioassay' or assay_obj['object_type'].lower() == 'oidd':
                return assay_obj['object']
    assay_obj_array = []
    for bio in get_oidd_bioassay_id(assay):
        base = " https://beta.openphacts.org/2.1/"
        ext = "assay?uri=http%3A%2F%2Fopeninnovation.lilly.com%2Fbioassay%23" + bio + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
        r = requests.get(base+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = json.loads(r.text)
        assay.assay_objects.append(
            {
                'object': decoded["result"],
                'object_type': "OIDD Bioassay"
            }
        )
        assay_obj_array.append(decoded["result"])
    return assay_obj_array
    
#   Get Bioassay ID.
def get_oidd_bioassay_id(assay):
    bioassay_array = []
    for ident in assay.identifiers:
        if ident["identifier_type"].lower() == "oidd bioassay id" or ident["identifier_type"].lower() == "oidd bioassay" or ident["identifier_type"].lower() == "oidd bioassay identifier":
            bioassay_array.append(ident["identifier"])
    return bioassay_array

#   UNIT TESTS
def oidd_unit_tests(bioassay_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    bio_assay = gnomics.objects.assay.Assay(identifier = bioassay_id, identifier_type = "OIDD Bioassay ID", source = "OIDD")
    get_oidd_bioassay_obj(bio_assay, user = user)

#   MAIN
if __name__ == "__main__": main()