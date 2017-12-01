#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get compounds from pathway.
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
import gnomics.objects.compound
import gnomics.objects.drug
import gnomics.objects.pathway

#   Other imports.
import json
import requests

#   MAIN
def main():
    pathway_compound_unit_tests("WP1002", "", "")
     
#   Get compounds.
def get_compounds(pathway, user = None):
    for ident in pathway.identifiers:
        if ident["identifier_type"].lower() == "wikipathways" or ident["identifier_type"].lower() == "wikipathways id" or ident["identifier_type"].lower() == "wikipathways identifier" or ident["identifier_type"].lower() == "wikipathway" or ident["identifier_type"].lower() == "wikipathway id" or ident["identifier_type"].lower() == "wikipathway identifier":
            base = "https://beta.openphacts.org/2.1/"
            ext = "pathway/getCompounds?uri=http%3A%2F%2Fidentifiers.org%2Fwikipathways%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            com_array = []
            for item in decoded["result"]["primaryTopic"]["latest_version"]["hasPart"]:
                if "hmdb" in item:
                    temp_com = gnomics.objects.compound.Compound(identifier = item.split("/hmdb/")[1], identifier_type = "HMDB ID", source = "OpenPHACTS")
                    com_array.append(temp_com)
                elif "kegg.compound" in item:
                    temp_com = gnomics.objects.compound.Compound(identifier = item.split("/kegg.compound/")[1], identifier_type = "KEGG COMPOUND ID", source = "OpenPHACTS")
                    com_array.append(temp_com)
                elif "chebi" in item:
                    temp_com = gnomics.objects.compound.Compound(identifier = item.split("/chebi/")[1], identifier_type = "ChEBI ID", source = "OpenPHACTS")
                    com_array.append(temp_com)
            return com_array
    
#   UNIT TESTS
def pathway_compound_unit_tests(wikipathways_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    wiki_pathway = gnomics.objects.drug.Drug(identifier = wikipathways_id, identifier_type = "WikiPathways ID", source = "OpenPHACTS")
    print("\nGetting compound identifiers from WikiPathways ID (%s):" % wikipathways_id)
    for com in get_compounds(wiki_pathway, user = user):
        for iden in com.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()