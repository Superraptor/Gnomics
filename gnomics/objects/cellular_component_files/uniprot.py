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
#   Get UniprotKB keyword for molecular functions.
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
import gnomics.objects.auxiliary_files.identifier
import gnomics.objects.cellular_component

#   Other imports.
from bioservices import QuickGO
import json
import re
import requests
import timeit

#   MAIN
def main():
    uniprot_unit_tests("GO:0043231")

#   Get UniProtKB Keywords.
def get_uniprotkb_kw(cellular_component, user=None):
    uniprot_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cellular_component.identifiers, ["uniprotkb-kw", "uniprotkb kw", "uniprot-kw", "uniprot kw", "uniprotkb keyword", "uniprotkb-keyword", "uniprot keyword", "uniprot-keyword"]):
        if iden["identifier"] not in uniprot_array:
            uniprot_array.append(iden["identifier"])
            
    if uniprot_array:
        return uniprot_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cellular_component.identifiers, ["go acc", "go accession", "go id", "go identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for obj in gnomics.objects.cellular_component.CellularComponent.quickgo(cellular_component):
                for new_id in obj["uniprotkb-kw"]:
                    if new_id not in uniprot_array:
                        gnomics.objects.cellular_component.CellularComponent.add_identifier(cellular_component, identifier=new_id, identifier_type="UniProtKB-KW", language=None, source="QuickGO")
                        uniprot_array.append(new_id)

    return uniprot_array

#   UNIT TESTS
def uniprot_unit_tests(go_acc):
    cell_comp = gnomics.objects.cellular_component.CellularComponent(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ontology Lookup Service")
    
    print("\nGetting UniProtKB-KW from GO Accession (%s):" % go_acc)
    start = timeit.timeit()
    uniprot_array = get_uniprotkb_kw(cell_comp)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for uni in uniprot_array:
        print("\t- " + str(uni))

#   MAIN
if __name__ == "__main__": main()