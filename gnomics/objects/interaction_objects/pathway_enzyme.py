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
#   Get enzymes from pathway.
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
    pathway_enzyme_unit_tests("ko00270")
     
#   Get eyzmes.
def get_enzymes(pathway, user=None):
    enz_array = []
    enz_id_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                    temp_id = temp["ORTHOLOGY"]
                    for key, value in temp_id.items():
                        if key not in enz_id_array:
                            name=value
                            if "[" in name:
                                sub_name=name.split("[")[0].strip()
                                new_iden=name.split("[")[1].strip()
                                new_iden=new_iden.replace("]","")
                                
                                for sub_iden in new_iden.split(" "):
                                    new_sub_iden=sub_iden.strip()
                                    if "EC:" in new_sub_iden:
                                        enz_id_array.append(new_sub_iden)
                                        temp_enz = gnomics.objects.enzyme.Enzyme(identifier=new_sub_iden, identifier_type="EC Number", language=None, source="KEGG", name=sub_name)
                                        enz_array.append(temp_enz)
                                    else:
                                        enz_id_array.append(new_sub_iden)
                                        temp_enz = gnomics.objects.enzyme.Enzyme(identifier="EC:"+new_sub_iden, identifier_type="EC Number", language=None, source="KEGG", name=sub_name)
                                        enz_array.append(temp_enz)
                            
    return enz_array      
    
#   UNIT TESTS
def pathway_enzyme_unit_tests(kegg_ko_pathway_id):
    kegg_ko_pathway = gnomics.objects.pathway.Pathway(identifier = kegg_ko_pathway_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
    print("\nGetting enzyme identifiers from KEGG KO PATHWAY ID (%s):" % kegg_ko_pathway_id)
    for enz in get_enzymes(kegg_ko_pathway):
        for iden in enz.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()