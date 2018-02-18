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
#   Get various KEGG compound identifiers.
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
    kegg_unit_tests()

#	Get KEGG drug identifier.
def get_kegg_drug_id(drug):
    kegg_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["kegg", "kegg id", "kegg identifier", "kegg accession", "kegg drug", "kegg drug id", "kegg drug identifier", "kegg drug accession"]):
        if iden["identifier"] not in kegg_array:
            kegg_array.append(iden["identifier"])  
    return kegg_array

#   UNIT TESTS
def kegg_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()