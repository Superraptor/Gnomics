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
#   Get taxa from anatomical structure.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    anatomical_structure_taxon_unit_tests("UBERON_0003097")
     
#   Get taxa.
def get_taxa(anatomical_structure, user=None):
    taxa_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anatomical_structure.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.replace(":", "_")
            
            base = "http://kb.phenoscape.org/api/taxon/"
            ext = "with_phenotype?entity=%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FBFO_0000050%3E%20some%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + str(proc_id) + "%3E&quality=%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPATO_0000052%3E&parts=false&limit=20&offset=0&total=false"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                #r.raise_for_status()
                #sys.exit()
                print("Something went wrong.")
            else:

                decoded = json.loads(r.text)
                for result in decoded["results"]:
                    vto_id = result["@id"].split("/obo/")[1]
                    sci_name = result["label"]

                    temp_taxon = gnomics.objects.taxon.Taxon(identifier = vto_id, identifier_type = "VTO ID", source = "Phenoscape Knowledgebase")
                    gnomics.objects.taxon.Taxon.add_identifier(temp_taxon, identifier = sci_name, identifier_type = "Scientific Name", language = "la", source = "Phenoscape Knowledgebase")
                    taxa_array.append(temp_taxon)
            
    return taxa_array
    
#   UNIT TESTS
def anatomical_structure_taxon_unit_tests(uberon_id):
    uberon_anat = gnomics.objects.tissue.Tissue(identifier = uberon_id, identifier_type = "UBERON ID", source = "Phenoscape Knowledgebase")
    
    start = timeit.timeit()
    getting_taxa = get_taxa(uberon_anat)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nGetting taxon identifiers from UBERON identifier (%s):" % uberon_id)
    for taxa in getting_taxa:
        for iden in taxa.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()