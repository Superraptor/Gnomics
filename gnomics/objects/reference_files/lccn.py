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
#   Get references from Library of Congress Control Number.
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
    lccn_unit_tests()
    
#   Return Library of Congress Control Number (LCCN).
def get_lccn(ref):
    lccn_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        if iden["identifier"] not in lccn_array:
            lccn_array.append(iden["identifier"])
        
    if lccn_array:
        return lccn_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["lccn"] not in lccn_array:
                lccn_array.append(obj["lccn"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["lccn"], identifier_type="LCCN", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["lccn"] not in lccn_array:
                lccn_array.append(obj["lccn"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["lccn"], identifier_type="LCCN", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["lccn"] not in lccn_array:
                lccn_array.append(obj["lccn"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["lccn"], identifier_type="LCCN", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["lccn"] not in lccn_array:
                lccn_array.append(obj["lccn"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["lccn"], identifier_type="LCCN", source="OpenLibrary", language=None)
                
    return lccn_array
    
#   UNIT TESTS
def lccn_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()