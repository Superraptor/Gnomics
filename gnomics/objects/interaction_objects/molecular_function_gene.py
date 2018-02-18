#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices
#

#
#   Get genes from molecular function.
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
import gnomics.objects.molecular_function
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
import json
import requests
import timeit

#   MAIN
def main():
    molecular_function_gene_unit_tests("K15406")
     
#   Get genes.
def get_genes(molecular_function, user=None):
    gene_array = []
    gene_id_array = []
    
    for ident in molecular_function.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                for ko_ortho in gnomics.objects.molecular_function.MolecularFunction.kegg_orthology(molecular_function):
                    for key, value in ko_ortho["GENES"].items():
                        if key not in gene_id_array:
                            for sub_val in value.split(" "):
                                new_val = sub_val.strip()
                                s = KEGG()
                                final_gene = key.lower() + ":" + str(sub_val)
                                res = s.get(final_gene)
                                gene = s.parse(res)
                                
                                if gene != 404:
                                    taxon = gene["ORGANISM"].replace(key.lower(),"").strip().split("(")[0].strip()

                                    gene_id_array.append(key)
                                    temp_gene = gnomics.objects.gene.Gene(identifier=final_gene, language=None, identifier_type="KEGG Gene ID", source="KEGG", taxon=taxon)

                                    if "DBLINKS" in gene:
                                        if "NCBI-GeneID" in gene["DBLINKS"]:
                                            gnomics.objects.gene.Gene.add_identifier(temp_gene, identifier=gene["DBLINKS"]["NCBI-GeneID"], identifier_type="NCBI Gene ID", source="KEGG", language=None)

                                    gnomics.objects.gene.Gene.add_object(temp_gene, obj=gene, object_type="KEGG GENE")

                                    gene_array.append(temp_gene)
                            
    return gene_array      
    
#   UNIT TESTS
def molecular_function_gene_unit_tests(kegg_orthology_id):
    kegg_orthology = gnomics.objects.molecular_function.MolecularFunction(identifier = kegg_orthology_id, identifier_type = "KEGG ORTHOLOGY ID", source = "KEGG")
    print("\nGetting gene identifiers from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for gene in get_genes(kegg_orthology):
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()