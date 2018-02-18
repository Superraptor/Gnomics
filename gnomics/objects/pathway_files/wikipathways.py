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
#   Get WikiPathways.
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
import gnomics.objects.pathway

#   Other imports.

#   MAIN
def main():
    wikipathways_unit_tests()
    
#   Get WikiPathways ID.
def get_wikipathways_id(path):
    wikipathways_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(path.identifiers, ["wikipathways", "wikipathways id", "wikipathways identifier"]):
        if iden["identifier"] not in wikipathways_array:
            wikipathways_array.append(iden["identifier"])
    return wikipathways_array

#   UNIT TESTS
def wikipathways_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()