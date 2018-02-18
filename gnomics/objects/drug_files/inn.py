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
#   Get INNs.
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
    inn_unit_tests()

#   Get INNs.
def get_inns(drug):
    inn_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["inn", "international nonproprietary name"]):
        if iden["identifier"] not in inn_array:
            inn_array.append(iden["identifier"])
    return inn_array

#   UNIT TESTS
def inn_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()