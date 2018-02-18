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
#   Get protein families from a cellular component.
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
import gnomics.objects.auxiliary_files.identifier
import gnomics.objects.cellular_component
import gnomics.objects.protein_family

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    cellular_component_protein_family_unit_tests("GO_0005634")
    
#   Get protein family identifiers for a cellular component.
def get_protein_families(cellular_component):
    
    prot_fam_id_array = []
    prot_fam_obj_array = []
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cellular_component.identifiers, ["go accession", "go acc", "go id", "go identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for obj in gnomics.objects.cellular_component.CellularComponent.quickgo(cellular_component):
                for new_id in obj["interpro"]:
                    if new_id not in prot_fam_id_array:
                        
                        temp_obj = gnomics.objects.protein_family.ProteinFamily(identifier=new_id, identifier_type="InterPro ID", language=None, source="QuickGO")
                        
                        prot_fam_id_array.append(new_id)
                        prot_fam_obj_array.append(temp_obj)
            
    return prot_fam_obj_array
    
#   UNIT TESTS
def cellular_component_protein_family_unit_tests(go_acc):
    cell_comp = gnomics.objects.cellular_component.CellularComponent(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ontology Lookup Service")
    
    print("Getting protein families from GO accession (%s):" % go_acc)
    for obj in get_protein_families(cell_comp):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()