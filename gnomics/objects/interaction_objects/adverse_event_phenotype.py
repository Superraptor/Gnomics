#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

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
#   Map adverse events to phenotypes.
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
import gnomics.objects.phenotype

#   Other imports.
import json
import requests
import time
import timeit

#   MAIN
def main():
    adverse_event_phenotype_unit_tests("Seizure", "", "")

#   Get phenotypes.
def get_phenotypes(adverse_event, user=None):
    phen_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["meddra term", "mdr label", "mdr name", "mdr term", "meddra label", "meddra name"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            if user.ncbo_api_key is not None:
    
                # Map MedDRA term to MedDRA ID.
                meddra_id_array = gnomics.objects.adverse_event.AdverseEvent.meddra_id(adverse_event, user)

                hpo_id_array = []
                for iden in meddra_id_array:

                    base = "http://data.bioontology.org/ontologies/"
                    ext = "MEDDRA/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F" + str(iden) + "/mappings/?apikey=" + user.ncbo_api_key

                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        continue
                    else:

                        decoded = json.loads(r.text)
                        for result in decoded:
                            for subresult in result["classes"]:
                                if "http://purl.obolibrary.org/obo/HP_" in subresult["@id"]:
                                    hpo_id = subresult["@id"].split("/obo/")[1]
                                    if hpo_id not in hpo_id_array:
                                        hpo_id_array.append(hpo_id)
                                        temp_phen = gnomics.objects.phenotype.Phenotype(identifier = hpo_id, identifier_type = "HPO ID", source = "NCBO BioPortal", taxon = "Homo sapiens")
                                        phen_array.append(temp_phen)

                if not hpo_id_array:
                    mesh_uid_array = []
                    mesh_uids = gnomics.objects.adverse_event.AdverseEvent.mesh_uid(adverse_event, user)
                    mesh_uid_array.extend(mesh_uids)

                    for iden in mesh_uid_array:
                        umls_tgt = User.umls_tgt(user)
                        page_num = 0
                        base = "https://uts-ws.nlm.nih.gov/rest"
                        ext = "/crosswalk/current/source/MSH/" + iden + "?targetSource=HPO"

                        try:
                            tick = User.umls_st(umls_tgt)
                            page_num += 1
                            query = {"ticket": tick, "pageNumber": page_num}
                            r = requests.get(base+ext, params=query)

                            r.encoding = 'utf-8'
                            if not r.ok:
                                print("No mapping from MeSH to HPO found.")
                            else:
                                items = json.loads(r.text)
                                json_data = items["result"]
                                for er in json_data:
                                    if er["ui"] not in hpo_id_array and er["ui"] != "NONE":
                                        hpo_id = er["ui"]
                                        hpo_id_array.append(hpo_id)
                                        temp_phen = gnomics.objects.phenotype.Phenotype(identifier = hpo_id, identifier_type = "HPO ID", source = "UMLS", taxon = "Homo sapiens")
                                        phen_array.append(temp_phen)
                                if not json_data:
                                    continue
                        except:
                            continue
            else:
                print("A valid NCBO API key is necessary to access the NCBO Bioontology API. Please provide a valid user object with such a key.")
        else:
            print("A valid user object with an NCBO API key is necessary to access the NCBO Bioontology API. Please provide such an object.")

    return phen_array

#   UNIT TESTS
def adverse_event_phenotype_unit_tests(meddra_term, umls_api_key, ncbo_api_key):
    user = User(umls_api_key = umls_api_key, ncbo_api_key = ncbo_api_key)
    
    print("\nGetting HPO IDs from MedDRA Term (%s):" % meddra_term)
    meddra_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", source = "UMLS", language = "en")
    
    start = timeit.timeit()
    phenotypes = get_phenotypes(meddra_ae, user = user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for phen in phenotypes:
        for iden in phen.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()