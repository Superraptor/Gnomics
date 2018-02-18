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
#   Get ISSN.
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
    issn_unit_tests()

#   Get ISSN.
def get_issn(reference):
    issn_array = []
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["issn"]):
        if iden["identifier"] not in issn_array:
            issn_array.append(iden["identifier"])
            
    if issn_array:
        return issn_array
    
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() in ["doi", "digital object id", "digital object identifier"]:
            for article in gnomics.objects.reference.Reference.doi_object(reference, user=user):
                if "message" in article:
                    if "ISSN" in article["message"]:
                        if article["message"]["ISSN"] not in issn_array:
                            gnomics.objects.reference.Reference.add_identifier(reference, identifier=article["message"]["ISSN"], identifier_type="ISSN", language=None, source="CrossRef")
                            issn_array.append(article["message"]["ISSN"])
                
    return issn_array

#   UNIT TESTS
def issn_unit_tests():
    print("NOT FUNCTIONAL")
    
#   MAIN
if __name__ == "__main__": main()