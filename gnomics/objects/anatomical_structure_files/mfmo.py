#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   MFMO ID.
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
    mfmo_unit_tests()
    
# Return MFMO ID.
def get_mfmo_id(anat):
    mfmo_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "mfmo id" or ident["identifier_type"].lower() == "mfmo identifier":
            mfmo_array.append(ident["identifier"])
    return mfmo_array
    
#   UNIT TESTS
def ceph_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()