#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get USP.
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
import gnomics.objects.drug

#   MAIN
def main():
    usp_unit_tests()

#   Get USP.
def get_usp(com):
    usp_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "usp":
            usp_array.append(ident["identifier"])
    return usp_array

#   UNIT TESTS
def usp_unit_tests(chembl_id):
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()