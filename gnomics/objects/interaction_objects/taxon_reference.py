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
#   Get references from taxa.
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
import gnomics.objects.taxon
import gnomics.objects.reference

#   Other imports.
import isbnlib
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    taxon_reference_unit_tests("9606")
     
#   Get references.
def get_references(taxon):
    ref_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["ncbi taxonomy", "ncbi taxonomy id", "ncbi taxonomy identifier"]:
            for obj in gnomics.objects.taxon.Taxon.eol_page(taxon):
                unfound_references = []
                found_references = []
                for ref in obj["references"]:
                    ref_str = ref
                    ref_set = gnomics.objects.reference.Reference.parse_citation(ref, score_threshold=70, normalized_score_threshold=100)
                    
                    for ref in ref_set:
                        for iden in ref.identifiers:
                            print("- %s" % iden["identifier"])
                        found_references.append(found_references)
                
                    if not ref_set:
                        unfound_references.append(ref)
                    else:
                         if len(ref_set) > 1:
                            print(ref_str)
                
                print("References found: %s / %s" % (str(len(found_references)), str(len(found_references) + len(unfound_references))))
                
                unfound_part_2 = []
                found_part_2 = []
                
                for ref in unfound_references:
                    urls = gnomics.objects.reference.Reference.extract_urls(ref)
                    for url in urls:
                        temp_ref = gnomics.objects.reference.Reference(identifier=url, identifier_type="URL", source="World Wide Web")
                        found_part_2.append(temp_ref)
                        
                    if not urls:
                        unfound_part_2.append(ref)
                        
                found_part_2.extend(found_references)
                unfound_part_2.extend(unfound_references)
                        
                print("References found: %s / %s" % (str(len(found_part_2)), str(len(found_part_2) + len(unfound_part_2))))
    
    return ref_array
    
#   UNIT TESTS
def taxon_reference_unit_tests(ncbi_tax_id):
    ncbi_taxon = gnomics.objects.taxon.Taxon(identifier=ncbi_tax_id, identifier_type="NCBI Taxonomy ID", source="NCBI")
    get_references(ncbi_taxon)

#   MAIN
if __name__ == "__main__": main()