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
#   Search for phenotype.
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
import gnomics.objects.molecular_function

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("CDK4 Amplification")
    
# Return search.
def search(query, source="ebi", search_type=None):
    if source == "ebi" and search_type == None:
        print("NOT FUNCTIONAL.")
        
    elif source == "ebi" and search_type == "exact":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=go,ncit"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            molec_list = []
            molec_id_array = []
            
            for doc in decoded["response"]["docs"]:
                if "short_form" in doc:
                    if "NCIT" in doc["short_form"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["short_form"]
                        if new_id not in molec_id_array:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/ncit/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]
                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                new_decoded = r.json()
                                new_id = doc["short_form"]
                                if "Cell or Molecular Dysfunction" in new_decoded["annotation"]["Semantic_Type"]:
                                    molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "NCIT ID", source = "Ontology Lookup Service", name = doc["label"])
                                    molec_list.append(molec_temp)
                                    molec_id_array.append(new_id)
                                    
                if "obo_id" in doc:
                    if "GO" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in molec_id_array:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/go/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                new_decoded = r.json()
                                new_id = doc["obo_id"]
                                if "molecular_function" in new_decoded["annotation"]["has_obo_namespace"]:
                                    molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "GO Accession", source = "Ontology Lookup Service", name = doc["label"])
                                    molec_list.append(molec_temp)
                                    molec_id_array.append(new_id)
            
            if not molec_list or True:
                for doc in decoded["response"]["docs"]:
                    if "short_form" in doc:
                        if "NCIT" in doc["short_form"]:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/ncit/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]
                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                new_decoded = r.json()
                                new_id = doc["short_form"]
                                if new_decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in new_decoded["synonyms"]] and new_id not in molec_id_array and "Cell or Molecular Dysfunction" in new_decoded["annotation"]["Semantic_Type"]:
                                        molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "NCIT ID", source = "Ontology Lookup Service", name = doc["label"])
                                        molec_list.append(molec_temp)
                                        molec_id_array.append(new_id)
                            
                    if "obo_id" in doc:
                        if "GO" in doc["obo_id"]:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/go/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]
                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                new_decoded = r.json()
                                new_id = doc["obo_id"]
                                if new_decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in new_decoded["synonyms"]] and new_id not in molec_id_array and "molecular_function" in new_decoded["annotation"]["has_obo_namespace"]:
                                        molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "GO Accession", source = "Ontology Lookup Service", name = doc["label"])
                                        molec_list.append(molec_temp)
                                        molec_id_array.append(new_id)
            
            if not molec_list:
                for doc in decoded["response"]["docs"]:
                    if "short_form" in doc:
                        if "NCIT" in doc["short_form"]:
                            match_count = 0
                            for sub_string in str(query).lower().split(" "):
                                if sub_string in doc["label"].lower():
                                    match_count += 1
                                    
                            if float(match_count) / float(len(str(query).lower().split(" "))) >= 0.60:
                                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                                ext = "/ncit/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]
                                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                                if not r.ok:
                                    print("Something went wrong.")
                                else:
                                    new_decoded = r.json()
                                    new_id = doc["short_form"]
                                    if new_id not in molec_id_array and "Cell or Molecular Dysfunction" in new_decoded["annotation"]["Semantic_Type"]:
                                        molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "NCIT ID", source = "Ontology Lookup Service", name = doc["label"])
                                        molec_list.append(molec_temp)
                                        molec_id_array.append(new_id)
                                            
                    if "obo_id" in doc:
                        if "GO" in doc["obo_id"]:
                            match_count = 0
                            for sub_string in str(query).lower().split(" "):
                                if sub_string in doc["label"].lower():
                                    match_count += 1
                                    
                            if float(match_count) / float(len(str(query).lower().split(" "))) >= 0.60:
                                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                                ext = "/go/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]
                                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                                if not r.ok:
                                    print("Something went wrong.")
                                else:
                                    new_decoded = r.json()

                                    new_id = doc["obo_id"]
                                    if new_decoded["synonyms"]:
                                        if query.lower() in [x.lower() for x in new_decoded["synonyms"]] and new_id not in molec_id_array and "molecular_function" in new_decoded["annotation"]["has_obo_namespace"]:
                                            molec_temp = gnomics.objects.molecular_function.MolecularFunction(identifier = new_id, identifier_type = "GO Accession", source = "Ontology Lookup Service", name = doc["label"])
                                            molec_list.append(molec_temp)
                                            molec_id_array.append(new_id)
                        
        return molec_list
    
#   UNIT TESTS   
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query, search_type = "exact")
    print("\nSearch returned %s result(s) with the following molecular function IDs:" % str(len(basic_search_results)))
    for molec in basic_search_results:
        for iden in molec.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()