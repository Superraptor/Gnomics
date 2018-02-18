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
#   Search for transcripts.
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
import gnomics.objects.disease
import gnomics.objects.protein

#   Other imports.
import eutils
import json
import requests
import timeit
import xml.etree.ElementTree as ET

#   MAIN
def main():
    basic_search_unit_tests("insulin")
    
# Return search.
def search(query, source="entrez", user=None):
    trans_list = []
    trans_id_array = []
    
    if source in ["ncbi", "entrez", "all"]:
        
        try:
            ec = eutils.client.Client()
            esr = ec.esearch(db="gene", term=query)
            id_array = []
            for x in esr.ids:
                id_array.append(x)
            egs = ec.efetch(db="gene", id=id_array)
            result_set = []
            for gen in egs.entrezgenes:
                hgnc = gen.hgnc
                genus_species = gen.genus_species
                references = gen.references

                transcript_ids = [p.acv for p in references[0].products]
                transcript_labels = [p.label for p in references[0].products]

                for counter, temp_iden in enumerate(transcript_ids):
                    if temp_iden not in trans_id_array:
                        temp_name = None
                        if transcript_labels[counter] is not None and gen.hgnc is not None:
                            temp_name = gen.hgnc + ", " + transcript_labels[counter]
                        elif transcript_labels[counter] is not None:
                            temp_name = transcript_labels[counter]

                        temp_trans = gnomics.objects.gene.Gene(identifier = temp_iden, language = None, source = "Entrez Programming Utilities", identifier_type = "RefSeq Accession", taxon = genus_species, name=temp_name)

                        trans_list.append(temp_trans)
                        trans_id_array.append(temp_iden)
                        
        except eutils.exceptions.EutilsNCBIError:
            print("NCBI returned data which appears to be incorrect or invalid.")
            
        except:
            print("Some other error occurred.")
    
    return trans_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="all")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nSearch returned %s result(s) with the following transcript IDs:" % str(len(basic_search_results)))
    for trans in basic_search_results:
        for iden in trans.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()