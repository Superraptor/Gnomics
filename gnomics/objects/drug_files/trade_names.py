#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get various drug names.
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

#   Other imports.

#   MAIN
def main():
    trade_names_unit_tests()

#   Get trade names.
def get_trade_names(drug):
    trade_name_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "trade name":
            trade_name_array.append(ident["identifier"])
    return trade_name_array

#   UNIT TESTS
def trade_names_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()