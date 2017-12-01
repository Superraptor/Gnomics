#
#
#
#
#

#
#   IMPORT SOURCES:
#       ISBNLIB
#           https://pypi.python.org/pypi/isbnlib/3.7.2
#

#
#   Get references from Springer.
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
import isbnlib
import json
import requests

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   Validate ISBN-10.
def validate_isbn10(isbn10):
    return is_isbn10(isbn10)

#   Validate ISBN-13.
def validate_isbn13(isbn13):
    return is_isbn13(isbn13)

#   Get ISBN-10.
def get_isbn10(reference):
    isbn10_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "isbn10" or ident["identifier_type"].lower() == "isbn-10":
            isbn10_array.append(ident["identifier"])
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "isbn13" or ident["identifier_type"].lower() == "isbn-13":
            try:
                isbn10_temp = isbnlib.to_isbn10(ident["identifier"])
                isbn10_array.append()
            except:
                print("No corresponding ISBN-10 found.")
    return isbn10_array

#   Get ISBN-13.
def get_isbn13(reference):
    isbn13_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "isbn13" or ident["identifier_type"].lower() == "isbn-13":
            isbn13_array.append(ident["identifier"])
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "isbn10" or ident["identifier_type"].lower() == "isbn-10":
            try:
                isbn13_temp = isbnlib.to_isbn13(ident["identifier"])
                isbn13_array.append()
            except:
                print("No corresponding ISBN-13 found.")
    return isbn13_array
    
#   MAIN
if __name__ == "__main__": main()