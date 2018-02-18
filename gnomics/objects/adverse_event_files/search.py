#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

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
#   Search for adverse events.
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
import gnomics.objects.adverse_event

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("Fatigue", "d6f408cd-ffac-4f0f-a645-75c1d966375e")

# Return search.
def search(query, user = None, source = "ols", search_type = "exact"):
    event_list = []
    event_id_array = []
    
    if source.lower() in ["fda", "all"] and user is not None:
        url = "https://api.fda.gov/drug/event.json"
        ext = "?search=patient.reaction.reactionmeddrapt.exact:%22" + query + "%22&count=patient.reaction.reactionmeddrapt.exact"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
        
        for x in decoded["results"]:
            if (x["term"] not in event_id_array) and (query.lower() == x["term"].lower()):
                temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = x["term"], identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA", name = x["term"])
                event_id_array.append(x["term"])
                event_list.append(temp_ae)
                
    if source.lower() in ["ols", "all"]:
        
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=aero,oae,ovae"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("An error occurred in the EBI OLS API.")
        else:

            decoded = r.json()

            # See here:
            # https://www.ebi.ac.uk/ols/ontologies
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:

                    # Taxon agnostic.
                    if "AERO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in event_id_array:
                            ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = new_id, identifier_type = "AERO ID", source = "Ontology Lookup Service", name = doc["label"])
                            event_list.append(ae_temp)
                            event_id_array.append(new_id)
                    elif "OAE" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in event_id_array:
                            ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = new_id, identifier_type = "OAE ID", source = "Ontology Lookup Service", name = doc["label"])
                            event_list.append(ae_temp)
                            event_id_array.append(new_id)
                    elif "OVAE" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in event_id_array:
                            ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = new_id, identifier_type = "OVAE ID", source = "Ontology Lookup Service", name = doc["label"])
                            event_list.append(ae_temp)
                            event_id_array.append(new_id)
                        
    if source.lower() in ["ncbo", "all"] and user.ncbo_api_key is not None:
            
        base = "http://data.bioontology.org/search"
        ext = "?q=" + str(query) + "&ontologies=AERO,OAE,OCVDAE,ODNAE,OVAE&roots_only=true/?apikey=" + user.ncbo_api_key

        r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            decoded = json.loads(r.text)
            
            for result in decoded["collection"]:
                if "OAE" in result["@id"]:
                    oae_id = result["@id"].split("/obo/")[1]
                    if oae_id not in event_id_array:
                        event_id_array.append(oae_id)
                        ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = oae_id, identifier_type = "OAE ID", source = "NCBO BioPortal", name = result["prefLabel"])
                        event_list.append(ae_temp)

                elif "OVAE" in result["@id"]:
                    ovae_id = result["@id"].split("/obo/")[1]
                    if ovae_id not in event_id_array:
                        event_id_array.append(ovae_id)
                        ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = ovae_id, identifier_type = "OVAE ID", source = "NCBO BioPortal", name = result["prefLabel"])
                        event_list.append(ae_temp)
                        
                elif "AERO" in result["@id"]:
                    aero_id = result["@id"].split("/obo/")[1]
                    if aero_id not in event_id_array:
                        event_id_array.append(aero_id)
                        ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = aero_id, identifier_type = "AERO ID", source = "NCBO BioPortal", name = result["prefLabel"])
                        event_list.append(ae_temp)
                        
                elif "OCVDAE" in result["@id"]:
                    ocvdae_id = result["@id"].split("/obo/")[1]
                    if ocvdae_id not in event_id_array:
                        event_id_array.append(ocvdae_id)
                        ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = ocvdae_id, identifier_type = "OCVDAE ID", source = "NCBO BioPortal", name = result["prefLabel"])
                        event_list.append(ae_temp)
                        
                elif "ODNAE" in result["@id"]:
                    odnae_id = result["@id"].split("/obo/")[1]
                    if odnae_id not in event_id_array:
                        event_id_array.append(odnae_id)
                        ae_temp = gnomics.objects.adverse_event.AdverseEvent(identifier = odnae_id, identifier_type = "ODNAE ID", source = "NCBO BioPortal", name = result["prefLabel"])
                        event_list.append(ae_temp)
                
    return event_list
        
#   UNIT TESTS
def basic_search_unit_tests(basic_query, ncbo_api_key):
    
    user = User(ncbo_api_key = ncbo_api_key)
    
    print("Beginning basic search for '%s'..." % basic_query)
    
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="all", user = user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
        
    print("\nSearch returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for ae in basic_search_results:
        for iden in ae.identifiers:
            print("- %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()