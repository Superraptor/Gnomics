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
#   Get EC Number.
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
import gnomics.objects.enzyme

#   Other imports.

#   MAIN
def main():
    ec_unit_tests()
    
#   Get Enzyme Commission number.
def get_ec_number(enzyme):
    ec_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(enzyme.identifiers, ["ec", "ec number", "enzyme commission number"]):
        if iden["identifier"] not in ec_array:
            ec_array.append(iden["identifier"])
    return ec_array

#   UNIT TESTS
def ec_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()