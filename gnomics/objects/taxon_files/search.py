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
#   Search for taxon.
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
import gnomics.objects.gene
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    basic_search_unit_tests("human", eol_api_key = "")
        
#   Search.
#
#   In-depth discussion of various parameters can be found here:
#   http://eol.org/api/docs/search
def search(query, source="eol", page=1, exact=True, filter_by_taxon_concept_id="", filter_by_hierarchy_entry_id="", filter_by_string="", cache_ttl="", user=None):
    result_array = []
    result_id_array = []
    
    if source in ["eol", "all"]:
        
        if user is not None:
            if user.eol_api_key is not None:
    
                base_url = "http://eol.org/api/search/1.0.json?"
                ext_url = "q=" + str(query) + "&" + "page=" + str(page) + "&" + "exact=" + str(exact).lower() + "&" + "filter_by_taxon_concept_id=" + str(filter_by_taxon_concept_id) + "&" + "filter_by_hierarchy_entry_id=" + str(filter_by_hierarchy_entry_id) + "&" + "filter_by_string=" + str(filter_by_string) + "&" + "cache_ttl=" + str(cache_ttl) + "&key=" + str(user.eol_api_key)

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()

                    for result in decoded["results"]:
                        if result["id"] not in result_id_array:
                            result_id_array.append(result["id"])
                            temp_taxon = gnomics.objects.taxon.Taxon(identifier = result["id"], identifier_type = "EOL ID", source = "Encyclopedia of Life", language = None, name = result["content"])
                            result_array.append(temp_taxon)
                            
            else:
                
                base_url = "http://eol.org/api/search/1.0.json?"
                ext_url = "q=" + str(query) + "&" + "page=" + str(page) + "&" + "exact=" + str(exact).lower() + "&" + "filter_by_taxon_concept_id=" + str(filter_by_taxon_concept_id) + "&" + "filter_by_hierarchy_entry_id=" + str(filter_by_hierarchy_entry_id) + "&" + "filter_by_string=" + str(filter_by_string) + "&" + "cache_ttl=" + str(cache_ttl)

                try:
                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        print("Something went wrong.")
                    else:
                        decoded = r.json()

                        for result in decoded["results"]:
                            if result["id"] not in result_id_array:
                                result_id_array.append(result["id"])
                                temp_taxon = gnomics.objects.taxon.Taxon(identifier = result["id"], identifier_type = "EOL ID", source = "Encyclopedia of Life", language = None, name = result["content"])
                                result_array.append(temp_taxon)
                                
                except requests.exceptions.ConnectionError:
                    print("A connection error occurred.")
        else:
            
            base_url = "http://eol.org/api/search/1.0.json?"
            ext_url = "q=" + str(query) + "&" + "page=" + str(page) + "&" + "exact=" + str(exact).lower() + "&" + "filter_by_taxon_concept_id=" + str(filter_by_taxon_concept_id) + "&" + "filter_by_hierarchy_entry_id=" + str(filter_by_hierarchy_entry_id) + "&" + "filter_by_string=" + str(filter_by_string) + "&" + "cache_ttl=" + str(cache_ttl)

            try:
                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()

                    for result in decoded["results"]:
                        if result["id"] not in result_id_array:
                            result_id_array.append(result["id"])
                            temp_taxon = gnomics.objects.taxon.Taxon(identifier = result["id"], identifier_type = "EOL ID", source = "Encyclopedia of Life", language = None, name = result["content"])
                            result_array.append(temp_taxon)
            except requests.exceptions.ConnectionError:
                print("A connection error occurred.")
                
    if source in ["ott", "opentreeoflife"]:
        
        base_url = "https://api.opentreeoflife.org/v3/"
        ext_url = "tnrs/match_names?names=" + "Homo sapiens"
        
        r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"}, params={"names": ["Home sapiens"]})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        exit()
        
    if source.lower() in ["ebi", "all"]:
        
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=ncbitaxon"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
        
        # See here:
        # https://www.ebi.ac.uk/ols/ontologies
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
                if "NCBITaxon" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in result_id_array:
                        tax_temp = gnomics.objects.taxon.Taxon(identifier = new_id, identifier_type = "NCBI TaxID", source = "Ontology Lookup Service", name = doc["label"])
                        result_array.append(tax_temp)
                        result_id_array.append(new_id)
                elif "VTO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in result_id_array:
                        tax_temp = gnomics.objects.taxon.Taxon(identifier = new_id, identifier_type = "VTO ID", source = "Ontology Lookup Service", name = doc["label"])
                        result_array.append(tax_temp)
                        result_id_array.append(new_id)
                        
    if source.lower() in ["ncbo", "all"] and user.ncbo_api_key is not None:
            
        base = "http://data.bioontology.org/search"
        ext = "?q=" + str(query) + "&ontologies=NCBITAXON,FB-SP,VTO,ATO&roots_only=true/?apikey=" + user.ncbo_api_key

        r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            decoded = json.loads(r.text)
            
            for result in decoded["collection"]:
                
                # NCBI Organismal Classification
                if "NCBITAXON" in result["@id"]:
                    ncbi_id = result["@id"].split("/obo/")[1]
                    if ncbi_id not in result_id_array:
                        result_id_array.append(ncbi_id)
                        tax_temp = gnomics.objects.taxon.Taxon(identifier=bto_id, identifier_type="NCBI Taxonomy ID", source="NCBO BioPortal", name=result["prefLabel"])
                        result_list.append(tax_temp)
                        
                # Fly Taxonomy
                elif "FB-SP" in result["@id"]:
                    fbsp_id = result["@id"].split("/obo/")[1]
                    if fbsp_id not in result_id_array:
                        result_id_array.append(fbsp_id)
                        tax_temp = gnomics.objects.taxon.Taxon(identifier=fbsp_id, identifier_type="FB-SP ID", source="NCBO BioPortal", name=result["prefLabel"])
                        result_list.append(tax_temp)
                        
                # Vertebrate Taxonomy Ontology
                elif "VTO" in result["@id"]:
                    vto_id = result["@id"].split("/obo/")[1]
                    if vto_id not in result_id_array:
                        result_id_array.append(vto_id)
                        tax_temp = gnomics.objects.taxon.Taxon(identifier=vto_id, identifier_type="VTO ID", source="NCBO BioPortal", name=result["prefLabel"])
                        result_list.append(tax_temp)
                        
                # Amphibian Taxonomy Ontology
                elif "ATO" in result["@id"]:
                    ato_id = result["@id"].split("/obo/")[1]
                    if ato_id not in result_id_array:
                        result_id_array.append(ato_id)
                        tax_temp = gnomics.objects.taxon.Taxon(identifier=ato_id, identifier_type="ATO ID", source="NCBO BioPortal", name=result["prefLabel"])
                        result_list.append(tax_temp)
                
    return result_array

#   UNIT TESTS
def basic_search_unit_tests(basic_query, eol_api_key = None):
    start = timeit.timeit()
    basic_search_results = search(basic_query)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
      
    print("\nSearch returned %s result(s) with the following EOL IDs:" % str(len(basic_search_results)))
    for tax in basic_search_results:
        for iden in tax.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()