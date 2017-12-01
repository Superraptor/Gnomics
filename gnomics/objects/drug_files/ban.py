#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get BAN.
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
    ban_unit_tests()

#   Get BAN.
def get_ban(com):
    ban_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "ban":
            ban_array.append(ident["identifier"])
    return ban_array

#   UNIT TESTS
def ban_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()