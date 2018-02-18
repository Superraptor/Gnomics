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
#   Get references from anatomical structure.
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
import gnomics.objects.reference

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    anatomical_structure_reference_unit_tests("UBERON_0003097")
     
#   Get references.
def get_references(anatomical_structure):
    ref_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anatomical_structure.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            print("As of 18 January 2018, this query type is not available due to an internal server error. Please check back for updates.")
            
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.replace(":", "_")
                
            base = "http://kb.phenoscape.org/api/study/"
            ext = "query?entity=%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FBFO_0000050%3E%20some%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + str(proc_id) + "%3E"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("It appears something went wrong.")
            else:
                decoded = json.loads(r.text)
                
    return ref_array
    
#   UNIT TESTS
def anatomical_structure_reference_unit_tests(uberon_id):
    uberon_anat = gnomics.objects.tissue.Tissue(identifier = uberon_id, identifier_type = "UBERON ID", source = "Phenoscape Knowledgebase")
    
    print("\nGetting reference identifiers from UBERON identifier (%s) entity:" % uberon_id)
    start = timeit.timeit()
    references = get_references(uberon_anat)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for ref in references:
        for iden in ref.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()