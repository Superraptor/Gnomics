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
#   Get KEGG ORTHOLOGY.
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
import gnomics.objects.pathway

#   Other imports.
from bioservices import *

#   MAIN
def main():
    kegg_unit_tests()

#   Get KEGG ORTHOLOGY object.
def get_kegg_orthology(molecular_function):
    kegg_orthology_array = []
    kegg_orthology_id_array = []
    
    for molec_obj in molecular_function.molecular_function_objects:
        if 'object_type' in molec_obj:
            if molec_obj['object_type'].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier", "kegg orthology object", "kegg ko object"]:
                if 'object' in molec_obj:
                    kegg_orthology_array.append(related_obj)
                    
    if kegg_orthology_array:
        return kegg_orthology_array
                    
    for identifier in get_kegg_orthology_id(molecular_function):
        if identifier not in kegg_orthology_id_array: 
            s = KEGG()
            res = s.get(identifier)
            kegg_orthology = s.parse(res)
            gnomics.objects.molecular_function.MolecularFunction.add_object(molecular_function, obj=kegg_orthology, object_type="KEGG ORTHOLOGY")
            kegg_orthology_id_array.append(identifier)
            kegg_orthology_array.append(kegg_orthology)

    return kegg_orthology_array
            
#   Get KEGG ORTHOLOGY ID.
def get_kegg_orthology_id(molecular_function):
    kegg_orthology_array = []
    for ident in molecular_function.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                if ident["identifier"] not in kegg_orthology_array:
                    kegg_orthology_array.append(ident["identifier"])
    return kegg_orthology_array

#   UNIT TESTS
def kegg_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()