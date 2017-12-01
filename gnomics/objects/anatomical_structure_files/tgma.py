#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   TGMA ID.
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
    tgma_unit_tests()
    
# Return TGMA ID.
def get_tgma_id(anat):
    tgma_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "tgma id" or ident["identifier_type"].lower() == "tgma identifier":
            tgma_array.append(ident["identifier"])
    return tgma_array
    
#   UNIT TESTS
def tgma_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()