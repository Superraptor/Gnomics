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
#   Get patents from reference.
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
import gnomics.objects.patent
import gnomics.objects.reference

#   Other imports.
import json
import requests

#   MAIN
def main():
    reference_patent_unit_tests("CHEMBL3638895")
     
#   Get patents.
def get_patents(reference, user = None):
    patent_array = []
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            for item in gnomics.objects.reference.Reference.chembl_document(reference):
                if "patent_id" in item:
                    temp_patent = gnomics.objects.patent.Patent(identifier = item["patent_id"], identifier_type = "Patent ID", source = "ChEMBL")
                    patent_array.append(temp_patent)
    return patent_array
    
#   UNIT TESTS
def reference_patent_unit_tests(chembl_id):
    chembl_ref = gnomics.objects.reference.Reference(identifier = chembl_id, identifier_type = "ChEMBL ID", language = None, source = "ChEMBL")
    print("Getting patent identifiers from ChEMBL ID (%s):" % chembl_id)
    for pat in get_patents(chembl_ref):
        for iden in pat.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()