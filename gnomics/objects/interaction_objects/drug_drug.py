#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get drugs from a drug.
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
import gnomics.objects.drug

#   Other imports.
import json
import requests

#   MAIN
def main():
    drug_drug_unit_tests("88014")
    
# Get drug-drug interactions.
#
# source: DrugBank, ONCHigh
def get_drug_drug_interactions(drug, source = "DrugBank"):
    drug_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique id" or ident["identifier_type"].lower() == "rxnorm concept unique identifier":
            if source == "DrugBank":
                server = "https://rxnav.nlm.nih.gov/REST/interaction"
                ext = "/interaction.json?rxcui=" + ident["identifier"] + "&sources=" + source
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    print("URL not found.")
                else:
                    decoded = json.loads(r.text)
                    for interaction in decoded["interactionTypeGroup"][0]["interactionType"][0]["interactionPair"]:
                        temp_drug = gnomics.objects.drug.Drug()
                        for interact_concept in interaction["interactionConcept"]:
                            if interact_concept["minConceptItem"]["rxcui"] != ident["identifier"]:
                                temp_drug = gnomics.objects.drug.Drug(identifier = interact_concept["minConceptItem"]["rxcui"], identifier_type = "RxCUI", name = interact_concept["minConceptItem"]["name"], source = "RxNorm")
                                gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = interact_concept["sourceConceptItem"]["id"], identifier_type = "DrugBank ID", name = interact_concept["sourceConceptItem"]["name"], source = "DrugBank")
                        interaction_object = {
                            "object_type": "drug-drug interaction",
                            "description": interaction["description"],
                            "severity": interaction["severity"],
                            "object": temp_drug
                        }
                        drug.related_objects.append({
                            "object_type": "drug-drug interaction",
                            "description": interaction["description"],
                            "severity": interaction["severity"],
                            "object": temp_drug
                        })
                        drug_array.append(interaction_object)
            elif source == "ONCHigh":
                server = "https://rxnav.nlm.nih.gov/REST/interaction"
                ext = "/interaction.json?rxcui=" + ident["identifier"] + "&sources=" + source
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    print("URL not found.")
                else:
                    decoded = json.loads(r.text)
                    for interaction in decoded["interactionTypeGroup"][0]["interactionType"][0]["interactionPair"]:
                        temp_drug = gnomics.objects.drug.Drug()
                        for interact_concept in interaction["interactionConcept"]:
                            if interact_concept["minConceptItem"]["rxcui"] != ident["identifier"]:
                                temp_drug = gnomics.objects.drug.Drug(identifier = interact_concept["minConceptItem"]["rxcui"], identifier_type = "RxCUI", name = interact_concept["minConceptItem"]["name"], source = "RxNorm")
                        interaction_object = {
                            "object_type": "drug-drug interaction",
                            "description": interaction["description"],
                            "severity": interaction["severity"],
                            "object": temp_drug
                        }
                        drug.related_objects.append({
                            "object_type": "drug-drug interaction",
                            "description": interaction["description"],
                            "severity": interaction["severity"],
                            "object": temp_drug
                        })
                        drug_array.append(interaction_object)
    return drug_array

#   UNIT TESTS
def drug_drug_unit_tests(rxcui):
    rxcui_drug = gnomics.objects.drug.Drug(identifier = str(rxcui), identifier_type = "RxCUI", source = "RxNorm")
    print("Getting drug-drug interactions (DrugBank) from RxCUI (%s):" % rxcui)
    for drug_obj in get_drug_drug_interactions(rxcui_drug, source = "DrugBank"):
        print("- Description: %s" % drug_obj["description"])
        print("  Severity: %s" % drug_obj["severity"])
        for iden in drug_obj["object"].identifiers:
            print("  Identifier: %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    print("\nGetting drug-drug interactions (ONCHigh) from RxCUI (%s):" % rxcui)
    for drug_obj in get_drug_drug_interactions(rxcui_drug, source = "ONCHigh"):
        print("- Description: %s" % drug_obj["description"])
        print("  Severity: %s" % drug_obj["severity"])
        for iden in drug_obj["object"].identifiers:
            print("  Identifier: %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    
#   MAIN
if __name__ == "__main__": main()