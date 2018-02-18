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
#   Get USAN.
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
    usan_unit_tests()

#   Get USAN.
def get_usan(drug):
    usan_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["usan", "us adopted name", "u.s. adopted name", "united states adopted name"]):
        if iden["identifier"] not in usan_array:
            usan_array.append(iden["identifier"])
    return usan_array

#   UNIT TESTS
def usan_unit_tests(chembl_id):
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()