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
#   Get references from Amazon.
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
    amazon_unit_tests()
    
#   Return Amazon Standard Identification Numbers (ASINs).
def get_asin(ref):
    asin_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["asin", "amazon standard identification number"]):
        if iden["identifier"] not in asin_array:
            asin_array.append(iden["identifier"])
        
    if asin_array:
        return asin_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["amazon"] not in asin_array:
                asin_array.append(obj["amazon"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["amazon"], identifier_type="ASIN", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["amazon"] not in asin_array:
                asin_array.append(obj["amazon"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["amazon"], identifier_type="ASIN", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["amazon"] not in asin_array:
                asin_array.append(obj["amazon"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["amazon"], identifier_type="ASIN", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["amazon"] not in asin_array:
                asin_array.append(obj["amazon"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["amazon"], identifier_type="ASIN", source="OpenLibrary", language=None)
                
    return asin_array
    
#   UNIT TESTS
def amazon_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()