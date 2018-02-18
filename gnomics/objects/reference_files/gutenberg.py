#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get references from Project Gutenberg.
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
    gutenberg_unit_tests()
    
#   Return Project Gutenberg ID.
def get_project_gutenberg_id(ref):
    gutenberg_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["asin", "amazon standard identification number"]):
        if iden["identifier"] not in gutenberg_array:
            gutenberg_array.append(iden["identifier"])
        
    if gutenberg_array:
        return gutenberg_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["project_gutenberg"] not in gutenberg_array:
                gutenberg_array.append(obj["project_gutenberg"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["project_gutenberg"], identifier_type="Project Gutenberg ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["project_gutenberg"] not in gutenberg_array:
                gutenberg_array.append(obj["project_gutenberg"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["project_gutenberg"], identifier_type="Project Gutenberg ID", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["project_gutenberg"] not in gutenberg_array:
                gutenberg_array.append(obj["project_gutenberg"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["project_gutenberg"], identifier_type="Project Gutenberg ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["project_gutenberg"] not in gutenberg_array:
                gutenberg_array.append(obj["project_gutenberg"])
                gnomics.objects.reference.Reference.add_identifier(ref, identifier=obj["project_gutenberg"], identifier_type="Project Gutenberg ID", source="OpenLibrary", language=None)
                
    return gutenberg_array
    
#   UNIT TESTS
def gutenberg_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()