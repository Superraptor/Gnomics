#
#
#
#
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.gene
import gnomics.objects.phenotype

#   Other imports.
import json
import requests

#   MAIN
def main():
    gene_phenotype_unit_tests("4750")

# Get phenotypes.
def get_phenotypes(gene):
    phen_array = []
    phen_dict = {}
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi gene" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "entrez gene id":
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/gene/NCBIGene:" + ident["identifier"] + "/phenotypes/"
            r = requests.get(server+ext)
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for obj in decoded["associations"]:
                if obj["object"]["id"] not in phen_array:
                    # Human Phenotype (HP) Ontology ID, also HPO ID
                    phen_array.append(obj["object"]["id"])
                    new_phen = gnomics.objects.phenotype.Phenotype(identifier = obj["object"]["id"], identifier_type = None, language = None, source = "Monarch Initiative")
                    phen_dict[obj["object"]["id"]] = new_phen
    return phen_array
        
#   UNIT TESTS
def gene_phenotype_unit_tests(ncbi_gene_id):
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, species = "Homo sapiens", source = "NCBI")
    print("Getting phenotypes (HPO IDs) from NCBI gene ID (%s):" % ncbi_gene_id)
    for phen in get_phenotypes(ncbi_gene):
        print("- %s" % phen)
    
#   MAIN
if __name__ == "__main__": main()