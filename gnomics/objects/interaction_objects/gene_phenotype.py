#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get phenotypes from a gene.
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
import gnomics.objects.compound
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.phenotype
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    gene_phenotype_unit_tests("4750")

# Get phenotypes.
def get_phenotypes(gene):
    phen_array = []
    phen_obj_array = []
    phen_dict = {}
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ncbi", "ncbi gene", "ncbi gene id", "ncbi gene identifier", "entrez gene id"]:
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/gene/NCBIGene:" + str(ident["identifier"]) + "/phenotypes/"
            r = requests.get(server+ext)

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for obj in decoded["associations"]:
                if obj["object"]["id"] not in phen_array:
                
                    # Human Phenotype (HP) Ontology ID, also HPO ID
                    phen_array.append(obj["object"]["id"])

                    new_phen = gnomics.objects.phenotype.Phenotype(identifier = obj["object"]["id"], identifier_type = "Human Phenotype Ontology ID", language = None, source = "Monarch Initiative", taxon = "Homo sapiens")
                    phen_dict[obj["object"]["id"]] = new_phen
                    phen_obj_array.append(new_phen)
                    
    return phen_obj_array
        
#   UNIT TESTS
def gene_phenotype_unit_tests(ncbi_gene_id):
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("Getting phenotypes (HPO IDs) from NCBI gene ID (%s):" % ncbi_gene_id)
    start = timeit.timeit()
    all_phen = get_phenotypes(ncbi_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for phen in all_phen:
        for iden in phen.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()