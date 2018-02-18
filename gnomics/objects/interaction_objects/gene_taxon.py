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
#   Get taxon from a gene.
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
import gnomics.objects.gene
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    gene_taxon_unit_tests("675", "ENSG00000113916")

# Get gene taxon.
def get_taxon(gene, user=None):
    tax_id_array = []
    tax_obj_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["entrez gene id", "entrez gene identifier", "entrez gene", "ncbi entrez gene identifier", "ncbi entrez gene", "ncbi gene id"]:    
            for gene_obj in gnomics.objects.gene.Gene.ncbi_entrez_gene(gene):
                if gene_obj.genus_species not in tax_id_array:
                    tax_id_array.append(gene_obj.genus_species)
                    tax_id_array.append(gene_obj.tax_id)
                    temp_tax = gnomics.objects.taxon.Taxon(identifier=gene_obj.genus_species, identifier_type="Scientific Name", source="NCBI", language="la")
                    gnomics.objects.taxon.Taxon.add_identifier(temp_tax, identifier=gene_obj.tax_id, identifier_type="NCBI Taxonomy ID", source="NCBI", language=None)
                    tax_obj_array.append(temp_tax)

        elif ident["identifier_type"].lower() in ["ensembl gene id", "ensembl gene identifier", "ensembl gene", "ensembl"]:
            for gene_obj in gnomics.objects.gene.Gene.ensembl_gene(gene):
                proc_species_array = gene_obj["species"].split("_")
                proc_species_array[0] = proc_species_array[0].capitalize()
                proc_species = " ".join(proc_species_array)
                if proc_species not in tax_id_array:
                    tax_id_array.append(proc_species)
                    temp_tax = gnomics.objects.taxon.Taxon(identifier=proc_species, identifier_type="Scientific Name", source="NCBI", language="la")
                    tax_obj_array.append(temp_tax)
    
        elif ident["identifier_type"].lower() in ["hgnc approved symbol", "hgnc gene symbol", "hgnc symbol"]: 
            if "Homo sapiens" not in tax_id_array:
                tax_id_array.append("Homo sapiens")
                temp_tax = gnomics.objects.taxon.Taxon(identifier="Homo sapiens", identifier_type="Scientific Name", source="HGNC", language="la")
                tax_obj_array.append(temp_tax)

    return tax_obj_array
    
#   UNIT TESTS
def gene_taxon_unit_tests(entrez_gene_id, ensembl_gene_id):
    entrez_gene = gnomics.objects.gene.Gene(identifier = entrez_gene_id, identifier_type = "Entrez Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("Getting taxon from NCBI Entrez gene ID (%s):" % entrez_gene_id)
    for taxa in get_taxon(entrez_gene):
        for iden in taxa.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting taxon from Ensembl Gene ID (%s):" % ensembl_gene_id)
    start = timeit.timeit()
    all_taxa = get_taxon(ensembl_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for taxon in all_taxa:
        for iden in taxon.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()