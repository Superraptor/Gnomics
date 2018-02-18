#!/usr/bin/env python

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
def get_meddra_id(phen, user=None):
    meddra_array = []
    
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["mdr", "mdr code", "mdr id", "mdr identifier", "meddra", "meddra code", "meddra id", "meddra identifier"]:
            if ident["identifier"] not in meddra_array:
                hpo_id_array.append(ident["identifier"])

    ids_completed = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["meddra term", "meddra label", "mdr label", "mdr term"]:
            if user is not None:
            
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
                    
        elif ident["identifier_type"].lower() in ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                hpo_id = ident["identifier"]
                if ":" in hpo_id:
                    hpo_id = hpo_id.replace(":", "_")

                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/hp/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + hpo_id
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
    
    if meddra_array:
        return meddra_array
    
    for ident in phen.identifiers:
        print("NOT FUNCTIONAL")
        return ""
    
#   Get MedDRA Term.
def get_meddra_term(phen, user):
    print("NOT FUNCTIONAL.")

#   UNIT TESTS
def meddra_unit_tests(meddra_term, meddra_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    meddra_term_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_term, identifier_type = "MedDRA Term", source = "MedDRA")
    print("Getting MedDRA IDs from MedDRA term (%s):" % meddra_term)
    for iden in get_meddra_id(meddra_term_phen, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()