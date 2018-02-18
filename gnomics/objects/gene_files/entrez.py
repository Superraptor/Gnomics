#!/usr/bin/env python

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
import eutils
import json
import mygene
import requests

#   MAIN
def main():
    entrez_unit_tests("ENSG00000148795")

#   Get NCBI Entrez gene.
def get_ncbi_entrez_gene(gene):
    
    entrez_obj_array = []
    
    for gene_obj in gene.gene_objects:
        if 'object_type' in gene_obj:
            if gene_obj['object_type'].lower() == 'ncbi entrez gene':
                entrez_obj_array.append(gene_obj['object'])
                
    if entrez_obj_array:
        return entrez_obj_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi-geneid", "entrez id", "entrez identifier", "ncbi id", "ncbi identifier"]:
            ec = eutils.client.Client()

            # Get Entrez Gene Set.
            egs = ec.efetch(db="gene", id=ident["identifier"])

            # Get individual Entrez Gene.
            #
            # Functions in Entrezgene object:
            # - common_tax
            # - description
            # - gene_commentaries
            #   - acv
            #   - version
            #   - heading
            #   - accession
            #   - products
            #       - accession
            #       - products
            #       - version
            #       - heading
            #       - acv
            #       - label
            #       - type
            #       - genomic_coords
            #   - label
            # - gene_id
            # - genus_species
            # - hgnc
            # - locus
            # - maploc
            # - references
            # - summary
            # - synonyms
            # - tax_id
            # - type
            eg = egs.entrezgenes[0]

            gnomics.objects.gene.Gene.add_object(gene, obj=eg, object_type="NCBI Entrez Gene")

            entrez_obj_array.append(eg)

    return entrez_obj_array
    
#   Get NCBI Entrez gene.
def get_ncbi_entrez_gene_id(gene):
    gene_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi-geneid", "entrez id", "entrez identifier", "ncbi id", "ncbi identifier"]:
            if ident["identifier"] not in gene_array:
                gene_array.append(ident["identifier"])
                
    if gene_array:
        return gene_array
                
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            mg = mygene.MyGeneInfo()
            temp_gen = mg.getgene(ident["identifier"])
            
            new_entrez = str(temp_gen["entrezgene"])
            ncbi_taxon_id = str(temp_gen["taxid"])
            hgnc_symbol = temp_gen["symbol"]
            hgnc_name = temp_gen["name"]
            
            if new_entrez not in gene_array:
                gnomics.objects.gene.Gene.add_identifier(gene, identifier_type = "Entrez Gene ID", identifier = str(new_entrez), source = "NCBI")
                gene_array.append(str(new_entrez))
                
        elif ident["identifier_type"].lower() in ["kegg", "kegg gene", "kegg gene id", "kegg gene identifier", "kegg id", "kegg identifier"]:
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene["DBLINKS"]["NCBI-GeneID"],
                'language': None,
                'identifier_type': "NCBI gene identifier",
                'taxon': ident["identifier"],
                'source': "NCBI"
            })
            gene_array.append(gnomics.objects.gene.Gene.kegg_gene["DBLINKS"]["NCBI-GeneID"])
            
        elif ident["identifier_type"].lower() in ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]:
            for stuff in gnomics.objects.gene.Gene.wikidata(gene):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    #print(decoded)
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