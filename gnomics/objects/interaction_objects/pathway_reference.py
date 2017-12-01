#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get references from pathway.
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
    pathway_reference_unit_tests("WP1984", "d4169a1a", "c133be1db72a55682afaf86b94c9e850")
     
#   Get references.
def get_references(pathway, user = None):
    for ident in pathway.identifiers:
        if ident["identifier_type"].lower() == "wikipathways" or ident["identifier_type"].lower() == "wikipathways id" or ident["identifier_type"].lower() == "wikipathways identifier" or ident["identifier_type"].lower() == "wikipathway" or ident["identifier_type"].lower() == "wikipathway id" or ident["identifier_type"].lower() == "wikipathway identifier":
            
            base = "https://beta.openphacts.org/2.1/"
            ext = "pathway/getReferences?uri=http%3A%2F%2Fidentifiers.org%2Fwikipathways%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            # print(decoded["result"])
            
            ref_array = []
            if isinstance(decoded["result"]["primaryTopic"]["latest_version"]["hasPart"], list):
                for item in decoded["result"]["primaryTopic"]["latest_version"]["hasPart"]:
                
                    ref_array.append(
                        gnomics.objects.reference.Reference(identifier = item.split("/pubmed/")[1], identifier_type = "PubMed ID", source = "OpenPHACTS")
                    )
                
            else:
                ref_array.append(
                    gnomics.objects.reference.Reference(identifier = decoded["result"]["primaryTopic"]["latest_version"]["hasVersion"].split("/pubmed/")[1], identifier_type = "PubMed ID", source = "OpenPHACTS")
                )

            return ref_array
             
    
#   UNIT TESTS
def pathway_reference_unit_tests(wikipathways_id, openphacts_app_id, openphacts_app_key):
    print("NOT FUNCTIONAL.")
    
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    wiki_pathway = gnomics.objects.drug.Drug(identifier = wikipathways_id, identifier_type = "WikiPathways ID", source = "OpenPHACTS")
    
    print("\nGetting reference identifiers from WikiPathways ID (%s):" % wikipathways_id)
    for ref in get_references(wiki_pathway, user = user):
        for iden in ref.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()