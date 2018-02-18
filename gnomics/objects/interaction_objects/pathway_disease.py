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
#   Get diseases from pathway.
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
import gnomics.objects.disease
import gnomics.objects.pathway

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    pathway_disease_unit_tests("ko00270")
     
#   Get diseases.
def get_diseases(pathway, user=None):
    dis_array = []
    dis_id_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                    if "DISEASE" in temp:
                        for key, value in temp["DISEASE"].items():
                            kegg_disease_id = key
                            kegg_disease_name = value
                            
                            if kegg_disease_id not in dis_id_array:
                                temp_dis = gnomics.objects.disease.Disease(identifier=kegg_disease_id, identifier_type="KEGG DISEASE ID", source="KEGG", language=None, name=kegg_disease_name)
                                dis_array.append(temp_dis)

            elif ident["identifier_type"].lower() in ["kegg map pathway", "kegg map pathway id", "kegg map pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_map_pathway(pathway):
                    if "DISEASE" in temp:
                        for key, value in temp["DISEASE"].items():
                            kegg_disease_id = key
                            kegg_disease_name = value
                            
                            if kegg_disease_id not in dis_id_array:
                                temp_dis = gnomics.objects.disease.Disease(identifier=kegg_disease_id, identifier_type="KEGG DISEASE ID", source="KEGG", language=None, name=kegg_disease_name)
                                dis_array.append(temp_dis)
                            
    return dis_array      
    
#   UNIT TESTS
def pathway_disease_unit_tests(kegg_ko_pathway_id):
    kegg_ko_pathway = gnomics.objects.pathway.Pathway(identifier = kegg_ko_pathway_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
    print("\nGetting disease identifiers from KEGG KO PATHWAY ID (%s):" % kegg_ko_pathway_id)
    for dis in get_diseases(kegg_ko_pathway):
        for iden in dis.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()