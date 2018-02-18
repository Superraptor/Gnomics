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
#   Search for drugs.
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
import gnomics.objects.drug

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("advil")
    
# Return search.
#
# https://rxnav.nlm.nih.gov/RxNormAPIs.html#
def search(query, search_type="exact", source="rxnorm"):
    if source == "rxnorm" and search_type == "exact":
        server = "https://rxnav.nlm.nih.gov/REST"
        ext = "/rxcui.json?name=" + str(query)
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            print("Something went wrong.")
        else:
            str_r = r.text
            decoded = json.loads(str_r)
            result_array = []
            if "idGroup" in decoded:
                if "rxnormId" in decoded["idGroup"]:
                    for iden in decoded["idGroup"]["rxnormId"]:
                        server2 = "https://rxnav.nlm.nih.gov/REST"
                        ext2 = "/rxcui/" + iden + "/allProperties.json?prop=all"
                        r = requests.get(server2+ext2, headers={"Content-Type": "application/json"})
                        if not r.ok:
                            r.raise_for_status()
                            sys.exit()

                        str_r2 = r.text
                        decoded2 = json.loads(str_r2)
                        rxnorm_name = None
                        for x in decoded2["propConceptGroup"]["propConcept"]:
                            if x["propName"] == "RxNorm Name":
                                rxnorm_name = x["propValue"]

                        temp_drug = gnomics.objects.drug.Drug(identifier = iden, identifier_type = "RxCUI", language = None, source = "RxNorm", name = rxnorm_name)

                        result_array.append(temp_drug)

        return result_array
    
    elif source == "rxnorm" and search_type == "approximate":
        server = "https://rxnav.nlm.nih.gov/REST"
        ext = "/approximateTerm.json?term=" + str(query)
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()

        str_r = r.text
        decoded = json.loads(str_r)
        result_array = []
        for iden in decoded["approximateGroup"]["candidate"]:
            server2 = "https://rxnav.nlm.nih.gov/REST"
            ext2 = "/rxcui/" + iden["rxcui"] + "/allProperties.json?prop=all"
            r = requests.get(server2+ext2, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            str_r2 = r.text
            decoded2 = json.loads(str_r2)
            rxnorm_name = None
            for x in decoded2["propConceptGroup"]["propConcept"]:
                if x["propName"] == "RxNorm Name":
                    rxnorm_name = x["propValue"]
            
            temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI", language = None, source = "RxNorm", name = rxnorm_name)
            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["rxaui"], language = None, source = "RxNorm", identifier_type = "RxAUI", name = rxnorm_name)
            
            score = iden["score"]
            rank = iden["rank"]
            
            result_array.append(temp_drug)
        
        return result_array
    
    elif source == "ebi":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
            
        drug_list = []
        drug_id_array = []
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
                if "DRON" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in drug_id_array:
                        drug_temp = gnomics.objects.drug.Drug(identifier = new_id, identifier_type = "DRON ID", source = "Ontology Lookup Service", name = doc["label"])
                        drug_list.append(drug_temp)
                        drug_id_array.append(new_id)
                elif "VO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in drug_id_array:
                        drug_temp = gnomics.objects.drug.Drug(identifier = new_id, identifier_type = "VO ID", source = "Ontology Lookup Service", name = doc["label"])
                        drug_list.append(drug_temp)
                        drug_id_array.append(new_id)
            
        return drug_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic searches for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="ebi")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    print("\nSearch returned %s exact result(s) with the following drug identifiers:" % str(len(basic_search_results)))
    for drug in basic_search_results:
        for iden in drug.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
        
    basic_search_results = search(basic_query)
    print("\nSearch returned %s exact result(s) with the following RxCUIs:" % str(len(basic_search_results)))
    for drug in basic_search_results:
        for iden in drug.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
    advanced_search_results = search(basic_query, search_type="approximate")
    print("\nSearch returned %s approximate result(s) with the following RxCUIs:" % str(len(advanced_search_results)))
    for drug in advanced_search_results:
        for iden in drug.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()