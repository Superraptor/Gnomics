#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get pathways from reference.
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
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
import json
import requests

#   MAIN
def main():
    reference_pathway_unit_tests("14769483", "", "")
     
#   Get pathways.
def get_pathways(reference, user = None):
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier":
            base = "https://beta.openphacts.org/2.1/"
            ext = "pathways/byReference?uri=http%3A%2F%2Fidentifiers.org%2Fpubmed%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            path_array = []
            for item in decoded["result"]["items"]:
                temp_path = gnomics.objects.pathway.Pathway(identifier = item["identifier"].split("/wikipathways/")[1], identifier_type = "WikiPathways ID", source = "OpenPHACTS", name = item["title"])
                path_array.append(temp_path)
            return path_array
    
#   UNIT TESTS
def reference_pathway_unit_tests(pmid, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    pm_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PubMed ID", source = "OpenPHACTS")
    print("\nGetting pathway identifiers from PubMed ID (%s):" % pmid)
    for path in get_pathways(pm_ref, user = user):
        for iden in path.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()