#
#
#
#
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.disease
import gnomics.objects.gene

#   Other imports.
import json
import requests

#   MAIN
def main():
    gene_disease_unit_tests("4750", "173505")

# Get diseases.
def get_diseases(gene):
    dis_array = []
    dis_dict = {}
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi gene" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "entrez gene id":
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/gene/NCBIGene:" + ident["identifier"] + "/diseases/"
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
                for edge in subj["evidence_graph"]["edges"]:
                    break
        elif ident["identifier_type"].lower() == "orphanet" or ident["identifier_type"].lower() == "orphanet gene" or ident["identifier_type"].lower() == "orphanet gene id" or ident["identifier_type"].lower() == "orphanet gene identifier" or ident["identifier_type"].lower() == "orphanet id":
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
                for edge in subj["evidence_graph"]["edges"]:
                    break
    return dis_array
        
#   UNIT TESTS
def gene_disease_unit_tests(ncbi_gene_id, orphanet_gene_id):
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, species = "Homo sapiens", source = "NCBI")
    print("Getting diseases from NCBI gene ID (%s):" % ncbi_gene_id)
    for dis in get_diseases(ncbi_gene):
        print("- %s" % dis)
    orphanet_gene = gnomics.objects.gene.Gene(identifier = orphanet_gene_id, identifier_type = "Orphanet Gene ID", language = None, species = "Homo sapiens", source = "Orphanet")
    print("\nGetting diseases from Orphanet gene ID (%s):" % orphanet_gene_id)
    for dis in get_diseases(orphanet_gene):
        print("- %s" % dis)
    
#   MAIN
if __name__ == "__main__": main()