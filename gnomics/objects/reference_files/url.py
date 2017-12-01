#
#
#
#
#

#
#   IMPORT SOURCES:
#       URLEXTRACT
#           https://pypi.python.org/pypi/urlextract
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
    print("NOT FUNCTIONAL.")

#   Get URls from string text.
def extract_urls(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    return urls
        
#   UNIT TESTS
def url_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()