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
#   ODNAE (Ontology of Drug Neuropathy Adverse Events) ID.
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
    odnae_unit_tests()

#   Get ODNAE ID.
def get_odnae_id(adverse_event, user = None):
    odnae_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["odnae id", "odnae identifier", "odnae"]):
        if iden["identifier"] not in odnae_array:
            odnae_array.append(iden["identifier"])
    return odnae_array

#   UNIT TESTS
def odnae_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()