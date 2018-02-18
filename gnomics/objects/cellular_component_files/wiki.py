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
#   Get Wikipedia information.
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
import gnomics.objects.cellular_component

#   Other imports.
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
import json
import requests

#   MAIN
def main():
    wiki_unit_tests("GO:0005634")
    
#   Get Wikipedia accession (English).
def get_english_wikipedia_accession(cellular_component, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cellular_component.identifiers, ["wikipedia", "wikipedia accession"]):
        if iden["identifier"] not in wiki_array:
            wiki_array.append(iden["identifier"])
    
    if wiki_array:
        return wiki_array
    
    ids_completed = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cellular_component.identifiers, ["go accession", "go acc", "go id", "go identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for obj in gnomics.objects.cellular_component.CellularComponent.quickgo(cellular_component):
                for new_id in obj["wikipedia"]:
                    if new_id not in wiki_array:
                        gnomics.objects.cellular_component.CellularComponent.add_identifier(cellular_component, identifier=new_id, identifier_type="Wikipedia Accession", language="en", source="QuickGO")
                        wiki_array.append(new_id)
                    
    return wiki_array

#   UNIT TESTS
def wiki_unit_tests(go_acc):
    cell_comp = gnomics.objects.cellular_component.CellularComponent(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ontology Lookup Service")
    
    print("Getting English Wikipedia accession from GO accession (%s):" % go_acc)
    for comp in get_english_wikipedia_accession(cell_comp):
        print("- %s" % comp)
        
#   MAIN
if __name__ == "__main__": main()