#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
#

#
#   Search for diseases.
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
import gnomics.objects.disease
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("breast cancer")
    
# Return search.
#
# Most of the parameters originate from OMIM search, as
# can be seen here:
# https://www.omim.org/help/api
#
def search(query, search_type=None, user=None, source="omim", filter_type=None, fields_type=None, sort_type=None, operator_type=None, start=0, limit=10, retrieve=None, format_param="jsonp"):
    
    disease_list = []
    disease_id_array = []
    
    if source.lower() in ["omim", "all"] and user is not None and search_type is None:
        server = "https://api.omim.org"
        ext = "/api/entry/search?search=" + str(query) + "&format=" + format_param
        api_key_str = "&apiKey=" + user.omim_api_key

        r = requests.get(server+ext+api_key_str, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rfind(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()

            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            entries = decoded["omim"]["searchResponse"]["entryList"]
            for entry in entries:
                disease_temp = gnomics.objects.disease.Disease(identifier = entry["entry"]["mimNumber"], identifier_type = "MIM number",
                source = "OMIM")
                disease_list.append(disease_temp)
    
    if (source.lower() in ["ebi", "all"] and search_type is None) or (source.lower() in ["omim", "all"] and search_type is None and user is None):
        
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            disease_list = []
            disease_id_array = []
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "DOID" in doc["obo_id"]:
                        pro_doid = doc["obo_id"].split(":")
                        new_doid = pro_doid[1]
                        if new_doid not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_doid, identifier_type = "DOID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_doid)
                    elif "IDO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "IDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "MFOMD" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MFOMD ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "MONDO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MONDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "Orphanet" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "ORDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
            
            return disease_list
    
    if (source.lower() in ["ebi", "all"] and search_type == "exact") or (source.lower() in ["omim", "all"] and search_type == "exact" and user is None):
        
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()               
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "DOID" in doc["obo_id"]:
                        pro_doid = doc["obo_id"].split(":")
                        new_doid = pro_doid[1]
                        if new_doid not in disease_id_array and str(query).lower() == doc["label"].lower():
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_doid, identifier_type = "DOID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_doid)
                    elif "IDO" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "IDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "MFOMD" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MFOMD ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "MONDO" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MONDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                    elif "Orphanet" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in disease_id_array:
                            disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "ORDO ID", source = "Ontology Lookup Service", name = doc["label"])
                            disease_list.append(disease_temp)
                            disease_id_array.append(new_id)
                                
            if not disease_list:
                for doc in decoded["response"]["docs"]:
                    if "obo_id" in doc:
                        if "DOID" in doc["obo_id"]:   
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                decoded = r.json()
                                
                                pro_doid = doc["obo_id"].split(":")
                                new_doid = pro_doid[1]
                                if decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in decoded["synonyms"]] and new_doid not in disease_id_array:

                                        disease_temp = gnomics.objects.disease.Disease(identifier = new_doid, identifier_type = "DOID", source = "Ontology Lookup Service", name = doc["label"])
                                        disease_list.append(disease_temp)
                                        disease_id_array.append(new_doid)
                                
                        elif "IDO" in doc["obo_id"]:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/ido/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                decoded = r.json()
                            
                                new_id = doc["obo_id"]
                                if decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in decoded["synonyms"]] and new_id not in disease_id_array:
                                        disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "IDO ID", source = "Ontology Lookup Service", name = doc["label"])
                                        disease_list.append(disease_temp)
                                        disease_id_array.append(new_id)
                                    
                        elif "MFOMD" in doc["obo_id"]:
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                decoded = r.json()
                            
                                new_id = doc["obo_id"]
                                if decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in decoded["synonyms"]] and new_id not in disease_id_array:
                                        disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MFOMD ID", source = "Ontology Lookup Service", name = doc["label"])
                                        disease_list.append(disease_temp)
                                        disease_id_array.append(new_id)
                                
                        elif "MONDO" in doc["obo_id"]:
                            
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/mondo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                decoded = r.json()
                                
                                new_id = doc["obo_id"]
                                if decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in decoded["synonyms"]] and new_id not in disease_id_array:
                                        disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "MONDO ID", source = "Ontology Lookup Service", name = doc["label"])
                                        disease_list.append(disease_temp)
                                        disease_id_array.append(new_id)
                            
                        elif "Orphanet" in doc["obo_id"]:
                            
                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/ordo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                decoded = r.json()
                                
                                new_id = doc["obo_id"]
                                if decoded["synonyms"]:
                                    if query.lower() in [x.lower() for x in decoded["synonyms"]] and new_id not in disease_id_array:
                                        disease_temp = gnomics.objects.disease.Disease(identifier = new_id, identifier_type = "ORDO ID", source = "Ontology Lookup Service", name = doc["label"])
                                        disease_list.append(disease_temp)
                                        disease_id_array.append(new_id)

    return disease_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
        
    print("\nSearch returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for dis in basic_search_results:
        for iden in dis.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()