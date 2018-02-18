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
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["usp", "u.s. pharmacopeia", "united states pharmacopeia", "us pharmacopeia"]):
        if iden["identifier"] not in usp_array:
            usp_array.append(iden["identifier"])
    return usp_array

#   UNIT TESTS
def usp_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()