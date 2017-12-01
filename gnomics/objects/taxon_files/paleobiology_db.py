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
#   Get Paleobiology Database.
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
    paleo_unit_tests("1045608")
    
#   Get Paleobiology Database identifiers.
def get_paleobiology_db_id(taxon):
    paleo_array = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "paleobiology database" or ident["identifier_type"].lower() == "paleobiology database id" or ident["identifier_type"].lower() == "paleobiology database identifier":
            paleo_array.append(ident["identifier"])
    if paleo_array:
        return paleo_array
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "eol" or ident["identifier_type"].lower() == "eol id" or ident["identifier_type"].lower() == "eol identifier":
            tax_obj = gnomics.objects.taxon.Taxon.eol_page(taxon)
            for iden2 in tax_obj["taxonConcepts"]:
                if iden2["sourceIdentifier"].isdigit() and iden2["nameAccordingTo"] == "Paleobiology Database":
                    if iden2["sourceIdentifier"] not in paleo_array:
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=iden2["sourceIdentifier"], identifier_type="Paleobiology Database ID", language=None, source="EOL")
                        paleo_array.append(iden2["sourceIdentifier"])
    return paleo_array

#   UNIT TESTS
def paleo_unit_tests(eol_id):
    eol_taxon = gnomics.objects.taxon.Taxon(identifier=eol_id, identifier_type="EOL ID", language=None, source="EOL")
    print("Getting Paleobiology Database IDs from EOL ID (%s):" % eol_id)
    for paleo_db_id in get_paleobiology_db_id(eol_taxon):
        print("- %s" % paleo_db_id)
        
#   MAIN
if __name__ == "__main__": main()