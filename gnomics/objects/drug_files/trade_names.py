#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
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
import pubchempy as pubchem

#   MAIN
def main():
    trade_names_unit_tests()

#   Get trade names.
def get_trade_names(drug):
    trade_name_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["trade name"]):
        if iden["identifier"] not in trade_name_array:
            trade_name_array.append(iden["identifier"])
    return trade_name_array

#   UNIT TESTS
def trade_names_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()