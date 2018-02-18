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
#   Get protein from a transcript.
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
import gnomics.objects.protein
import gnomics.objects.transcript

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    transcript_protein_unit_tests("ENST00000288602")

# Get protein.
def get_protein(transcript, user=None):
    prot_array = []
    prot_id_array = []
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
                if "Translation" in decoded:
                    ensembl_prot_id = decoded["Translation"]["id"]
                    species = decoded["Translation"]["species"][0].upper() + decoded["Translation"]["species"].replace("_", " ")[1:]
                    temp_prot = gnomics.objects.protein.Protein(identifier=ensembl_prot_id, identifier_type="Ensembl Protein ID", language=None, source="Ensembl", taxon=species)
                    prot_array.append(temp_prot)
                    prot_id_array.append(ensembl_prot_id)
            
    if prot_array:
        return prot_array
                            
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
                    ensembl_prot_id = decoded["Translation"]["id"]
                    species = decoded["Translation"]["species"][0].upper() + decoded["Translation"]["species"].replace("_", " ")[1:]
                    temp_prot = gnomics.objects.protein.Protein(identifier=ensembl_prot_id, identifier_type="Ensembl Protein ID", language=None, source="Ensembl", taxon=species)
                    prot_array.append(temp_prot)
                    prot_id_array.append(ensembl_prot_id)
                
            
    return prot_array
        
#   UNIT TESTS
def transcript_protein_unit_tests(ensembl_transcript_id):
    ensembl_trans = gnomics.objects.transcript.Transcript(identifier = str(ensembl_transcript_id), identifier_type = "Ensembl Transcript ID", source = "Ensembl")
    print("Getting gene from transcript (Ensembl ID) (%s):" % ensembl_transcript_id)
    start = timeit.timeit()
    all_prot = get_protein(ensembl_trans)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for prot in all_prot:
        for iden in prot.identifiers:
            print("- %s" % str(iden["identifier"]))
    
#   MAIN
if __name__ == "__main__": main()