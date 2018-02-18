#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       MYGENE
#           https://pypi.python.org/pypi/mygene
#

#
#   Get WikiGene gene.
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
import mygene
import requests

#   MAIN
def main():
    wikigene_unit_tests("ENSG00000157764")

# Returns WikiGene identifier.
def get_wikigene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["wikigene", "wikigene id", "wikigene identifier"]:
            return ident["identifier"]
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
                if new_id["dbname"] == "WikiGene":
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier = new_id["primary_id"], identifier_type = "WikiGene identifier", taxon = "Homo sapiens", source = "Ensembl", name = new_id["display_id"])
                    return new_id["primary_id"]
        
#   UNIT TESTS
def wikigene_unit_tests(ensembl_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting WikiGene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_wikigene_id(ensembl_gene))

#   MAIN
if __name__ == "__main__": main()