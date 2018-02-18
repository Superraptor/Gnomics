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
#   Convert to Vertebrate Trait Ontology (VT).
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
    vt_unit_tests()

#   Get VT ID.
def get_vt_id(phen, user=None):
    vt_id_array = []
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["vt", "vt id", "vt identifier"]:
            if ident["identifier"] not in vt_id_array:
                vt_id_array.append(ident["identifier"])
    return vt_id_array
        
#   UNIT TESTS
def vt_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()