#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   ZFA ID.
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
    zfa_unit_tests()
    
# Return ZFA ID.
def get_zfa_id(anat):
    zfa_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "zfa id" or ident["identifier_type"].lower() == "zfa identifier":
            zfa_array.append(ident["identifier"])
    return zfa_array
    
#   UNIT TESTS
def zfa_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()