#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

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
#   AERO (Adverse Event Reporting Ontology) ID.
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
import gnomics.objects.adverse_event

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    aero_unit_tests()

#   Get AERO ID.
def get_aero_id(adverse_event, user=None):
    aero_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["aero id", "aero identifier", "aero"]):
        if iden["identifier"] not in aero_array:
            aero_array.append(iden["identifier"])
    return aero_array

#   UNIT TESTS
def aero_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()