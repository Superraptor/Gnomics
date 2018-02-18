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
#   Search for cellular components.
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
import gnomics.objects.cellular_component

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("nucleus")

#   Return search.
def search(query, source="ebi", search_type=None):
    cell_list = []
    cell_id_array = []
    
    if source.lower() in ["ebi", "all"]:
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=go"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()

            # See here:
            # https://www.ebi.ac.uk/ols/ontologies
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "GO" in doc["obo_id"] and str(query).lower() == doc["label"].lower():
                        new_id = doc["obo_id"]
                        if new_id not in cell_id_array:

                            url = "https://www.ebi.ac.uk/ols/api/ontologies"
                            ext = "/go/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doc["short_form"]

                            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                print("Something went wrong.")
                            else:
                                new_decoded = r.json()
                                new_id = doc["obo_id"]
                                if "cellular_component" in new_decoded["annotation"]["has_obo_namespace"]:
                                    cell_temp = gnomics.objects.cellular_component.CellularComponent(identifier = new_id, identifier_type = "GO Accession", source = "Ontology Lookup Service", name = doc["label"])
                                    cell_list.append(cell_temp)
                                    cell_id_array.append(new_id)
    
    return cell_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
        
    print("\nSearch returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for symp in basic_search_results:
        for iden in symp.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()