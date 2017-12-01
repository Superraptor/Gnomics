#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   EHDAA2 (Human Developmental Anatomy Ontology, Abstract V2).
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
    ehdaa2_unit_tests()
    
# Return EHDAA2 ID.
def get_ehdaa2_id(anat):
    ehdaa2_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "ehdaa2 id" or ident["identifier_type"].lower() == "ehdaa2 identifier":
            ehdaa2_array.append(ident["identifier"])
    return ehdaa2_array
    
#   UNIT TESTS
def ehdaa2_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()