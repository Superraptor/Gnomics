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
    mesh_unit_tests("10051097", "")

#   Get MeSH UID.
def get_mesh_uid(phen, user=None):
    mesh_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["mesh", "mesh uid", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]:
            if ident["identifier"] not in mesh_array:
                mesh_array.append(ident["identifier"])
                
    if mesh_array:
        return mesh_array

    meddra_array = []
    ids_completed = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["mdr", "mdr code", "mdr id", "mdr identifier", "meddra", "meddra code", "meddra id", "meddra identifier"]:
            if user is not None:
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
                    for xref in decoded["annotation"]["database_cross_reference"]:
                        if "MSH:" in xref:
                            mesh_uid = xref.split("MSH:")[1]
                            mesh_array.append(mesh_uid)
                            gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = mesh_uid, identifier_type = "MeSH UID", source = "OLS")

    return mesh_array

#   UNIT TESTS
def mesh_unit_tests(meddra_id, umls_api_key):
    user = User(umls_api_key = umls_ap_key)
    
    meddra_phen = gnomics.objects.phenotype.Phenotype(identifier = meddra_id, identifier_type = "MedDRA ID", source = "MedDRA")
    print("Getting MeSH UIDs from MedDRA ID (%s):" % meddra_id)
    for iden in get_mesh_uid(meddra_phen, user):
        print("- " + str(iden))

#   MAIN
if __name__ == "__main__": main()