#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Common Anatomy Reference Ontology (CARO).
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
    caro_unit_tests()
    
# Return CARO ID.
def get_caro_id(anat):
    caro_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "caro id" or ident["identifier_type"].lower() == "caro identifier":
            caro_array.append(ident["identifier"])
    return caro_array
    
#   UNIT TESTS
def caro_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()