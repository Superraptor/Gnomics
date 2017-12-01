#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get ChemSpider identifier.
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
import gnomics.objects.compound

#   Other imports.

#   MAIN
def main():
    schembl_unit_tests()

#   Get SCHEMBL ID.
def get_schembl_id(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "schembl" or ident["identifier_type"].lower() == "schembl id" or ident["identifier_type"].lower() == "schembl identifier":
            return ident["identifier"]

#   UNIT TESTS
def schembl_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()