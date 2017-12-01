#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   FBbt ID.
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
    fbbt_unit_tests()
    
# Return FBbt ID.
def get_fbbt_id(anat):
    fbbt_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "fbbt id" or ident["identifier_type"].lower() == "fbbt identifier":
            fbbt_array.append(ident["identifier"])
    return fbbt_array
    
#   UNIT TESTS
def fbbt_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()