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
#   Get ORC ID.
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
import gnomics.objects.person

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    orc_unit_tests()
    
#   Get ORCID.
def get_orcid(person):
    orcid_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(person.identifiers, ["orcid"]):
        if iden["identifier"] not in orcid_array:
            orcid_array.append(iden["identifier"])
    return orcid_array
    
#   UNIT TESTS
def orc_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()