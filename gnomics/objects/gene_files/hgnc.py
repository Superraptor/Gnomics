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
#   Get HGNC gene.
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
import mygene
import requests

#   MAIN
def main():
    hgnc_unit_tests("hsa:5315", "ENSG00000157764")

# Returns HGNC gene identifier.
def get_hgnc_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower()  in ["hgnc id", "hgnc identifier", "hgnc gene id", "hgnc gene identifier"]:
            return ident["identifier"]
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["kegg", "kegg gene", "kegg gene id", "kegg gene identifier", "kegg id", "kegg identifier"]:
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["HGNC"],
                'language': None,
                'identifier_type': "HGNC gene identifier",
                'taxon': "Homo sapiens",
                'source': "HGNC"
            })
            return gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["HGNC"]
        
        elif ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"]
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for new_id in decoded:
                if new_id["dbname"] == "HGNC":
                    gene.identifiers.append({
                        'identifier': new_id["primary_id"].split(":")[1],
                        'language': None,
                        'identifier_type': "HGNC gene identifier",
                        'taxon': "Homo sapiens",
                        'source': "Ensembl"
                    })
                    return new_id["primary_id"].split(":")[1]
        elif ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
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

                    if en_prop_name.lower() == "hgnc id":
                        for x in prop_dict:
                            gnomics.objects.gene.Gene.add_identifier(gene, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "HGNC ID", language = None, source = "Wikidata", taxon="Homo sapiens")
                            return x["mainsnak"]["datavalue"]["value"]
            
    for gene_obj in gene.gene_objects:
        if 'object_type' in gene_obj:
            if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['taxon'].lower() == taxon):
                return gene_obj['object'].hgnc

# Return HGNC gene symbol.
def get_hgnc_gene_symbol(gene):
    hgnc_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["hgnc symbol", "hgnc gene symbol", "hgnc gene symbol"]:
            if ident["identifier"] not in hgnc_array:
                hgnc_array.append(ident["identifier"])
        
    if hgnc_array:
        return hgnc_array
        
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
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

                    if en_prop_name.lower() == "hgnc symbol":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in hgnc_array:
                                gnomics.objects.gene.Gene.add_identifier(gene, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "HGNC Symbol", language = None, source = "Wikidata", taxon="Homo sapiens")
                                hgnc_array.append(x["mainsnak"]["datavalue"]["value"])
                        
        elif ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"] + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for new_ident in decoded:
                if new_ident["db_display_name"] == "HGNC Symbol":
                    hgnc_symbol = new_ident["display_id"]
                    if hgnc_symbol not in hgnc_array:
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = hgnc_symbol, identifier_type = "HGNC Symbol", source = "Ensembl", taxon="Homo sapiens")
                        hgnc_array.append(hgnc_symbol)
                
    return hgnc_array
            
#   UNIT TESTS
def hgnc_unit_tests(kegg_gene_id, ensembl_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, taxon = "Homo sapiens", source = "KEGG")
    print("Getting HGNC Gene ID from KEGG GENE ID (%s):" % kegg_gene_id)
    print("- %s" % get_hgnc_gene_id(kegg_gene))
    
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    
    print("\nGetting HGNC Gene ID from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_hgnc_gene_id(ensembl_gene))
    
    print("\nGetting HGNC Gene Symbol from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_hgnc_gene_symbol(ensembl_gene))

#   MAIN
if __name__ == "__main__": main()