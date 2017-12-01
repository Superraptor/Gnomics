#
#
#
#
#

#
#   IMPORT SOURCES:
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

#   MAIN
def main():
    basic_search_unit_tests("Fatigue")

# Return search.
def search(query, user = None, source = "ols", search_type = "exact"):
    event_list = []
    event_id_array = []
    
    if (source == "fda" or source == "all") and user is not None:
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
    if (source == "ols" or source == "all"):
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=aero,oae,ovae"
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
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
    return event_list
        
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following identifiers (EBI):" % str(len(basic_search_results)))
    for ae in basic_search_results:
        for iden in ae.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()