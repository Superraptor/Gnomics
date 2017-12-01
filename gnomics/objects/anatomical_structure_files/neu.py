#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   NEU ID.
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
    neu_unit_tests()
    
# Return NEU ID.
def get_neu_id(anat):
    neu_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "neu id" or ident["identifier_type"].lower() == "neu identifier":
            neu_array.append(ident["identifier"])
    return neu_array
    
#   UNIT TESTS
def neu_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()