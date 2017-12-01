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
#   Convert to HPO.
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
import gnomics.objects.phenotype

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    mesh_unit_tests("10051097", "")

#   Get MeSH UID.
def get_mesh_uid(phen, user):
    mesh_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "mesh id" or ident["identifier_type"].lower() == "mesh identifier" or ident["identifier_type"].lower() == "mesh uid":
            if ident["identifier"] not in mesh_array:
                mesh_array.append(ident["identifier"])
    meddra_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "meddra id" or ident["identifier_type"].lower() == "meddra identifier":
            if ident["identifier"] not in meddra_array:
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/MDR/" + str(ident["identifier"]) + "?targetSource=MSH"
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"string": ident["identifier"], "ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    try:
                        items = json.loads(r.text)
                        json_data = items["result"]
                        empty = False
                        for rep in json_data:
                            if rep["ui"] not in mesh_array and rep["ui"] != "NONE":
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = rep["ui"], identifier_type = "MeSH ID", source = "UMLS")
                                mesh_array.append(rep["ui"])
                            if "ui" not in rep and not rep["result"]:
                                empty = True
                                break
                        if not json_data:
                            break
                        if empty:
                            break
                    except:
                        break
                    break
                meddra_array.append(ident["identifier"])
    return mesh_array

#   UNIT TESTS
def mesh_unit_tests(meddra_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    meddra_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_id, identifier_type = "MedDRA ID", source = "MedDRA")
    print("Getting MeSH UIDs from MedDRA ID (%s):" % meddra_id)
    for iden in get_mesh_uid(meddra_phen, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()