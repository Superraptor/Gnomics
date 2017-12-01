#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYTAXIZE
#           http://pytaxize.readthedocs.io/en/latest/
#

#
#   Get COL identifiers.
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
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   Other imports.
import pytaxize

#   MAIN
def main():
    accepted_unit_tests("208527")
    
#   Get accepted names.
def get_accepted_names(taxon):
    accepted_array = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "accepted name":
            accepted_array.append(ident["identifier"])
    if accepted_array:
        return accepted_array
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "tsn" or ident["identifier_type"].lower() == "itis tsn" or ident["identifier_type"].lower() == "itis taxonomic serial number" or ident["identifier_type"].lower() == "taxonomic serial number":
            res = pytaxize.getacceptednamesfromtsn(ident["identifier"])
            if res not in accepted_array:
                gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=str(res), identifier_type="Accepted Name", source="ITIS")
                accepted_array.append(res)
    return accepted_array

#   UNIT TESTS
def accepted_unit_tests(tsn):
    tsn_taxon = gnomics.objects.taxon.Taxon(identifier=tsn, identifier_type="TSN", language=None, source="COL")
    print("Getting accepted names from TSN (%s):" % tsn)
    for accept_name in get_accepted_names(tsn_taxon):
        print("- %s" % accept_name)
        
#   MAIN
if __name__ == "__main__": main()