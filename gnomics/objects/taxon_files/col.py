#!/usr/bin/env python

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
import pytaxize
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    col_unit_tests("Poa annua", "1045608")
    
#   Get COL identifier.
def get_col_id(taxon):
    
    col_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["catalogue of life", "catalogue of life id", "catalogue of life identifier", "col", "col id", "col identifier"]:
            col_array.append(ident["identifier"])
            
    if col_array:
        return col_array
    
    ids_completed = []
    for ident in taxon.identifiers:
        if (ident["identifier_type"].lower() in ["scientific name", "binomial name", "binomial nomenclature", "binomen", "latin name"]) and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            res = pytaxize.Ids(ident["identifier"], db="col")
            for x in res.get_colid():
                if x not in col_array:
                    gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=str(x), identifier_type="COL ID", source="COL")
                    col_array.append(x)
                    
        elif ident["identifier_type"].lower() in ["eol", "eol id", "eol identifier"]:
            ids_completed.append(ident["identifier"])
            tax_obj = gnomics.objects.taxon.Taxon.eol_page(taxon)
            for obj in tax_obj:
                for iden2 in obj["taxonConcepts"]:
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