#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#
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
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["atc", "atc id", "atc identifier", "atc code", "atc classification", "atc classification code"]):
        if iden["identifier"] not in atc_array:
            atc_array.append(iden["identifier"])
    return atc_array

#   UNIT TESTS
def atc_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()