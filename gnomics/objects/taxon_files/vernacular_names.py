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
#   Get vernacular names.
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

#   MAIN
def main():
    vernacular_name_unit_tests("1045608", )
    
def get_vernacular_names(taxon):
    vernacular_name_array = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "vernacular name" or ident["identifier_type"].lower() == "common name":
            vernacular_name_array.append(ident["identifier"])
    if vernacular_name_array:
        return vernacular_name_array
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "eol" or ident["identifier_type"].lower() == "eol id":
            eol_obj = gnomics.objects.taxon.Taxon.eol_page(taxon)
            for vernacular in eol_obj["vernacularNames"]:
                if vernacular["vernacularName"] not in vernacular_name_array:
                    vernacular_name_array.append(vernacular["vernacularName"])
                    gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = vernacular["vernacularName"], identifier_type = "Vernacular Name", language = vernacular["language"], source = "EOL")
    return vernacular_name_array

#   UNIT TESTS
def vernacular_name_unit_tests(eol_id, eol_api_key = None):
    print("Creating user...")
    user = User(eol_api_key = eol_api_key)
    print("User created successfully.\n")
    eol_tax = gnomics.objects.taxon.Taxon(identifier = str(eol_id), identifier_type = "EOL ID", source = "EOL")
    print("Getting EOL object from EOL ID (%s):" % eol_id)
    for iden in get_vernacular_names(eol_tax):
        print("- %s" % iden)
        
#   MAIN
if __name__ == "__main__": main()