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
#   Get drugs from pathway.
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
import gnomics.objects.drug
import gnomics.objects.pathway

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    pathway_drug_unit_tests()
     
#   Get drugs.
def get_drugs(pathway, user=None):
    drug_array = []
    
    for ident in pathway.identifiers:
        if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
            for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                if "COMPOUND" in temp:
                    for kegg_com, norm_name in temp["COMPOUND"].items():
                        if "D" in kegg_com:
                            temp_compound = gnomics.objects.drug.Drug(identifier = kegg_com, identifier_type = "KEGG DRUG Accession", source = "KEGG", name = norm_name, language = None)
                            drug_array.append(temp_compound)

    return drug_array         
    
#   UNIT TESTS
def pathway_drug_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()