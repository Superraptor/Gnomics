#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#
#

#
#   Get genes from a gene.
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
import gnomics.objects.tissue

#   Other imports.
import json
import numpy
import requests
import timeit
import xml.etree.ElementTree as ET

#   MAIN
def main():
    gene_gene_unit_tests("ENSG00000134057")

# Get orthologs.
def get_orthologs(gene):
    
    ortho_id_array = []
    ortho_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]:
            server = "https://rest.ensembl.org"
            ext = "/homology/id/" + ident["identifier"] + "?"
            
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.json()
            for homology in decoded["data"]:
                if "homologies" in homology:
                    for item in homology["homologies"]:
                        align_seq = item["target"]["align_seq"]
                        perc_id = item["target"]["perc_id"]
                        species = item["target"]["species"]
                        cigar_line = item["target"]["cigar_line"]
                        gene_id = item["target"]["id"]
                        perc_pos = item["target"]["perc_pos"]
                        protein_id = item["target"]["protein_id"]
                        taxon_id = item["target"]["taxon_id"]
                        
                        proc_species_array = item["target"]["species"].split("_")
                        proc_species_array[0] = proc_species_array[0].capitalize()
                        proc_species = " ".join(proc_species_array)
                        
                        if gene_id not in ortho_id_array:
                            ortho_id_array.append(gene_id)
                            temp_gen = gnomics.objects.gene.Gene(identifier=gene_id, identifier_type="Ensembl Gene ID", language=None, source="Ensembl", taxon=proc_species)
                            ortho_array.append(temp_gen)
            
    return ortho_array
        
#   UNIT TESTS
def gene_gene_unit_tests(ensembl_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("Getting orthologs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for ortholog in get_orthologs(ensembl_gene):
        for iden in ortholog.identifiers:
            print("- %s (%s) [%s]" % (str(iden["identifier"]), iden["identifier_type"], iden["taxon"]))
    
#   MAIN
if __name__ == "__main__": main()