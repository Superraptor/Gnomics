#
#
#
#
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.reference
import gnomics.objects.variation

#   Other imports.
import json
import requests
import sys

#   MAIN
def main():
    reference_variation_unit_tests("26318936", "PMC5002951")

#   Get variations.
def get_variations(reference, taxon = "Homo sapiens", user = None):
    species_formatted = taxon.lower().replace(" ", "_")
    variation_array = []
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier":
            server = "https://rest.ensembl.org"
            ext = "/variation/" + species_formatted + "/pmid/" + ident["identifier"] + "?"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for variant in decoded:
                if "rs" in variant["name"]:
                    temp_variation = gnomics.objects.variation.Variation(identifier = variant["name"], identifier_type = "RS Number", source = "dbSNP")
                    variation_array.append(temp_variation)
        elif ident["identifier_type"].lower() == "pmc" or ident["identifier_type"].lower() == "pmc id" or ident["identifier_type"].lower() == "pmc identifier":
            server = "https://rest.ensembl.org"
            ext = "/variation/" + species_formatted + "/pmcid/" + ident["identifier"] + "?"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for variant in decoded:
                if "rs" in variant["name"]:
                    temp_variation = gnomics.objects.variation.Variation(identifier = variant["name"], identifier_type = "RS Number", source = "dbSNP")
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