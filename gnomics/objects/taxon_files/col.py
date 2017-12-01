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
#   Get COL (Catalogue of Life) identifiers.
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
    col_unit_tests("Poa annua", "1045608")
    
#   Get COL identifier.
def get_col_id(taxon):
    col_array = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "col" or ident["identifier_type"].lower() == "col id":
            col_array.append(ident["identifier"])
    if col_array:
        return col_array
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "scientific name" or ident["identifier_type"].lower() == "binomial name" or ident["identifier_type"].lower() == "binomial nomenclature" or ident["identifier_type"].lower() == "binomen" or ident["identifier_type"].lower() == "latin name":
            res = pytaxize.Ids(ident["identifier"], db="col")
            for x in res.get_colid():
                if x not in col_array:
                    gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=str(x), identifier_type="COL ID", source="COL")
                    col_array.append(x)              
        elif ident["identifier_type"].lower() == "eol" or ident["identifier_type"].lower() == "eol id" or ident["identifier_type"].lower() == "eol identifier":
            tax_obj = gnomics.objects.taxon.Taxon.eol_page(taxon)
            for iden2 in tax_obj["taxonConcepts"]:
                if iden2["sourceIdentifier"].isdigit() and iden2["nameAccordingTo"] == "Integrated Taxonomic Information System (ITIS)":
                    if iden2["sourceIdentifier"] not in col_array:
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=iden2["sourceIdentifier"], identifier_type="COL ID", language=None, source="EOL")
                        col_array.append(iden2["sourceIdentifier"])         
    return col_array

#   UNIT TESTS
def col_unit_tests(sci_name, eol_id):
    eol_taxon = gnomics.objects.taxon.Taxon(identifier=eol_id, identifier_type="EOL ID", language=None, source="EOL")
    print("Getting COL IDs from EOL ID (%s):" % eol_id)
    for col_id in get_col_id(eol_taxon):
        print("- %s" % col_id)
    sci_taxon = gnomics.objects.taxon.Taxon(identifier=sci_name, identifier_type="Scientific Name", language="Latin", source="COL")
    print("\nGetting COL IDs from scientific name (%s):" % sci_name)
    for col_id in get_col_id(sci_taxon):
        print("- %s" % col_id)
        
#   MAIN
if __name__ == "__main__": main()