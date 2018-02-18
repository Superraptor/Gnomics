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
#   Get Ensembl gene.
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
import mygene
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    ensembl_unit_tests("hsa:3630", "3630", "ZNF14")
    
# Return Ensembl gene.
def get_ensembl_gene(gene):
    ensembl_obj_array = []
    
    for gene_obj in gene.gene_objects:
        if gene_obj["object_type"].lower() in ["ensembl", "ensembl gene"]:
            ensembl_obj_array.append(gene_obj["object"])
    
    if ensembl_obj_array:
        return ensembl_obj_array
    
    for ensembl_id in get_ensembl_gene_id(gene):
    
        server = "https://rest.ensembl.org"
        ext = "/lookup/id/" + ensembl_id + "?expand=1"

        r = requests.get(server+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()

        decoded = r.json()
        new_ensembl_obj = {
            'source': decoded["source"],
            'object_type': decoded["object_type"],
            'logic_name': decoded["logic_name"],
            'seq_region_name': decoded["seq_region_name"],
            'db_type': decoded["db_type"],
            'strand': decoded["strand"],
            'id': decoded["id"],
            'version': decoded["version"],
            'species': decoded["species"],
            'assembly_name': decoded["assembly_name"],
            'display_name': decoded["display_name"],
            'description': decoded["description"],
            'end': decoded["end"],
            'biotype': decoded["biotype"],
            'start': decoded["start"]
        }
        
        temp_ensembl_obj = {
            'object': new_ensembl_obj,
            'object_type': "Ensembl Gene"
        }
        gnomics.objects.gene.Gene.add_object(gene, obj = new_ensembl_obj, object_type = "Ensembl Gene")
        ensembl_obj_array.append(new_ensembl_obj)
        
    return ensembl_obj_array

# Returns Ensembl gene identifier.
def get_ensembl_gene_id(gene, user=None):
    ensembl_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            ensembl_array.append(ident["identifier"])
        
    if ensembl_array:
        return ensembl_array
        
    for ident in gene.identifiers:    
        if ident["identifier_type"].lower() in ["kegg", "kegg gene", "kegg gene id", "kegg gene identifier", "kegg id", "kegg identifier"]:
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Ensembl"],
                'language': None,
                'identifier_type': "Ensembl gene identifier",
                'taxon': ident["taxon"],
                'source': "Ensembl"
            })
            ensembl_array.append(gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Ensembl"])
        
        
        elif ident["identifier_type"].lower() in ["hgnc approved symbol", "hgnc gene symbol", "hgnc symbol"]:
            base = "http://rest.ensembl.org"
            ext = "/xrefs/symbol/" + "homo_sapiens" + "/" + ident["identifier"] + "?external_db=HGNC"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            for result in decoded:
                if "ENSG" in result["id"]:
                    ensembl_array.append(result["id"])
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["id"], identifier_type = "Ensembl Gene ID", source = "Ensembl")
        
        elif ident["identifier_type"].lower() in ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi-geneid", "entrez id", "entrez identifier", "ncbi id", "ncbi identifier"]:
            taxon = ident["taxon"]
            if ident["taxon"] is None:
                for gene_obj in gnomics.objects.gene.Gene.ncbi_entrez_gene(gene):
                    taxon = gene_obj.genus_species
            
            base = "http://rest.ensembl.org"
            ext = "/xrefs/symbol/" + taxon.lower().replace(" ", "_") + "/" + ident["identifier"] + "?external_db=EntrezGene"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:

                decoded = json.loads(r.text)
                for result in decoded:
                    if "ENSG" in result["id"]:
                        ensembl_array.append(result["id"])
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["id"], identifier_type = "Ensembl Gene ID", source = "Ensembl")

    return ensembl_array
        
#   UNIT TESTS
def ensembl_unit_tests(kegg_gene_id, ncbi_entrez_gene_id, hgnc_symbol):
    print("NOT FUNCTIONAL.")
    
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