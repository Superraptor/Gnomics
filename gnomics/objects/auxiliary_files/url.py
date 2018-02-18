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
#   Extract URLs.
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
import gnomics.objects.disease
import gnomics.objects.reference

#   Other imports.
from urlextract import URLExtract
import json
import pdfx
import re
import requests
import tempfile
import xml.etree.ElementTree

#   MAIN
def main():
    url_unit_tests("DOID:9074")

#   Get URls from string text.
def extract_urls(text):
    extractor = URLExtract()
    if type(text) is str:
        urls = extractor.find_urls(text)
        return urls
    elif type(text) is list:
        urls = []
        for x in text:
            url_x = extractor.find_urls(x)
            urls.extend(url_x)
        return urls
    else:
        print("Provided text type (%s) is not currently supported. Please supply either a list of string objects or a string object." % str(type(text)))
        
#   UNIT TESTS
def url_unit_tests(doid):
    
    # Given a disease, get the Wikipedia page.
    do_dis = gnomics.objects.disease.Disease(identifier = doid, identifier_type = "DOID", language = None, source = "Wikidata")
    
    text = gnomics.objects.disease.Disease.wikipedia_content(do_dis, language = "en")
    
#   MAIN
if __name__ == "__main__": main()