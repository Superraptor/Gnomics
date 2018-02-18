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
#   Get ISBN.
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
    isbn_unit_tests()
    
#   Return a probable ISBN from a list of words.
def get_probable_isbn(words):
    return isbnlib.isbn_from_words(words)
    
#   Return a list of ISBNs of editions related
#   to the provided ISBN.
def get_editions_from_isbn(ref, verbose=False):
    results_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn10", "isbn-10", "isbn 10", "isbn13", "isbn-13", "isbn 13", "isbn"]):
        try:
            results_array.append(isbnlib.editions(iden["identifier"], "wcat"))
        except isbnlib._exceptions.NotRecognizedServiceError:
            if verbose:
                print("An unrecognized service error occurred.")
            
        try:
            results_array.append(isbnlib.editions(iden["identifier"], "thingl"))
        except isbnlib._exceptions.NotRecognizedServiceError:
            if verbose:
                print("An unrecognized service error occurred.")
        
    return results_array
    
#   Return if canonical ISBN.
def is_canonical_isbn(isbnlike):
    return isbnlib.canonical(isbnlike)

#   Validate ISBN-10.
def validate_isbn10(isbn10):
    return isbnlib.is_isbn10(isbn10)

#   Validate ISBN-13.
def validate_isbn13(isbn13):
    return isbnlib.is_isbn13(isbn13)

#   Get ISBN-10.
def get_isbn10(reference, verbose=False):
    isbn10_array = []
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn10", "isbn-10", "isbn 10"]):
        if iden["identifier"] not in isbn10_array:
            isbn10_array.append(iden["identifier"])
            
    if isbn10_array:
        return isbn10_array
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn13", "isbn-13", "isbn 13"]):
        try:
            isbn10_temp = isbnlib.to_isbn10(iden["identifier"])
            if isbn10_temp not in isbn10_array:
                isbn10_array.append(isbn10_temp)
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=isbn10_temp, identifier_type="ISBN-10", source="ISBNlib", language=None)
        except:
            if verbose:
                print("No corresponding ISBN-10 found.")
            
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_10"] not in isbn10_array:
                isbn10_array.append(obj["isbn_10"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_10"], identifier_type="ISBN-10", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_10"] not in isbn10_array:
                isbn10_array.append(obj["isbn_10"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_10"], identifier_type="ISBN-10", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_10"] not in isbn10_array:
                isbn10_array.append(obj["isbn_10"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_10"], identifier_type="ISBN-10", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_10"] not in isbn10_array:
                isbn10_array.append(obj["isbn_10"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_10"], identifier_type="ISBN-10", source="OpenLibrary", language=None)
                
    return isbn10_array

#   Get ISBN-13.
def get_isbn13(reference, verbose=False):
    isbn13_array = []
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn13", "isbn-13", "isbn 13"]):
        if iden["identifier"] not in isbn13_array:
            isbn13_array.append(iden["identifier"])
            
    if isbn13_array:
        return isbn13_array
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn10", "isbn-10", "isbn 10"]):
        try:
            isbn13_temp = isbnlib.to_isbn13(iden["identifier"])
            if isbn13_temp not in isbn13_array:
                isbn13_array.append(isbn13_temp)
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=isbn13_temp, identifier_type="ISBN-13", source="ISBNlib", language=None)
        except:
            if verbose:
                print("No corresponding ISBN-13 found.")
            
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_13"] not in isbn13_array:
                isbn13_array.append(obj["isbn_13"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_13"], identifier_type="ISBN-13", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_13"] not in isbn13_array:
                isbn13_array.append(obj["isbn_13"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_13"], identifier_type="ISBN-13", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_13"] not in isbn13_array:
                isbn13_array.append(obj["isbn_13"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_13"], identifier_type="ISBN-13", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["isbn_13"] not in isbn13_array:
                isbn13_array.append(obj["isbn_13"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["isbn_13"], identifier_type="ISBN-13", source="OpenLibrary", language=None)
                
    return isbn13_array
    
#   UNIT TESTS
def isbn_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()