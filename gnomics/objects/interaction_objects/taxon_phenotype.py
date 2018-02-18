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
#   Get phenotypes from taxon.
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
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    taxon_phenotype_unit_tests("VTO_0011993")
     
#   Get phenotypes.
def get_phenotypes(taxon):
    phenotype_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["vto", "vto identifier", "vto id"]:
            base = "http://kb.phenoscape.org/api/taxon/"
            ext = "phenotypes?taxon=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + ident["identifier"]

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            
            for result in decoded["results"]:
                phenoscape_uuid = result["phenotype"]["@id"].split("/phenoscape/uuid/")[1]
                phenoscape_name = result["phenotype"]["label"]
                
                temp_phen = gnomics.objects.phenotype.Phenotype(identifier = phenoscape_uuid, identifier_type = "Phenoscape UUID", source = "Phenoscape Knowledgebase", name = phenoscape_name)
                phenotype_array.append(temp_phen)
            
    return phenotype_array
    
#   UNIT TESTS
def taxon_phenotype_unit_tests(vto_id):
    vto_taxon = gnomics.objects.tissue.Tissue(identifier = vto_id, identifier_type = "VTO ID", source = "Phenoscape Knowledgebase")
    print("\nGetting phenotype identifiers from VTO identifier (%s):" % vto_id)
    for phenotype in get_phenotypes(vto_taxon):
        for iden in phenotype.identifiers:
            print("- %s [%s] (%s)" % (iden["name"], str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()