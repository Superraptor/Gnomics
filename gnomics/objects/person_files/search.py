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
#   Search for people.
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
import gnomics.objects.person

#   Other imports.
import json
import orcid
import requests
import time
import timeit

#   MAIN
def main():
    search_unit_tests("eric kandel")
    
#   Search ORCID API.
def orcid_search(query):
    api = orcid.SearchAPI(sandbox=True)
    search_results = api.search_public(query)
    print(search_results)
    
#   Search PubMed for people.
def pubmed_search(query):
    print("NOT FUNCTIONAL.")
    
#   Search Wikipedia for people.
def wikipedia_search(query):
    print("NOT FUNCTIONAL.")
    
#   UNIT TESTS
def search_unit_tests(query):
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()