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
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    pathway_reference_unit_tests("WP1984", "", "", "ko00270")
     
#   Get references.
def get_references(pathway, user=None):
    ref_array = []
    ref_id_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"].lower() in ["wikipathways", "wikipathways id", "wikipathways identifier", "wikipathway", "wikipathway id", "wikipathway identifier"] and user is not None:
            base = "https://beta.openphacts.org/2.1/"
            ext = "pathway/getReferences?uri=http%3A%2F%2Fidentifiers.org%2Fwikipathways%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:

                decoded = json.loads(r.text)
                if isinstance(decoded["result"]["primaryTopic"]["latest_version"]["hasPart"], list):
                    for item in decoded["result"]["primaryTopic"]["latest_version"]["hasPart"]:
                        ref_array.append(
                            gnomics.objects.reference.Reference(identifier = item.split("/pubmed/")[1], identifier_type = "PubMed ID", source = "OpenPHACTS")
                        )

                else:
                    ref_array.append(
                        gnomics.objects.reference.Reference(identifier = decoded["result"]["primaryTopic"]["latest_version"]["hasVersion"].split("/pubmed/")[1], identifier_type = "PubMed ID", source = "OpenPHACTS")
                    )
                
        elif ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
            for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                if "REFERENCE" in temp:
                    for ref in temp["REFERENCE"]:
                        if "REFERENCE" in ref:

                            if "PMID" in ref["REFERENCE"]:
                                pmid = ref["REFERENCE"].split(":")[1].strip()
                                if pmid not in ref_id_array:
                                    title = ref["TITLE"]
                                    temp_ref = gnomics.objects.reference.Reference(identifier=pmid, identifier_type="PMID", language=None, source="KEGG", name=title)
                                    ref_id_array.append(pmid)
                                    ref_array.append(temp_ref)
                            else:
                                print(ref["REFERENCE"])
                                
                        elif "TITLE" in ref:
                            if title not in ref_id_array:
                                title = ref["TITLE"]
                                temp_ref = gnomics.objects.reference.Reference(identifier=title, identifier_type="Title", language="en", source="KEGG", name=title)
                                ref_id_array.append(title)
                                ref_array.append(temp_ref)
                                
        elif ident["identifier_type"].lower() in ["kegg map pathway", "kegg map pathway id", "kegg map pathway identifier"]:
            for temp in gnomics.objects.pathway.Pathway.kegg_map_pathway(pathway):
                if "REFERENCE" in temp:
                    for ref in temp["REFERENCE"]:
                        if "REFERENCE" in ref:

                            if "PMID" in ref["REFERENCE"]:
                                pmid = ref["REFERENCE"].split(":")[1].strip()
                                if pmid not in ref_id_array:
                                    title = ref["TITLE"]
                                    temp_ref = gnomics.objects.reference.Reference(identifier=pmid, identifier_type="PMID", language=None, source="KEGG", name=title)
                                    ref_id_array.append(pmid)
                                    ref_array.append(temp_ref)
                            else:
                                print(ref["REFERENCE"])
                                
                        elif "TITLE" in ref:
                            if title not in ref_id_array:
                                title = ref["TITLE"]
                                temp_ref = gnomics.objects.reference.Reference(identifier=title, identifier_type="Title", language="en", source="KEGG", name=title)
                                ref_id_array.append(title)
                                ref_array.append(temp_ref)

    return ref_array         
    
#   UNIT TESTS
def pathway_reference_unit_tests(wikipathways_id, openphacts_app_id, openphacts_app_key, kegg_ko_pathway_id):
    kegg_ko_pathway = gnomics.objects.pathway.Pathway(identifier = kegg_ko_pathway_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
    print("\nGetting reference identifiers from KEGG KO PATHWAY ID (%s):" % kegg_ko_pathway_id)
    for ref in get_references(kegg_ko_pathway):
        for iden in ref.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    wiki_pathway = gnomics.objects.pathway.Pathway(identifier = wikipathways_id, identifier_type = "WikiPathways ID", source = "OpenPHACTS")
    print("\nGetting reference identifiers from WikiPathways ID (%s):" % wikipathways_id)
    for ref in get_references(wiki_pathway, user = user):
        for iden in ref.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()