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
#   Convert to Ontology of Biological Attributes (OBA).
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
    oba_unit_tests()

#   Get OBA ID.
def get_oba_id(phen, user=None):
    oba_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["oba", "oba id", "oba identifier"]:
            if ident["identifier"] not in oba_id_array:
                oba_id_array.append(ident["identifier"])
    return oba_id_array
        
#   UNIT TESTS
def oba_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()