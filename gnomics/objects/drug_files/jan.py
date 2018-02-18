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
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["jan", "japanese accepted name"]):
        if iden["identifier"] not in jan_array:
            jan_array.append(iden["identifier"])
    return jan_array

#   UNIT TESTS
def jan_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()