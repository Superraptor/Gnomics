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
#   Get SCHEMBL identifier.
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
import timeit

#   MAIN
def main():
    schembl_unit_tests()

#   Get SCHEMBL ID.
def get_schembl_id(com, user=None):
    schembl_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["schembl", "schembl id", "schembl identifier"]):
        if iden["identifier"] not in schembl_array:
            schembl_array.append(iden["identifier"])
    return schembl_array

#   UNIT TESTS
def schembl_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()