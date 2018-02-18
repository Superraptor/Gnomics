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
#   Get tissue from a variation.
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
import gnomics.objects.tissue
import gnomics.objects.variation

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    variation_tissue_unit_tests()

# Get tissues.
def get_tissues(variation):
    print("NOT FUNCTIONAL.")
            
#   UNIT TESTS
def variation_tissue_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()