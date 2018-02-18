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
#   Convert to Combined Phenotype Ontology (UPHENO).
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
import gnomics.objects.phenotype

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    upheno_unit_tests()

#   Get UPHENO ID.
def get_upheno_id(phen, user=None):
    upheno_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["upheno", "upheno id", "upheno identifier"]:
            if ident["identifier"] not in upheno_id_array:
                upheno_id_array.append(ident["identifier"])
    return upheno_id_array
        
#   UNIT TESTS
def upheno_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()