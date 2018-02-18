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
#   Get genes from a drug.
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
import gnomics.objects.drug
import gnomics.objects.gene

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    drug_gene_unit_tests("DB00398", "", "")
    
# Get drug-gene interactions.
def get_genes(drug, user=None, source=None, interaction_sources=None, interaction_types=None, gene_categories=None, source_trust_levels=None):
    gene_array = []
    
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["drugbank accession", "drugbank", "drugbank id", "drugbank identifier"]:
            compounds = gnomics.objects.drug.Drug.compounds(drug, user = user)
            for com in compounds:
                genes = gnomics.objects.compound.Compound.genes(com, source = source, interaction_sources = interaction_sources, interaction_types = interaction_types, gene_categories = gene_categories, source_trust_levels = source_trust_levels)
                gene_array.extend(genes)
                
    if gene_array:            
        return gene_array
    
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["rxcui", "rxnorm id", "rxnorm identifier"]:
            gnomics.objects.drug.Drug.drugbank_id(drug)
            compounds = gnomics.objects.drug.Drug.compounds(drug, user = user)
            if compounds:
                for com in compounds:
                    genes = gnomics.objects.compound.Compound.genes(com, source = source, interaction_sources = interaction_sources, interaction_types = interaction_types, gene_categories = gene_categories, source_trust_levels = source_trust_levels)
                    gene_array.extend(genes)
                
    return gene_array

#   UNIT TESTS
def drug_gene_unit_tests(drugbank_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    drugbank_drug = gnomics.objects.drug.Drug(identifier = drugbank_id, identifier_type = "DrugBank ID", source = "OpenPHACTS")
    start = timeit.timeit()
    all_genes = get_genes(drugbank_drug, user = user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for gene in all_genes:
        for iden in gene.identifiers:
            if iden["identifier_type"] == "HGNC Approved Symbol":
                print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()