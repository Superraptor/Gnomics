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
    hpo_unit_tests("D012006", "10051097", "Seizure", "HP:0002573", "")

#   Get HPO ID.
def get_hpo_id(phen, user):
    hpo_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "hpo" or ident["identifier_type"].lower() == "hpo id" or ident["identifier_type"].lower() == "hpo identifier":
            if ident["identifier"] not in hpo_id_array:
                hpo_id_array.append(ident["identifier"])
    mesh_is_here = False
    mesh_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "mesh id" or ident["identifier_type"].lower() == "mesh uid" or ident["identifier_type"].lower() == "mesh identifier":
            mesh_is_here = True
            if ident["identifier"] not in mesh_array:
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/MSH/" + ident["identifier"] + "?targetSource=HPO"
                umls_tgt = User.umls_tgt(user)
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    try:
                        items = json.loads(r.text)
                        json_data = items["result"]
                        print(json_data)
                        for er in json_data:
                            if er["ui"] not in hpo_id_array and er["ui"] != "NONE":
                                hpo_id = er["ui"]
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = hpo_id, identifier_type = "HPO ID", source = "UMLS", taxon = "Homo sapiens")
                                hpo_id_array.append(hpo_id)
                        if not json_data:
                            break
                    except:
                        break
                    break
    if hpo_id_array:        
        return hpo_id_array
    if mesh_is_here:
        return []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "meddra id" or ident["identifier_type"].lower() == "meddra identifier":
            mesh_uid = gnomics.objects.phenotype.Phenotype.mesh_uid(phen, user)
            if mesh_uid:
                return get_hpo_id(phen, user)
            else:
                return []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "meddra term":
            gnomics.objects.phenotype.Phenotype.meddra_id(phen, user)
            return get_hpo_id(phen, user)
        
#   Get HPO Term
def get_hpo_term(phen, user):
    hpo_term_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "hpo term":
            if ident["identifier"] not in hpo_id_array:
                hpo_id_array.append(ident["identifier"])
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() == "hpo id" or ident["identifier_type"].lower() == "hpo" or ident["identifier_type"].lower() == "hpo identifier":
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/content/current/source/HPO/" + ident["identifier"]
            umls_tgt = User.umls_tgt(user)
            while True:
                tick = User.umls_st(umls_tgt)
                page_num += 1
                query = {"ticket": tick, "pageNumber": page_num}
                r = requests.get(base+ext, params=query)
                r.encoding = 'utf-8'

                try:
                    items = json.loads(r.text)
                    json_data = items["result"]
                    print(json_data)
                    if "name" in json_data:
                        if json_data["name"] not in hpo_term_array:
                            hpo_term = json_data["name"]
                            gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = hpo_term, identifier_type = "HPO Term", source = "UMLS", taxon = "Homo sapiens")
                            hpo_id_term.append(hpo_term)
                    else:
                        break
                except:
                    break
                break
        return hpo_term_array
        
#   UNIT TESTS
def hpo_unit_tests(mesh_uid, meddra_id, meddra_term, hpo_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    hpo_phen = gnomics.objects.phenotype.Phenotype(identifier = hpo_id, identifier_type = "HPO ID", source = "UMLS")
    print("\nGetting HPO Terms from HPO ID (%s):" % hpo_id)
    for iden in get_hpo_term(hpo_phen, user):
        print("- " + str(iden))
    mesh_phen = gnomics.objects.phenotype.Phenotype(identifier = mesh_uid, identifier_type = "MeSH UID", source = "MeSH")
    print("Getting HPO IDs from MeSH UID (%s):" % mesh_uid)
    for iden in get_hpo_id(mesh_phen, user):
        print("- " + str(iden))
    meddra_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_id, identifier_type = "MedDRA ID", source = "MedDRA")
    print("\nGetting HPO IDs from MedDRA ID (%s):" % meddra_id)
    for iden in get_hpo_id(meddra_phen, user):
        print("- " + str(iden))
    meddra_term_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_term, identifier_type = "MedDRA Term", source = "MedDRA")
    print("\nGetting MedDRA IDs from MedDRA term (%s):" % meddra_term)
    for iden in get_hpo_id(meddra_term_phen, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()