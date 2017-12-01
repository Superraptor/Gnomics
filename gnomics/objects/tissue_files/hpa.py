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
#   HPA (Human Protein Atlas).
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests

#   MAIN
def main():
    hpa_unit_tests()
    
# Return HPA accession.
def get_hpa_accession(tissue):
    hpa_array = []
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "hpa id" or ident["identifier_type"].lower() == "hpa identifier" or ident["identifier_type"].lower() == "hpa identifier" or ident["identifier_type"].lower() == "the human protein atlas accession" or ident["identifier_type"].lower() == "human protein atlas accession" or ident["identifier_type"].lower() == "human protein atlas id":
            hpa_array.append(ident["identifier"])
    return hpa_array
    
#   UNIT TESTS
def hpa_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()