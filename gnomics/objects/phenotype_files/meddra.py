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
    meddra_unit_tests("Temporomandibular joint syndrome", "10011233", "")

#   Get MedDRA ID.
def get_meddra_id(phen, user):
    meddra_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "meddra id" or ident["identifier_type"].lower() == "meddra identifier":
            if ident["identifier"] not in meddra_array:
                hpo_id_array.append(ident["identifier"])
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "meddra term":
            umls_tgt = User.umls_tgt(user)
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/search/current?sabs=MDR&searchType=exact&returnIdType=code"
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
                    for rep in json_data["results"]:
                        if rep["ui"] not in meddra_array and rep["ui"] != "NONE":
                            gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = rep["ui"], identifier_type = "MedDRA ID", source = "UMLS")
                            meddra_array.append(rep["ui"])
                        if json_data["results"][0]["ui"] == "NONE":
                            empty = True
                            break
                    if not json_data:
                        break
                    if empty:
                        break
                except:
                    break
    if meddra_array:
        return meddra_array
    for ident in phen.identifiers:
        return ""

#   UNIT TESTS
def meddra_unit_tests(meddra_term, meddra_id, umls_api_key):
    user = User(umls_api_key = "c8ec0cca-e10f-485b-bf82-ea0e07000f4f")
    meddra_term_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_term, identifier_type = "MedDRA Term", source = "MedDRA")
    print("Getting MedDRA IDs from MedDRA term (%s):" % meddra_term)
    for iden in get_meddra_id(meddra_term_phen, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()