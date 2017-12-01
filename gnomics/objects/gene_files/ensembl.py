#
#
#
#
#

#
#   Get Ensembl gene.
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.gene

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    ensembl_unit_tests("hsa:3630", "3630", "ZNF14")

# Returns Ensembl gene identifier.
def get_ensembl_gene_id(gene, taxon = "Homo sapiens"):
    ensembl_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier" or ident["identifier_type"].lower() == "ensembl":
            ensembl_array.append(ident["identifier"])
    if ensembl_array:
        return ensembl_array
    for ident in gene.identifiers:    
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg gene id" or ident["identifier_type"].lower() == "kegg gene identifier":
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Ensembl"],
                'language': None,
                'identifier_type': "Ensembl gene identifier",
                'taxon': taxon,
                'source': "Ensembl"
            })
            ensembl_array.append(gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Ensembl"])
        elif ident["identifier_type"].lower() == "hgnc symbol" or ident["identifier_type"].lower() == "hgnc approved symbol": 
            base = "http://rest.ensembl.org"
            ext = "/xrefs/symbol/" + taxon.lower().replace(" ", "_") + "/" + ident["identifier"] + "?external_db=HGNC"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for result in decoded:
                if "ENSG" in result["id"]:
                    ensembl_array.append(result["id"])
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["id"], identifier_type = "Ensembl Gene ID", source = "Ensembl")
        elif ident["identifier_type"].lower() == "entrez" or ident["identifier_type"].lower() == "entrez id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez gene identifier" or ident["identifier_type"].lower() == "ncbi gene" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi-geneid" or ident["identifier_type"].lower() == "ncbi entrez gene id" or ident["identifier_type"].lower() == "ncbi entrez gene identifier":
            base = "http://rest.ensembl.org"
            ext = "/xrefs/symbol/" + taxon.lower().replace(" ", "_") + "/" + ident["identifier"] + "?external_db=EntrezGene"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for result in decoded:
                if "ENSG" in result["id"]:
                    ensembl_array.append(result["id"])
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["id"], identifier_type = "Ensembl Gene ID", source = "Ensembl")            
    return ensembl_array
        
#   UNIT TESTS
def ensembl_unit_tests(kegg_gene_id, ncbi_entrez_gene_id, hgnc_symbol):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, taxon = "Homo sapiens", source = "KEGG")
    print("Getting Ensembl Gene IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    for ens in get_ensembl_gene_id(kegg_gene):
        print("- %s" % ens)
    hgnc_gene = gnomics.objects.gene.Gene(identifier = hgnc_symbol, identifier_type = "HGNC Symbol", language = None, taxon = "Homo sapiens", source = "HGNC")
    print("\nGetting Ensembl Gene IDs from HGNC Symbol (%s):" % hgnc_symbol)
    for ens in get_ensembl_gene_id(hgnc_gene):
        print("- %s" % ens)
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_entrez_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("\nGetting Ensembl Gene IDs from NCBI Entrez Gene ID (%s):" % ncbi_entrez_gene_id)
    for ens in get_ensembl_gene_id(ncbi_gene):
        print("- %s" % ens)

#   MAIN
if __name__ == "__main__": main()