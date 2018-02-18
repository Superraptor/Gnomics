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
#   Search for cell lines.
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
import gnomics.objects.cell_line

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("breast")

# Return search.
def search(query, source = "ebi"):
    if source in ["ebi", "all"]:
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=clo"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
        
        # See here:
        # https://www.ebi.ac.uk/ols/ontologies
        clo_list = []
        clo_id_array = []
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
            
                if "CLO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in clo_id_array:
                        clo_temp = gnomics.objects.cell_line.CellLine(identifier = new_id, identifier_type = "CLO ID", source = "Ontology Lookup Service", name = doc["label"])
                        clo_list.append(clo_temp)
                        clo_id_array.append(new_id)
                
        return clo_list
    
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