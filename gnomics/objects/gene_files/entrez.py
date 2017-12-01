#
#
#
#
#

#
#   IMPORT SOURCES:
#       MYGENE
#           https://pypi.python.org/pypi/mygene
#

#
#   Get NCBI/Entrez gene.
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

#   Other imports.
import json
import mygene
import requests

#   MAIN
def main():
    entrez_unit_tests("ENSG00000148795")

#   Get NCBI Entrez gene.
def get_ncbi_entrez_gene(gene, taxon = "Homo sapiens"):
    for gene_obj in gene.gene_objects:
        if 'object_type' in gene_obj:
            if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['taxon'].lower() == taxon):
                return gene_obj['object']
    for ident in self.identifiers:
        if ident["identifier_type"].lower() == "ncbi gene" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "ncbi gene identifier":
            ec = eutils.client.Client()
            # Get Entrez Gene Set.
            egs = ec.efetch(db="gene", id=get_entrez_id(gene))
            # Get individual Entrez Gene.
            eg = egs.entrezgenes[0]
            gene.gene_objects.append({
                'object': eg,
                'object_type': "NCBI Entrez gene",
                'taxon': taxon
            })
            return eg
    
#   Get NCBI Entrez gene.
def get_ncbi_entrez_gene_id(gene, taxon = "Homo sapiens"):
    gene_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "entrez" or ident["identifier_type"].lower() == "entrez id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez gene identifier" or ident["identifier_type"].lower() == "ncbi gene" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi-geneid" or ident["identifier_type"].lower() == "ncbi entrez gene id" or ident["identifier_type"].lower() == "ncbi entrez gene identifier":
            if ident["identifier"] not in gene_array:
                gene_array.append(ident["identifier"])
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier":
            mg = mygene.MyGeneInfo()
            temp_gen = mg.getgene(ident["identifier"])
            new_entrez = str(temp_gen["entrezgene"])
            ncbi_taxon_id = str(temp_gen["taxid"])
            hgnc_symbol = temp_gen["symbol"]
            hgnc_name = temp_gen["name"]
            if new_entrez not in gene_array:
                gnomics.objects.gene.Gene.add_identifier(gene, identifier_type = "Entrez Gene ID", identifier = str(new_entrez), source = "NCBI")
                gene_array.append(str(new_entrez))
        elif ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier":
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene["DBLINKS"]["NCBI-GeneID"],
                'language': None,
                'identifier_type': "NCBI gene identifier",
                'taxon': taxon,
                'source': "NCBI"
            })
            gene_array.append(gnomics.objects.gene.Gene.kegg_gene["DBLINKS"]["NCBI-GeneID"])
        elif ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.gene.Gene.wikidata(gene):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "entrez gene id":
                        for x in prop_dict:
                            gnomics.objects.gene.Gene.add_identifier(gene, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Entrez Gene ID", language = None, source = "Wikidata")
                            gene_array.append(x["mainsnak"]["datavalue"]["value"])
    return gene_array

#   UNIT TESTS
def entrez_unit_tests(ensembl_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("Getting Entrez Gene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for gen in get_ncbi_entrez_gene_id(ensembl_gene):
            print("- %s" % gen)

#   MAIN
if __name__ == "__main__": main()