#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get proteins from a gene.
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
import gnomics.objects.pathway

#   Other imports.
import json
import requests

#   MAIN
def main():
    gene_pathway_unit_tests("hsa:3630", "ENSG00000157764")

# Get pathways.
def get_pathways(gene):
    path_array = []
    path_obj_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg gene id" or ident["identifier_type"].lower() == "kegg gene identifier" or ident["identifier_type"].lower() == "kegg gene":
            kegg_gene_path = gnomics.objects.gene.Gene.kegg_gene(gene)["PATHWAY"]
            for kegg_path_id, kegg_path_name in kegg_gene_path.items():
                if kegg_path_id not in path_array:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = kegg_path_id, language = None, identifier_type = "KEGG PATHWAY hsa ID", source = "KEGG")
                    path_array.append(kegg_path_id)
                    path_obj_array.append(temp_path)
        elif ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier" or ident["identifier_type"].lower() == "ensembl":
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"]
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for new_id in decoded:
                if new_id["dbname"] == "Reactome_gene" and new_id["primary_id"] not in path_array:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = new_id["primary_id"], language = None, identifier_type = "REACTOME Pathway ID", source = "Ensembl")
                    path_array.append(new_id["primary_id"])
                    path_obj_array.append(temp_path)
    return path_obj_array
        
#   UNIT TESTS
def gene_pathway_unit_tests(kegg_gene_id, ensembl_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, species = "Homo sapiens", source = "KEGG")
    print("Getting KEGG PATHWAY hsa IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    for path in get_pathways(kegg_gene):
        print("- %s" % path)
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, species = "Homo sapiens", source = "Ensembl")
    print("\nGetting REACTOME pathway IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for path in get_pathways(ensembl_gene):
        print("- %s" % path)
    
#   MAIN
if __name__ == "__main__": main()