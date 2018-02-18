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
#   Get proteins from tissue.
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
import gnomics.objects.protein
import gnomics.objects.tissue

#   Other imports.
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    tissue_protein_unit_tests("TS-0016", "", "")
     
#   Get proteins.
#
#   Parameters:
#   - evidence
#   - quality
#   - _page
#   - _pageSize
#   - _orderBy
#   - _format
#   - _callback
#   - _metadata
def get_proteins(tissue, user=None):
    prot_array = []
    
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() in ["caloha", "caloha identifier", "caloha id"] and user is not None:
            base = "https://beta.openphacts.org/2.1/"
            ext = "tissue/getProteins?uri=ftp%3A%2F%2Fftp.nextprot.org%2Fpub%2Fcurrent_release%2Fcontrolled_vocabularies%2Fcaloha.obo%23" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            for item in decoded["result"]["items"]:
                temp_prot = gnomics.objects.protein.Protein(identifier = item["protein"]["exactMatch"]["_about"].split("/uniprot/")[1], identifier_type = "UniProt Accession", source = "OpenPHACTS")
                prot_array.append(temp_prot)

    return prot_array
    
#   UNIT TESTS
def tissue_protein_unit_tests(caloha_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    print("\nGetting protein identifiers from CALOHA identifier (%s):" % caloha_id)
    for prot in get_proteins(caloha_tiss, user = user):
        for iden in prot.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()