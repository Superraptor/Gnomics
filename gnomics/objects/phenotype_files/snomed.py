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
#   Get SNOMED-CT IDs.
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

#   MAIN
def main():
    snomed_unit_tests("HP:0001947", "c8ec0cca-e10f-485b-bf82-ea0e07000f4f")

#   Get SNOMED-CT IDs.
def get_snomed_ct_id(phen, user = None):
    if user is not None:
        umls_tgt = User.umls_tgt(user)
    phen_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "hpo" or ident["identifier_type"].lower() == "hp" or ident["identifier_type"].lower() == "human phenotype ontology" or ident["identifier_type"].lower() == "human phenotype ontology id":
            phen_array.append(ident["identifier"])
    for ident in phen.identifiers:
        if (ident["identifier_type"].lower() == "hpo" or ident["identifier_type"].lower() == "hp" or ident["identifier_type"].lower() == "human phenotype ontology" or ident["identifier_type"].lower() == "human phenotype ontology id" or ident["identifier_type"].lower() == "hpo id") and user is not None:
            stringy = ident["identifier"]
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/crosswalk/current/source/HPO/" + ident["identifier"] + "?targetSource=SNOMEDCT_US"
            while True:
                tick = User.umls_st(umls_tgt)
                page_num += 1
                query = {"ticket": tick, "pageNumber": page_num}
                r = requests.get(base+ext, params=query)
                r.encoding = 'utf-8'
                items = json.loads(r.text)
                json_data = items["result"]
                for er in json_data:
                    if er["ui"] not in phen_array and er["ui"] != "NONE":
                        snomedct = er["ui"]
                        phen_array.append(snomedct)
                if not json_data:
                    break
    return phen_array

#   UNIT TESTS
def snomed_unit_tests(hpo_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    hpo_phen = gnomics.objects.compound.Compound(identifier = str(hpo_id), identifier_type = "HPO ID", source = "Human Phenotype Ontology")
    print("Getting SNOMED-CT IDs from HPO ID (%s):" % hpo_id)
    for sno in get_snomed_ct_id(hpo_phen, user = user):
        print("- " + str(sno))

#   MAIN
if __name__ == "__main__": main()