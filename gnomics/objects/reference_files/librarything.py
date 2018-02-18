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
#   Get references from LibraryThing.
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
    librarything_unit_tests()
    
#   Return LibraryThing ID.
def get_librarything_id(ref):
    librarything_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["asin", "amazon standard identification number"]):
        if iden["identifier"] not in librarything_array:
            librarything_array.append(iden["identifier"])
        
    if librarything_array:
        return librarything_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["librarything"] not in librarything_array:
                librarything_array.append(obj["librarything"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["librarything"], identifier_type="LibraryThing ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["librarything"] not in librarything_array:
                librarything_array.append(obj["librarything"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["librarything"], identifier_type="LibraryThing ID", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["librarything"] not in librarything_array:
                librarything_array.append(obj["librarything"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["librarything"], identifier_type="LibraryThing ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["librarything"] not in librarything_array:
                librarything_array.append(obj["librarything"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["librarything"], identifier_type="LibraryThing ID", source="OpenLibrary", language=None)
                
    return librarything_array
    
#   UNIT TESTS
def librarything_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()