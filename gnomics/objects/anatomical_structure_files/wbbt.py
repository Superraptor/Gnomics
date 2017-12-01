#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   WBBT ID.
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
    wbbt_unit_tests()
    
# Return WBBT ID.
def get_wbbt_id(anat):
    wbbt_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wbbt id" or ident["identifier_type"].lower() == "wbbt identifier":
            wbbt_array.append(ident["identifier"])
    return wbbt_array
    
#   UNIT TESTS
def wbbt_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()