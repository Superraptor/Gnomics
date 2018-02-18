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
#   Get tissues from a transcript.
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
import gnomics.objects.transcript

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    transcript_tissue_unit_tests()

# Get tissue expression.
def get_tissue_expression(gene):
    print("NOT FUNCTIONAL.")
        
#   UNIT TESTS
def transcript_tissue_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()