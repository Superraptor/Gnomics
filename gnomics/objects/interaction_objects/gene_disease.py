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
#   Get diseases from a gene.
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
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    gene_disease_unit_tests("4750", "173505")

# Get diseases.
def get_diseases(gene):
    dis_array = []
    dis_obj_array = []
    dis_dict = {}
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ncbi", "ncbi gene", "ncbi gene id", "ncbi gene identifier", "entrez gene id"]:
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/gene/NCBIGene:" + str(ident["identifier"]) + "/diseases/"
            r = requests.get(server+ext)

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for subj in decoded["associations"]:
                omim_dis = subj["object"]["id"].split(":")[1]

                if omim_dis not in dis_array:
                    new_dis = gnomics.objects.disease.Disease(identifier = omim_dis, identifier_type = "MIM Number", language = None, source = "OMIM")

                    dis_array.append(omim_dis)
                    dis_dict[omim_dis] = new_dis
                    dis_obj_array.append(new_dis)

                for edge in subj["evidence_graph"]["edges"]:
                    # Come back to this!!!
                    break

        elif ident["identifier_type"].lower() in ["orphanet", "orphanet gene", "orphanet gene id", "orphanet gene identifier", "orphanet id"]:
            print("Orphanet Gene ID to disease conversion is currently non-functional.")
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/gene/Orphanet:" + ident["identifier"] + "/diseases/"
            r = requests.get(server+ext)

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for subj in decoded["associations"]:
                omim_dis = subj["object"]["id"].split(":")[1]

                if omim_dis not in dis_array:
                    new_dis = gnomics.objects.disease.Disease(identifier = omim_dis, identifier_type = "MIM Number", language = None, source = "OMIM")

                    dis_array.append(omim_dis)
                    dis_dict[omim_dis] = new_dis
                    dis_obj_array.append(new_dis)

                for edge in subj["evidence_graph"]["edges"]:
                    break
                    
    return dis_obj_array
        
#   UNIT TESTS
def gene_disease_unit_tests(ncbi_gene_id, orphanet_gene_id):
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("Getting diseases from NCBI gene ID (%s):" % ncbi_gene_id)
    for dis in get_diseases(ncbi_gene):
        for iden in dis.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
        
    orphanet_gene = gnomics.objects.gene.Gene(identifier = orphanet_gene_id, identifier_type = "Orphanet Gene ID", language = None, taxon = "Homo sapiens", source = "Orphanet")
    print("\nGetting diseases from Orphanet gene ID (%s):" % orphanet_gene_id)
    start = timeit.timeit()
    all_dis = get_diseases(orphanet_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for dis in all_dis:
        for iden in dis.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()