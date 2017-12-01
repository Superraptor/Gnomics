#
#
#
#
#

#
#   Convert to and from MedDRA.
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
import gnomics.objects.adverse_event

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    meddra_unit_tests("Temporomandibular joint syndrome", "10051097", "")

#   Get MedDRA ID.
def get_meddra_id(adverse_event, user):
    id_array = []
    for ident in adverse_event.identifiers:
        if ident["identifier_type"].lower() == "meddra id" or ident["identifier_type"].lower() == "meddra identifier":
            id_array.append(ident["identifier"])
    if id_array:
        return id_array
    for ident in adverse_event.identifiers:
        if ident["identifier_type"].lower() == "meddra term":
            umls_tgt = User.umls_tgt(user)
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/search/current?sabs=MDR&searchType=exact&returnIdType=code"
            while True:
                try:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"string": ident["identifier"], "ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    if not r.ok:
                        #print("No MedDRA ID found.")
                        break
                    else:
                        items = json.loads(r.text)
                        json_data = items["result"]
                        for rep in json_data["results"]:
                            if rep["ui"] not in id_array and rep["ui"] != "NONE":
                                id_array.append(rep["ui"])
                                gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = rep["ui"], identifier_type = "MedDRA ID", source = "UMLS")
                        if json_data["results"][0]["ui"] == "NONE":
                            break
                except:
                    if not id_array:
                        base = "http://data.bioontology.org/search"
                        ext = "?q=" + str(ident["identifier"]) + "&ontologies=MEDDRA&require_exact_match=true&roots_only=true/?apikey=" + user.ncbo_api_key
                        r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                        if not r.ok:
                            continue
                        else:
                            decoded = json.loads(r.text)
                            for result in decoded["collection"]:
                                if "http://purl.bioontology.org/ontology/MEDDRA" in subresult["@id"]:
                                    meddra_id = subresult["@id"].split("/MEDDRA/")[1]
                                    if meddra_id not in id_array:
                                        id_array.append(meddra_id)
                                        gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = meddra_id, identifier_type = "MedDRA ID", source = "NCBO BioPortal")
                    break
    return id_array

#   Get MedDRA Term.
def get_meddra_term(adverse_event):
    id_array = []
    for ident in adverse_event.identifiers:
        if ident["identifier_type"].lower() == "meddra term":
            id_array.append(ident["identifier"])
    return id_array

#   UNIT TESTS
def meddra_unit_tests(meddra_term, meddra_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    meddra_term_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "UMLS")
    print("Getting MedDRA IDs from MedDRA term (%s):" % meddra_term)
    for iden in get_meddra_id(meddra_term_ae, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()