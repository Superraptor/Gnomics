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
#   OAE (Ontology of Adverse Events) ID.
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
import timeit

#   MAIN
def main():
    oae_unit_tests()

#   Get OAE ID.
def get_oae_id(adverse_event, user = None):
    oae_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["oae id", "oae identifier", "oae"]):
        if iden["identifier"] not in oae_array:
            oae_array.append(iden["identifier"])
    return oae_array

#   UNIT TESTS
def oae_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()