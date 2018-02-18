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
#   OCVDAE (Ontology of Cardiovascular Drug Adverse Events) ID.
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
    ocvdae_unit_tests()

#   Get OCVDAE ID.
def get_ocvdae_id(adverse_event, user = None):
    ocvdae_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["ocvdae id", "ocvdae identifier", "ocvdae"]):
        if iden["identifier"] not in ocvdae_array:
            ocvdae_array.append(iden["identifier"])
    return ocvdae_array

#   UNIT TESTS
def ocvdae_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()