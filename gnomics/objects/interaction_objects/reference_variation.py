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
#   Get mutations/variations from reference.
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
import gnomics.objects.variation
import gnomics.objects.reference

#   Other imports.
import json
import requests
import sys
import timeit

#   MAIN
def main():
    reference_variation_unit_tests("26318936", "PMC5002951")

#   Get variations.
def get_variations(reference, taxon="Homo sapiens", user=None):
    species_formatted = taxon.lower().replace(" ", "_")
    
    variation_array = []
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() in ["pmid", "pubmed id", "pubmed identifier"]:
            server = "https://rest.ensembl.org"
            ext = "/variation/" + str(species_formatted) + "/pmid/" + str(ident["identifier"]) + "?"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            
            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                for variant in decoded:
                    if "rs" in variant["name"]:
                        temp_variation = gnomics.objects.variation.Variation(identifier = variant["name"], identifier_type = "RS Number", source = "dbSNP", taxon=taxon)
                        variation_array.append(temp_variation)
                
        elif ident["identifier_type"].lower() == "pmc" or ident["identifier_type"].lower() == "pmc id" or ident["identifier_type"].lower() == "pmc identifier":
            server = "https://rest.ensembl.org"
            ext = "/variation/" + str(species_formatted) + "/pmcid/" + str(ident["identifier"]) + "?"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            
            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                for variant in decoded:
                    if "rs" in variant["name"]:
                        temp_variation = gnomics.objects.variation.Variation(identifier = variant["name"], identifier_type = "RS Number", source = "dbSNP", taxon=taxon)
                        variation_array.append(temp_variation)
                    
    return variation_array
    
#   UNIT TESTS
def reference_variation_unit_tests(pmid, pmcid):
    pmid_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PubMed ID", language = None, source = "PubMed")
    print("Getting variation identifiers from PubMed ID (%s):" % pmid)
    for mut in get_variations(pmid_ref):
        for iden in mut.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
    pmcid_ref = gnomics.objects.reference.Reference(identifier = pmcid, identifier_type = "PMC ID", language = None, source = "PubMed")
    print("\nGetting variation identifiers from PMC ID (%s):" % pmcid)
    for mut in get_variations(pmcid_ref):
        for iden in mut.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()