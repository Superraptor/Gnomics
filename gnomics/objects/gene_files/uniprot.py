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
#   Get UniProt gene.
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
    uniprot_unit_tests()

# Returns UniProtKB Gene accession.
def get_uniprot_kb_acc(gene):
    uniprot_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["uniprot gene", "uniprot gene accession"]:
            uniprot_array.append(ident["identifier"])
        
    if uniprot_array:
        return uniprot_array
        
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
                if new_id["dbname"] == "Uniprot_gn":
                    gnomics.objects.gene.Gene.add_identifier(identifier = new_id["primary_id"], identifier_type = "UniProt Gene Accession", taxon = "Homo sapiens", source = "Ensembl", name = new_id["display_id"])
                    uniprot_array.append(new_id["primary_id"])
        
    return uniprot_array
        
#   UNIT TESTS
def uniprot_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()