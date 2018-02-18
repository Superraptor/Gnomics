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
#   Map adverse events (AEs) to drugs.
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
import gnomics.objects.drug

#   Other imports.
import json
import requests
import time
import timeit

#   MAIN
def main():
    # Temporomandibular joint syndrome
    adverse_event_phenotype_unit_tests("Seizure", "", "", "")

#   Get drugs from AE.
#
#   Parameters:
#   - counts: if true, return AE counts for the
#             given drug.
def get_drugs(adverse_event, user=None, counts=False):
    drug_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["meddra term", "mdr label", "mdr name", "mdr term", "meddra label", "meddra name"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            if user.fda_api_key is not None: 

                base = "https://api.fda.gov/drug/"
                ext = "event.json?api_key=" + str(user.fda_api_key) + "&search=patient.reaction.reactionmeddrapt:%22" + str(iden["identifier"].lower().strip()) + "%22&count=rxcui"

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("An error occurred while trying to access the OpenFDA API.")
                else:

                    for result in r.json()["results"]:
                        rxcui = result["term"]

                        base2 = "https://rxnav.nlm.nih.gov/REST/rxcui/"
                        ext2 = str(rxcui) + "/properties.json"

                        r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})

                        if not r.ok:
                            print("An error occurred while trying to access the OpenFDA API.")
                            
                        else:

                            temp_drug = gnomics.objects.drug.Drug(identifier=rxcui, identifier_type="RxCUI", language=None, source="OpenFDA", name=r.json()["properties"]["name"])

                            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier=r.json()["properties"]["umlscui"], identifier_type="UMLS CUI", language=None, source="RxNorm")

                            drug_array.append(temp_drug)
                            
            else:
                print("A valid FDA API key is necessary to access OpenFDA. Please provide a valid user object with such a key.")
        else:
            print("A user object with a valid FDA API key is necessary to access OpenFDA. Please provide one.")

    return drug_array

#   UNIT TESTS
def adverse_event_phenotype_unit_tests(meddra_term, umls_api_key, ncbo_api_key, fda_api_key):
    user = User(umls_api_key = umls_api_key, ncbo_api_key = ncbo_api_key, fda_api_key = fda_api_key)
    
    print("\nGetting RxCUIs from MedDRA Term (%s):" % meddra_term)
    meddra_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", source = "UMLS", language = "en")
    
    start = timeit.timeit()
    drugs = get_drugs(meddra_ae, user = user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for drug in drugs:
        for iden in drug.identifiers:
            print("- %s (%s) [%s]" % (str(iden["identifier"]), iden["identifier_type"], str(iden["name"])))

#   MAIN
if __name__ == "__main__": main()