#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Anatomical Entity Ontology (AEO).
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    aeo_unit_tests()
    
# Return AEO ID.
def get_aeo_id(anat, user = None):
    aeo_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "aeo id" or ident["identifier_type"].lower() == "aeo identifier":
            aeo_array.append(ident["identifier"])
    return aeo_array
    
#   UNIT TESTS
def aeo_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()