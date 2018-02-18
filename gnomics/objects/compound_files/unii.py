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
#   Get UNII.
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
    unii_unit_tests()

#   Get UNII.
def get_unii(com, user=None):
    unii_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["unii"]):
        if iden["identifier"] not in unii_array:
            unii_array.append(iden["identifier"])
    return unii_array

#   UNIT TESTS
def unii_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()