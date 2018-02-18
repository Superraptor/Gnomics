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
#   OVAE (Ontology of Vaccine Adverse Events) ID.
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
    ovae_unit_tests()

#   Get OVAE ID.
def get_ovae_id(adverse_event, user = None):
    ovae_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["ovae id", "ovae identifier", "ovae"]):
        if iden["identifier"] not in ovae_array:
            ovae_array.append(iden["identifier"])
    return ovae_array

#   UNIT TESTS
def ovae_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()