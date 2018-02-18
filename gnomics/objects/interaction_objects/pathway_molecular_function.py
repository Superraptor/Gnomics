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
#   Get molecular functions from pathway.
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
import gnomics.objects.molecular_function
import gnomics.objects.pathway

#   Other imports.
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    pathway_molecular_function_unit_tests("ko00270")
     
#   Get molecular functions.
def get_molecular_functions(pathway, user=None):
    molec_array = []
    molec_id_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                    if "ORTHOLOGY" in temp:
                        temp_id = temp["ORTHOLOGY"]
                        for key, value in temp_id.items():
                            if key not in molec_id_array:
                                name=value
                                if "[" in name:
                                    name=name.split("[")[0].strip()
                                molec_id_array.append(key)
                                temp_molec = gnomics.objects.molecular_function.MolecularFunction(identifier=key, identifier_type="KEGG ORTHOLOGY ID", language=None, source="KEGG", name=name)
                                molec_array.append(temp_molec)
                    
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
                                    
                                    if decoded["namespace"] == "molecular_function":
                                        go_acc = decoded["accession"]
                                        go_name = decoded["name"]
                                        temp_molec = gnomics.objects.molecular_function.MolecularFunction(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ensembl", name=go_name)
                                        
                                        molec_array.append(temp_molec)

            elif ident["identifier_type"].lower() in ["kegg map pathway", "kegg map pathway id", "kegg map pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_map_pathway(pathway):
                    if "ORTHOLOGY" in temp:
                        temp_id = temp["ORTHOLOGY"]
                        for key, value in temp_id.items():
                            if key not in molec_id_array:
                                name=value
                                if "[" in name:
                                    name=name.split("[")[0].strip()
                                molec_id_array.append(key)
                                temp_molec = gnomics.objects.molecular_function.MolecularFunction(identifier=key, identifier_type="KEGG ORTHOLOGY ID", language=None, source="KEGG", name=name)
                                molec_array.append(temp_molec)
                            
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
                                    
                                    if decoded["namespace"] == "molecular_function":
                                        go_acc = decoded["accession"]
                                        go_name = decoded["name"]
                                        temp_molec = gnomics.objects.molecular_function.MolecularFunction(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ensembl", name=go_name)
                                        
                                        molec_array.append(temp_molec)
                            
    return molec_array      
    
#   UNIT TESTS
def pathway_molecular_function_unit_tests(kegg_ko_pathway_id):
    kegg_ko_pathway = gnomics.objects.pathway.Pathway(identifier = kegg_ko_pathway_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
    print("\nGetting molecular function identifiers from KEGG KO PATHWAY ID (%s):" % kegg_ko_pathway_id)
    for molec in get_molecular_functions(kegg_ko_pathway):
        for iden in molec.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()