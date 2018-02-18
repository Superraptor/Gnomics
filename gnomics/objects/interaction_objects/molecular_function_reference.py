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
#   Get references from molecular function.
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
    molecular_function_reference_unit_tests("K15406")
     
#   Get references.
def get_references(molecular_function, user=None):
    ref_array = []
    ref_id_array = []
    
    for ident in molecular_function.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                for ko_ortho in gnomics.objects.molecular_function.MolecularFunction.kegg_orthology(molecular_function):
                    for ref in ko_ortho["REFERENCE"]:
                        if "PMID" in ref["REFERENCE"]:
                            pmid = ref["REFERENCE"].split(":")[1].strip()
                            if pmid not in ref_id_array:
                                title = ref["TITLE"]
                                temp_ref = gnomics.objects.reference.Reference(identifier=pmid, identifier_type="PMID", language=None, source="KEGG", name=title)
                                ref_id_array.append(pmid)
                                ref_array.append(temp_ref)
                        else:
                            print(ref["REFERENCE"])
                            
    return ref_array      
    
#   UNIT TESTS
def molecular_function_reference_unit_tests(kegg_orthology_id):
    kegg_orthology = gnomics.objects.molecular_function.MolecularFunction(identifier = kegg_orthology_id, identifier_type = "KEGG ORTHOLOGY ID", source = "KEGG")
    print("\nGetting reference identifiers from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for ref in get_references(kegg_orthology):
        for iden in ref.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()