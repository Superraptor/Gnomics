# https://developers.google.com/api-client-library/python/apis/books/v1

#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get references from Google Books.
#  
#   Google Scholar is currently not made available
#   by Google.
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
    google_unit_tests("0191078972")
    
#   Return Google Books ID.
def get_google_books_id(ref):
    google_books_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["google book", "google books", "google book id", "google book identifier", "google books id", "google books identifier"]):
        if iden["identifier"] not in google_books_array:
            google_books_array.append(iden["identifier"])
        
    if google_books_array:
        return google_books_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["google"] not in google_books_array:
                google_books_array.append(obj["google"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["google"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["google"] not in google_books_array:
                google_books_array.append(obj["google"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["google"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["google"] not in google_books_array:
                google_books_array.append(obj["google"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["google"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["google"] not in google_books_array:
                google_books_array.append(obj["google"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["google"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
                
    return google_books_array
    
#   Return a list of Google Books multiple
#   references.
def get_google_books_multiple_references(ref, verbose=False):
    google_obj_array = []
    
    for ref_obj in ref.reference_objects:
        if 'object_type' in ref_obj:
            if ref_obj['object_type'].lower() in ["google books", "google books object"]:
                google_obj_array.append(ref_obj['object'])
    
    if google_obj_array:
        return google_obj_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn10", "isbn-10", "isbn 10", "isbn13", "isbn-13", "isbn 13", "isbn"]):
        try:
            temp_obj = isbnlib.goom(iden["identifier"])
            gnomics.objects.reference.Reference.add_object(ref, obj=temp_obj, object_type="Google Books")
            google_obj_array.append(temp_obj)
            
        except isbnlib._exceptions.NotRecognizedServiceError:
            if verbose:
                print("An unrecognized service error occurred.")
        
    return google_obj_array
    
def google_books():
    print("NOT FUNCTIONAL.")
    
def google_scholar():
    print("NOT FUNCTIONAL.")
    
#   UNIT TESTS
def google_unit_tests(isbn):
    print("NOT FUNCTIONAL")
    
    print("Getting Google Books multiple references from ISBN (%s):" % isbn)
    isbn_ref = gnomics.objects.reference.Reference(identifier = isbn, identifier_type = "ISBN", language = None, source = "Google Books")
    for multiple_ref in get_google_books_multiple_references(isbn_ref):
        print(multiple_ref)

#   MAIN
if __name__ == "__main__": main()