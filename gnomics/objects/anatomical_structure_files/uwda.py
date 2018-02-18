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
#   Get UWDA identifiers.
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
import gnomics.objects.auxiliary_files.identifier
import gnomics.objects.auxiliary_files.umls

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    uwda_unit_tests("21", "")

# Return UWDA ID.
def get_uwda_id(anat, user=None, source="umls"):
    
    uwda_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in uwda_array:
            uwda_array.append(iden["identifier"])
            
    if uwda_array:
        return uwda_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "UWDA", iden["identifier"])
            
            for x in found_array:
                if x not in uwda_array:
                    uwda_array.append(x)
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x, identifier_type="UWDA ID", language=None, source="UMLS Metathesaurus")

    return uwda_array
    
#   UNIT TESTS
def uwda_unit_tests(neu_id, umls_api_key):
            
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
        
    print("Getting UWDA IDs from NEU ID (%s):" % neu_id)
    for uwda in get_uwda_id(neu_anat, user = user):
        print("- " + str(uwda))
    
#   MAIN
if __name__ == "__main__": main()