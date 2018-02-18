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
#   Get phenotype from a variation.
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
import gnomics.objects.phenotype
import gnomics.objects.variation

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    variation_phenotype_unit_tests("rs699")

# Get phenotypes.
def get_phenotypes(variation):
    phen_array = []
    phen_id_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variation.identifiers, ["reference snp id", "reference snp identifier", "rs", "rs id", "rs identifier", "rs number", "rsid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            if iden["taxon"]:
                server = "https://rest.ensembl.org"
                ext = "/variation/" + iden["taxon"].lower().replace(" ", "_") + "/" + iden["identifier"] + "?phenotypes=1"

                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for phen in decoded["phenotypes"]:
                    if "ontology_accessions" in phen:
                        for onto in phen["ontology_accessions"]:
                            if "HP:" in onto and onto not in phen_id_array:
                                temp_phen = gnomics.objects.phenotype.Phenotype(identifier = onto, identifier_type = "HPO ID", language = None, source = phen["source"], taxon = "Homo sapiens")
                                phen_id_array.append(onto)
                                phen_array.append(temp_phen)
            else:
                server = "https://rest.ensembl.org"
                ext = "/variation/" + "homo_sapiens" + "/" + iden["identifier"] + "?phenotypes=1"

                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for phen in decoded["phenotypes"]:
                    if "ontology_accessions" in phen:
                        for onto in phen["ontology_accessions"]:
                            if "HP:" in onto and onto not in phen_id_array:
                                temp_phen = gnomics.objects.phenotype.Phenotype(identifier = onto, identifier_type = "HPO ID", language = None, source = phen["source"], taxon = "Homo sapiens")
                                phen_id_array.append(onto)
                                phen_array.append(temp_phen)
            
    return phen_array
            
#   UNIT TESTS
def variation_phenotype_unit_tests(rsid):
    rs_var = gnomics.objects.variation.Variation(identifier = rsid, identifier_type = "RS Number", language = None, source = None, taxon = "Homo sapiens")
    print("\nGetting phenotypes from RSID (%s):" % rsid)
    for phen in get_phenotypes(rs_var):
        for iden in phen.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()