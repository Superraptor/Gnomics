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
#   Search for tissues.
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("lung, upper lobe", "", "")

# Return search.
def search(query, user=None, source="ebi", search_type="exact", return_id_type="sourceUi"):
    tiss_list = []
    tiss_id_array = []
    
    if source in ["ebi", "all"]:
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=bto,uberon"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()

            # See here:
            # https://www.ebi.ac.uk/ols/ontologies
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "BTO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in tiss_id_array:
                            tiss_temp = gnomics.objects.tissue.Tissue(identifier = new_id, identifier_type = "BTO ID", source = "Ontology Lookup Service", name = doc["label"])
                            tiss_list.append(tiss_temp)
                            tiss_id_array.append(new_id)
                    elif "UBERON" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in tiss_id_array:
                            tiss_temp = gnomics.objects.tissue.Tissue(identifier = new_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service", name = doc["label"])
                            tiss_list.append(tiss_temp)
                            tiss_id_array.append(new_id)
                            
    if source.lower() in ["ncbo", "all"] and user.ncbo_api_key is not None:
        base = "http://data.bioontology.org/search"
        ext = "?q=" + str(query) + "&ontologies=BTO,UBERON&roots_only=true/?apikey=" + user.ncbo_api_key
        r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            decoded = json.loads(r.text)
            for result in decoded["collection"]:
                
                # BRENDA Tissue and Enzyme Source Ontology
                if "BTO" in result["@id"]:
                    bto_id = result["@id"].split("/obo/")[1]
                    if bto_id not in tiss_id_array:
                        tiss_id_array.append(bto_id)
                        tiss_temp = gnomics.objects.tissue.Tissue(identifier=bto_id, identifier_type="BTO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        tiss_list.append(tiss_temp)
                        
                # Uber Anatomy Ontology
                elif "UBERON" in result["@id"]:
                    uberon_id = result["@id"].split("/obo/")[1]
                    if uberon_id not in tiss_id_array:
                        tiss_id_array.append(uberon_id)
                        tiss_temp = gnomics.objects.tissue.Tissue(identifier=uberon_id, identifier_type="UBERON ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        tiss_list.append(tiss_temp)
               
    return tiss_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query, umls_api_key, ncbo_api_key):
    print("Beginning basic search for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="umls")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
        
    print("\nSearch returned %s result(s) with the following identifiers (EBI):" % str(len(basic_search_results)))
    for tiss in basic_search_results:
        for iden in tiss.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()