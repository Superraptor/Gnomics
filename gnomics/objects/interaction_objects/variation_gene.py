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
#   Get gene from a variation.
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
import gnomics.objects.variation

#   Other imports.
import json
import myvariant
import requests
import timeit

#   MAIN
def main():
    variation_gene_unit_tests("chr7:g.140453134T>C", "RS121913364")

# Get gene.
def get_gene(variation):
    gene_array = []
    gene_id_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variation.identifiers, ["coding hgvs", "coding hgvs id", "coding hgvs identifier", "genomic hgvs", "genomic hgvs id", "genomic hgvs identifier", "hgvs", "hgvs id", "hgvs identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for obj in gnomics.objects.variation.Variation.hgvs(variation):
                if "civic" in obj:
                    entrez_id = str(obj["civic"]["entrez_id"])
                    entrez_name = obj["civic"]["entrez_name"]

                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
                        
                if "clinvar" in obj:
                    entrez_id = str(obj["clinvar"]["gene"]["id"])
                    entrez_name = obj["clinvar"]["gene"]["symbol"]
                    
                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
                        
                if "dbnsfp" in obj:
                    ensembl_id = obj["dbnsfp"]["ensembl"]["geneid"]
                    ensembl_name = obj["dbnsfp"]["genename"]
                    
                    if ensembl_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=ensembl_id, identifier_type="Ensembl Gene ID", language=None, source="MyVariant", name=ensembl_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(ensembl_id)
                        
                if "dbsnp" in obj:
                    entrez_id = str(obj["dbsnp"]["gene"]["geneid"])
                    entrez_name = obj["dbsnp"]["gene"]["symbol"]
                    
                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
                        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variation.identifiers, ["reference snp id", "reference snp identifier", "rs", "rs id", "rs identifier", "rs number", "rsid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for obj in gnomics.objects.variation.Variation.hgvs(variation):
            
                if "civic" in obj:
                    entrez_id = str(obj["civic"]["entrez_id"])
                    entrez_name = obj["civic"]["entrez_name"]

                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
                        
                if "clinvar" in obj:
                    entrez_id = str(obj["clinvar"]["gene"]["id"])
                    entrez_name = obj["clinvar"]["gene"]["symbol"]
                    
                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
                        
                if "dbnsfp" in obj:
                    ensembl_id = obj["dbnsfp"]["ensembl"]["geneid"]
                    ensembl_name = obj["dbnsfp"]["genename"]
                    
                    if ensembl_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=ensembl_id, identifier_type="Ensembl Gene ID", language=None, source="MyVariant", name=ensembl_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(ensembl_id)
                
                if "dbsnp" in obj:
                    entrez_id = str(obj["dbsnp"]["gene"]["geneid"])
                    entrez_name = obj["dbsnp"]["gene"]["symbol"]
                    
                    if entrez_id not in gene_id_array:
                        temp_gene = gnomics.objects.gene.Gene(identifier=entrez_id, identifier_type="Entrez ID", language=None, source="MyVariant", name=entrez_name)
                        gene_array.append(temp_gene)
                        gene_id_array.append(entrez_id)
            
    return gene_array
            
#   UNIT TESTS
def variation_gene_unit_tests(hgvs_id, rsid):
    hgvs_var = gnomics.objects.variation.Variation(identifier = hgvs_id, identifier_type = "HGVS ID", language = None, source = None)
    print("\nGetting gene identifiers from HGVS ID (%s):" % hgvs_id)
    for gene in get_gene(hgvs_var):
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
    dbsnp_var = gnomics.objects.variation.Variation(identifier = rsid, identifier_type = "RS Number", language = None, source = None)
    print("\nGetting gene identifiers from RSID (%s):" % rsid)
    for gene in get_gene(dbsnp_var):
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()