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
#   Get references from Goodreads ID.
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
import json
import requests

#   MAIN
def main():
    goodreads_unit_tests()
    
#   Return Goodreads ID.
def get_goodreads_id(ref):
    goodreads_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["goodreads id", "goodreads", "goodreads identifier"]):
        if iden["identifier"] not in goodreads_array:
            goodreads_array.append(iden["identifier"])
        
    if goodreads_array:
        return goodreads_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["goodreads"] not in goodreads_array:
                goodreads_array.append(obj["goodreads"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["goodreads"], identifier_type="Goodreads ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["goodreads"] not in goodreads_array:
                goodreads_array.append(obj["goodreads"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["goodreads"], identifier_type="Goodreads ID", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["goodreads"] not in goodreads_array:
                goodreads_array.append(obj["goodreads"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["goodreads"], identifier_type="Goodreads ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["goodreads"] not in goodreads_array:
                goodreads_array.append(obj["goodreads"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["goodreads"], identifier_type="Goodreads ID", source="OpenLibrary", language=None)
                
    return goodreads_array
    
#   UNIT TESTS
def goodreads_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()