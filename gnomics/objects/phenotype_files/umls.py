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
#   Get UMLS CUIs.
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
import pubchempy as pubchem
import requests

#   MAIN
def main():
    umls_unit_tests("HP:0001947")

#   Get SNOMED-CT IDs.
def get_umls_cui(phen, user=None):
    phen_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["umls concept uid", "umls concept unique id", "umls concept unique identifier", "umls cui", "umls id", "umls identifier"]:
            phen_array.append(ident["identifier"])
            
    if phen_array:
        return phen_array
            
    ids_completed = []
    for ident in phen.identifiers:
        if (ident["identifier_type"].lower() in ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology"]) and user is None:
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
                        if "UMLS:" in xref:
                            umls_cui = xref.split("UMLS:")[1]
                            phen_array.append(umls_cui)
                            gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = umls_cui, identifier_type = "UMLS CUI", source = "OLS")
            
    return phen_array

#   UNIT TESTS
def umls_unit_tests(hpo_id):
    hpo_phen = gnomics.objects.compound.Compound(identifier = str(hpo_id), identifier_type = "HPO ID", source = "Human Phenotype Ontology")
    print("Getting UMLS CUIs from HPO ID (%s):" % hpo_id)
    for umls in get_umls_cui(hpo_phen):
        print("- " + str(umls))

#   MAIN
if __name__ == "__main__": main()