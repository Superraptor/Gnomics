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
import gnomics.objects.protein

#   Other imports.
import json
import requests

#   MAIN
def main():
    gene_protein_unit_tests("hsa:3630", "ENSG00000157764")

# Returns NCBI protein identifier.
def get_proteins(gene, taxon = "Homo sapiens"):
    protein_id_array = []
    protein_obj_array = []
    protein_obj_dict = {}
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg gene id" or ident["identifier_type"].lower() == "kegg gene identifier" or ident["identifier_type"].lower() == "kegg gene":
            kegg_gene_map = gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["NCBI-ProteinID"]
            temp_prot = gnomics.objects.protein.Protein(identifier = kegg_gene_map, language = None, identifier_type = "NCBI protein identifier", source = "NCBI", taxon = taxon)
            temp_prot.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["UniProt"],
                'language': None,
                'identifier_type': "UniProt identifier",
                'taxon': taxon,
                'source': "UniProt"
            })
            protein_id_array.append(kegg_gene_map)
            protein_obj_dict[kegg_gene_map] = temp_prot
            protein_obj_array.append(temp_prot)
        elif ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier" or ident["identifier_type"].lower() == "ensembl":
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"]
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for new_id in decoded:
                if new_id["dbname"] == "Uniprot_gn":
                    temp_prot = gnomics.objects.protein.Protein(identifier = new_id["primary_id"], language = None, identifier_type = "UniProt accession", source = "Ensembl", taxon = taxon)
                    protein_id_array.append(new_id["primary_id"])
                    protein_obj_dict[new_id["primary_id"]] = temp_prot
                    protein_obj_array.append(temp_prot)
    return protein_obj_array
        
#   UNIT TESTS
def gene_protein_unit_tests(kegg_gene_id, ensembl_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, species = "Homo sapiens", source = "KEGG")
    print("Getting NCBI Protein IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    for key, val in get_proteins(kegg_gene).items():
        print("- %s" % str(key))
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, species = "Homo sapiens", source = "Ensembl")
    print("\nGetting UniProt accessions from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for key, val in get_proteins(ensembl_gene).items():
        print("- %s" % str(key))
    
#   MAIN
if __name__ == "__main__": main()