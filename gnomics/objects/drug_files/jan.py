#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get JAN.
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
    jan_unit_tests()

#   Get JAN.
def get_jan(drug):
    jan_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "jan":
            jan_array.append(ident["identifier"])
    return jan_array

#   UNIT TESTS
def jan_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()