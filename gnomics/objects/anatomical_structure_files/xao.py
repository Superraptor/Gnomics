#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   XAO ID.
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
    xao_unit_tests()
    
# Return XAO ID.
def get_xao_id(anat):
    xao_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "xao id" or ident["identifier_type"].lower() == "xao identifier":
            xao_array.append(ident["identifier"])
    return xao_array
    
#   UNIT TESTS
def xao_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()