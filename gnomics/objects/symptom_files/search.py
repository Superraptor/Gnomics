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
#   Search for symptoms.
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
import gnomics.objects.symptom

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("chronic pain")

# Return search.
def search(query, source = "ebi"):
    if source == "ebi":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        # See here:
        # https://www.ebi.ac.uk/ols/ontologies
        symp_list = []
        symp_id_array = []
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
                # Taxon agnostic.
                if "SYMP" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in symp_id_array:
                        symp_temp = gnomics.objects.symptom.Symptom(identifier = new_id, identifier_type = "SYMP ID", source = "Ontology Lookup Service", name = doc["label"])
                        symp_list.append(symp_temp)
                        symp_id_array.append(new_id)
        return symp_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for symp in basic_search_results:
        for iden in symp.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()