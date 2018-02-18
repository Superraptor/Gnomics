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
#   Get gene from a transcript.
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
import gnomics.objects.transcript

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    transcript_gene_unit_tests("ENST00000288602")

# Get gene.
def get_gene(transcript, user=None):
    gene_array = []
    gene_id_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl transcript", "ensembl transcript id", "ensembl transcript identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            server = "https://rest.ensembl.org"
            ext = "/lookup/id/" + str(iden["identifier"]) + "?expand=1"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                ensembl_gene_id = decoded["Parent"]
                species = decoded["species"][0].upper() + decoded["species"].replace("_", " ")[1:]
                temp_gene = gnomics.objects.gene.Gene(identifier=ensembl_gene_id, identifier_type="Ensembl Gene ID", language=None, source="Ensembl", taxon=species)
                gene_array.append(temp_gene)
                gene_id_array.append(ensembl_gene_id)
    
    if gene_array:
        return gene_array
                            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["refseq", "refseq id", "refseq identifier", "refseq rna id", "refseq rna identifier", "refseq rna", "refseq accession", "refseq rna accession", "refseq mrna", "refseq mrna id", "refseq mrna identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for ensembl_iden in gnomics.objects.transcript.Transcript.ensembl_transcript_id(transcript):
            
                server = "https://rest.ensembl.org"
                ext = "/lookup/id/" + str(ensembl_iden) + "?expand=1"
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    ensembl_gene_id = decoded["Parent"]
                    species = decoded["species"][0].upper() + decoded["species"].replace("_", " ")[1:]
                    temp_gene = gnomics.objects.gene.Gene(identifier=ensembl_gene_id, identifier_type="Ensembl Gene ID", language=None, source="Ensembl", taxon=species)
                    gene_array.append(temp_gene)
                    gene_id_array.append(ensembl_gene_id)
            
    return gene_array
        
#   UNIT TESTS
def transcript_gene_unit_tests(ensembl_transcript_id):
    ensembl_trans = gnomics.objects.transcript.Transcript(identifier = str(ensembl_transcript_id), identifier_type = "Ensembl Transcript ID", source = "Ensembl")
    print("Getting gene from transcript (Ensembl ID) (%s):" % ensembl_transcript_id)
    start = timeit.timeit()
    all_genes = get_gene(ensembl_trans)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for gene in all_genes:
        for iden in gene.identifiers:
            print("- %s" % str(iden["identifier"]))
    
#   MAIN
if __name__ == "__main__": main()