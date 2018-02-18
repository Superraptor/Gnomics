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
#   Get pathways from molecular function.
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
import requests
import timeit

#   MAIN
def main():
    molecular_function_pathway_unit_tests("K15406")
     
#   Get pathways.
def get_pathways(molecular_function, user=None):
    path_array = []
    path_id_array = []
    
    for ident in molecular_function.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                for ko_ortho in gnomics.objects.molecular_function.MolecularFunction.kegg_orthology(molecular_function):
                    for key, value in ko_ortho["PATHWAY"].items():
                        if key not in path_id_array:
                            path_id_array.append(key)
                            temp_path = gnomics.objects.pathway.Pathway(identifier=key, language=None, identifier_type="KEGG KO PATHWAY ID", source="KEGG")
                            path_array.append(temp_path)
                            
    return path_array      
    
#   UNIT TESTS
def molecular_function_pathway_unit_tests(kegg_orthology_id):
    kegg_orthology = gnomics.objects.molecular_function.MolecularFunction(identifier = kegg_orthology_id, identifier_type = "KEGG ORTHOLOGY ID", source = "KEGG")
    print("\nGetting pathway identifiers from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for path in get_pathways(kegg_orthology):
        for iden in path.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()