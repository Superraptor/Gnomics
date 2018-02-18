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
#   Get Reactome gene.
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
import gnomics.objects.gene

#   Other imports.
import json
import requests

#   MAIN
def main():
    reactome_unit_tests()

# Returns Reactome Gene.
def get_reactome_gene_id(gene):
    reactome_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["reactome gene", "reactome gene id", "reactome gene identifier", "reactome", "reactome id"]:
            reactome_array.append(ident["identifier"])
        
    if reactome_array:
        return reactome_array
        
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"]
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            
            for new_id in decoded:
                if new_id["dbname"] == "Reactome_gene":
                    gnomics.objects.gene.Gene.add_identifier(identifier = new_id["primary_id"], identifier_type = "Reactome Gene ID", taxon = "Homo sapiens", source = "Ensembl")
                    reactome_array.append(new_id["primary_id"])
        
    return reactome_array
        
#   UNIT TESTS
def reactome_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()