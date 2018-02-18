#!/usr/bin/env python

#
#
#
#
#

#
#   Get RefSeq RNA.
#
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
import gnomics.objects.transcript

#   Other imports.
import requests
import timeit

#   MAIN
def main():
    refseq_unit_tests()

# Returns RefSeq RNA ID.
def get_refseq_rna_id(transcript):
    trans_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["refseq", "refseq id", "refseq identifier", "refseq rna id", "refseq rna identifier", "refseq rna", "refseq accession", "refseq rna accession", "refseq mrna", "refseq mrna id", "refseq mrna identifier"]):
        if iden["identifier"] not in trans_array:
            trans_array.append(iden["identifier"])
    
    if trans_array:
        return trans_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl transcript", "ensembl transcript id", "ensembl transcript identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + str(iden["identifier"]) + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                print("Something went wrong.")

            else:
                decoded = r.json()
                
                for result in decoded:
                    if result["dbname"] == "RefSeq_mRNA":
                        if result["primary_id"] not in trans_array:
                            trans_array.append(result["primary_id"])
                            gnomics.objects.transcript.Transcript.add_identifier(transcript, identifier=result["primary_id"], identifier_type="RefSeq mRNA ID", language=None, source="Ensembl")
                            
    return trans_array
        
#   UNIT TESTS
def refseq_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()