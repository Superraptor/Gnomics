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
#   Perform identifier operations.
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    identifier_unit_tests()
    
#   Check if identifier type in identifier array.
#
#   TRUE = there is at least one identifier match.
#   FALSE = there are no identifier matches.
#
#   Both inputs should be arrays.
def matches_identifier(identifier_array, identifier_type_array):
    return not set([d["identifier_type"].lower() for d in identifier_array if "identifier_type" in d]).isdisjoint(identifier_type_array)

#   Filter identifiers by type.
def filter_identifiers(identifier_array, identifier_type_array):
    return list(filter(lambda d: d['identifier_type'].lower() in identifier_type_array, identifier_array))
    
#   UNIT TESTS
def identifier_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()