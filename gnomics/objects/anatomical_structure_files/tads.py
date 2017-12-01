#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   TADS ID.
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
    tads_unit_tests()
    
# Return TADS ID.
def get_tads_id(anat):
    tads_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "tads id" or ident["identifier_type"].lower() == "tads identifier":
            tads_array.append(ident["identifier"])
    return tads_array
    
#   UNIT TESTS
def tads_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()