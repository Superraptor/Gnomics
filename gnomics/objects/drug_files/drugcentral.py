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
#   Get DrugCentral identifier.
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
    drugcentral_unit_tests()

#   Get DrugCentral ID.
def get_drugcentral_id(drug):
    drugcentral_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["drug central accession", "drugcentral accession", "drug central", "drugcentral", "drugcentral id", "drugcentral identifier"]):
        if iden["identifier"] not in drugcentral_array:
            drugcentral_array.append(iden["identifier"])
    return drugcentral_array

#   UNIT TESTS
def drugcentral_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()