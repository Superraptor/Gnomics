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
#   Get NCI Thesaurus-related information.
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
import gnomics.objects.molecular_function

#   Other imports.
import json
import requests

#   MAIN
def main():
    nci_unit_tests()

#   Get NCI Thesaurus ID.
def get_nci_thesaurus_id(molec, user=None):
    molec_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(molec.identifiers, ["nci", "nci code", "nci id", "nci identifier", "nci thesaurus code", "nci thesaurus id", "nci thesaurus identifier", "ncit", "ncit code", "ncit id", "ncit identifier"]):
        if iden["identifier"] not in molec_array:
            molec_array.append(iden["identifier"])
    return molec_array

#   Get NCI Thesaurus synonyms.
def get_nci_synonyms(molec):
    nci_syn_array = []
    nci_id_array = []
    
    for ident in molec.identifiers:
        if ident["identifier_type"].lower() in ["nci", "nci code", "nci id", "nci identifier", "nci thesaurus code", "nci thesaurus id", "nci thesaurus identifier", "ncit", "ncit code", "ncit id", "ncit identifier"]:
            if ident["name"] not in nci_syn_array and ident["identifier"] not in nci_id_array:
                nci_syn_array.append(ident["name"])
                nci_id_array.append(ident["identifier"])
                
                nci_id = ident["identifier"]
                if ":" in nci_id:
                    nci_id = nci_id.replace(":", "_")
                
                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/ncit/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + nci_id
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    
                    if decoded["synonyms"]:
                        for syn in decoded["synonyms"]:
                            if syn not in nci_syn_array:
                                nci_syn_array.append(syn)
                                gnomics.objects.molecular_function.MolecularFunction.add_identifier(molec, identifier = ident["identifier"], identifier_type = "NCI Thesaurus ID", source = "OLS", name = syn)

    return nci_syn_array

#   UNIT TESTS
def nci_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()