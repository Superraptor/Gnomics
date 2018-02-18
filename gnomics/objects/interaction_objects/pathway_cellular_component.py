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
#   Get cellular components from pathway.
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
import gnomics.objects.cellular_component
import gnomics.objects.pathway

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    pathway_cellular_component_unit_tests("ko00270")
     
#   Get cellular components.
def get_cellular_components(pathway, user=None):
    molec_array = []
    molec_id_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                    if "DBLINKS" in temp:
                        if "GO" in temp["DBLINKS"]:
                            for temp_go in temp["DBLINKS"]["GO"].split(" "):
                                temp_go_id = "GO:"+str(temp_go)
                                
                                server = "https://rest.ensembl.org"
                                ext = "/ontology/id/" + temp_go_id + "?"
                                r = requests.get(server + ext, headers = {
                                    "Content-Type" : "application/json"
                                })

                                if not r.ok:
                                    print("Something went wrong.")
                                else:
                                    decoded = r.json()
                                    if decoded["namespace"] == "cellular_component":
                                        go_acc = decoded["accession"]
                                        go_name = decoded["name"]
                                        temp_molec = gnomics.objects.cellular_component.CellularComponent(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ensembl", name=go_name)
                                        molec_array.append(temp_molec)

            elif ident["identifier_type"].lower() in ["kegg map pathway", "kegg map pathway id", "kegg map pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_map_pathway(pathway):
                    if "DBLINKS" in temp:
                        if "GO" in temp["DBLINKS"]:
                            for temp_go in temp["DBLINKS"]["GO"].split(" "):
                                temp_go_id = "GO:"+str(temp_go)
                                
                                server = "https://rest.ensembl.org"
                                ext = "/ontology/id/" + temp_go_id + "?"
                                r = requests.get(server + ext, headers = {
                                    "Content-Type" : "application/json"
                                })

                                if not r.ok:
                                    print("Something went wrong.")
                                else:
                                    decoded = r.json()
                                    if decoded["namespace"] == "cellular_component":
                                        go_acc = decoded["accession"]
                                        go_name = decoded["name"]
                                        temp_molec = gnomics.objects.cellular_component.CellularComponent(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ensembl", name=go_name)
                                        molec_array.append(temp_molec)
                            
    return molec_array      
    
#   UNIT TESTS
def pathway_cellular_component_unit_tests(kegg_ko_pathway_id):
    kegg_ko_pathway = gnomics.objects.pathway.Pathway(identifier = kegg_ko_pathway_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
    print("\nGetting cellular component identifiers from KEGG KO PATHWAY ID (%s):" % kegg_ko_pathway_id)
    for molec in get_cellular_components(kegg_ko_pathway):
        for iden in molec.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()