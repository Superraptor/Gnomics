#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get genes from anatomical structure.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.gene

#   Other imports.
import json
import requests

#   MAIN
def main():
    anatomical_structure_gene_unit_tests("UBERON_0003097")
     
#   Get genes affecting entity phenotype.
def get_genes_affecting_phenotype_of(anatomical_structure):
    gene_array = []
    for ident in anatomical_structure.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon identifier" or ident["identifier_type"].lower() == "uberon id":
            base = "http://kb.phenoscape.org/api/gene/"
            ext = "affecting_entity_phenotype?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for result in decoded["results"]:
                gene_name = result["label"]
                gene_taxon = result["taxon"]["label"]
                if "zfin" in result["@id"]:
                    zfin_id = result["@id"].split("http://zfin.org/")[1]
                    temp_gene = gnomics.objects.gene.Gene(identifier = zfin_id, identifier_type = "ZFIN ID", source = "Phenoscape Knowledgebase", taxon = gene_taxon)
                    gene_array.append(temp_gene)
    return gene_array

#   Get genes expressed within entity.
def get_genes_expressed_within(anatomical_structure):
    gene_array = []
    for ident in anatomical_structure.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon identifier" or ident["identifier_type"].lower() == "uberon id":
            base = "http://kb.phenoscape.org/api/taxon/"
            ext = "with_phenotype?entity=%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FBFO_0000050%3E%20some%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + ident["identifier"] + "%3E&quality=%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPATO_0000052%3E&parts=false&limit=20&offset=0&total=false"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for result in decoded["results"]:
                vto_id = result["@id"].split("/obo/")[1]
                sci_name = result["label"]
                temp_taxon = gnomics.objects.taxon.Taxon(identifier = vto_id, identifier_type = "VTO ID", source = "Phenoscape Knowledgebase")
                gnomics.objects.taxon.Taxon.add_identifier(temp_taxon, identifier = sci_name, identifier_type = "Scientific Name", language = "la", source = "Phenoscape Knowledgebase")
                taxa_array.append(temp_taxon)
    return gene_array
    
#   UNIT TESTS
def anatomical_structure_gene_unit_tests(uberon_id):
    uberon_anat = gnomics.objects.tissue.Tissue(identifier = uberon_id, identifier_type = "UBERON ID", source = "Phenoscape Knowledgebase")
    print("\nGetting gene identifiers which affect UBERON identifier (%s) entity phenotypes:" % uberon_id)
    for gene in get_genes_affecting_phenotype_of(uberon_anat):
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    print("\nGetting gene identifiers expressed within UBERON identifier (%s) entity:" % uberon_id)
    for gene in get_genes_expressed_within(uberon_anat):
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()