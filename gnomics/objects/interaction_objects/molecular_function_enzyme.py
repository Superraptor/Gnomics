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
#   Get enzymes from molecular function.
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
    molecular_function_enzyme_unit_tests("K15406")
     
#   Get enzymes.
def get_enzymes(molecular_function, user=None):
    enz_array = []
    enz_id_array = []
    
    for ident in molecular_function.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                for ko_ortho in gnomics.objects.molecular_function.MolecularFunction.kegg_orthology(molecular_function):
                    if "EC:" in ko_ortho["DEFINITION"]:
                        proc_idens = ko_ortho["DEFINITION"].split("[")[1].strip().replace("]","").strip()
                        
                        for proc_iden in proc_idens.split(" "):
                            if "EC:" in proc_iden:
                                if proc_iden not in enz_id_array:
                                    temp_enz = gnomics.objects.enzyme.Enzyme(identifier=proc_iden, identifier_type="EC Number", source="KEGG", language=None, name=ko_ortho["DEFINITION"].split("[")[0].strip())
                                    enz_id_array.append(proc_iden)
                                    enz_array.append(temp_enz)
                            else:
                                new_proc_iden = "EC:" + str(proc_iden)
                                if new_proc_iden not in enz_id_array:
                                    temp_enz = gnomics.objects.enzyme.Enzyme(identifier=new_proc_iden, identifier_type="EC Number", source="KEGG", language=None, name=ko_ortho["DEFINITION"].split("[")[0].strip())
                                    enz_id_array.append(new_proc_iden)
                                    enz_array.append(temp_enz)
    return enz_array      
    
#   UNIT TESTS
def molecular_function_enzyme_unit_tests(kegg_orthology_id):
    kegg_orthology = gnomics.objects.molecular_function.MolecularFunction(identifier = kegg_orthology_id, identifier_type = "KEGG ORTHOLOGY ID", source = "KEGG")
    print("\nGetting enzyme identifiers from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for enz in get_enzymes(kegg_orthology):
        for iden in enz.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()