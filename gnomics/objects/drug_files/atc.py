#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get ATC codes.
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
import gnomics.objects.drug

#   MAIN
def main():
    atc_unit_tests()

#   Get ATC codes.
def get_atc_codes(drug):
    atc_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "atc" or ident["identifier_type"].lower() == "atc code" or ident["identifier_type"].lower() == "atc classification":
            atc_array.append(ident["identifier"])
    return atc_array

#   UNIT TESTS
def atc_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()