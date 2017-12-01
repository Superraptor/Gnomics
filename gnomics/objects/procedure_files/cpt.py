#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   CPT (Current Procedural Terminology).
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
import gnomics.objects.procedure

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("C0042014", "")
    
# Return CPT ID.
def get_cpt_id(procedure, user):
    for iden in procedure.identifiers:
        if iden["identifier_type"].lower() == "umls cui" or iden["identifier_type"].lower() == "umls":
            proc_array = []
            umls_tgt = User.umls_tgt(user)
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/search/current?string=" + iden["identifier"] + "inputType=sourceUi&searchType=exact&sabs=MTH"
            while True:
                tick = User.umls_st(umls_tgt)
                page_num += 1
                query = {"string": query, "ticket": tick, "pageNumber": page_num}
                r = requests.get(base+ext, params=query)
                r.encoding = 'utf-8'
                print(r.text)
                items = json.loads(r.text)
                json_data = items["result"]
                for rep in json_data["results"]:
                    if rep["ui"] not in proc_array and rep["ui"] != "NONE":
                        proc_array.append(rep["ui"])
                if json_data["results"][0]["ui"] == "NONE":
                    break
            return proc_array
    
#   UNIT TESTS
def basic_search_unit_tests(umls_cui, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    umls_proc = gnomics.objects.procedure.Procedure(identifier=umls_cui, identifier_type="UMLS CUI", language=None, source="UMLS Metathesaurus")
    for proc in get_cpi_id(umls_proc, user):
        print("- %s" % proc)
    
#   MAIN
if __name__ == "__main__": main()