#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
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
import gnomics.objects.compound
import gnomics.objects.phenotype

#   Other imports.
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    snomed_unit_tests("HP:0001947", "")

#   Get SNOMED-CT IDs.
def get_snomed_ct_id(phen, user = None):
    if user is not None:
        umls_tgt = User.umls_tgt(user)
    
    phen_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["sct id", "sct identifier", "sctid", "snomed ct", "snomed ct concept id", "snomed id", "snomed identifier", "snomed-ct", "snomed-ct concept id", "snomed-ct id", "snomed-ct identifier"]:
            phen_array.append(ident["identifier"])
            
    if phen_array:
        return phen_array
    
    ids_completed = []
    for ident in phen.identifiers:
        if (ident["identifier_type"].lower() in ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology"]) and user is not None:

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
                    
        elif (ident["identifier_type"].lower() in ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology"]) and user is None:
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
                        if "SNOMEDCT_US:" in xref:
                            snomed_id = xref.split("SNOMEDCT_US:")[1]
                            phen_array.append(snomed_id)
                            gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier = snomed_id, identifier_type = "SNOMED-CT ID", source = "OLS")

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