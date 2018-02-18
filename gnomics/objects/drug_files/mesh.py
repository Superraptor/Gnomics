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
#   Get MeSH terms, unique identifiers.
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
import gnomics.objects.drug

#   Other imports.
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
import requests

#   MAIN
def main():
    mesh_unit_tests()
	
#	Get MeSH UID.
def get_mesh_uid(drug):
    mesh_uid_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(drug.identifiers, ["mesh", "mesh uid", "mesh unique id", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]):
        if iden["identifier"] not in mesh_uid_array:
            mesh_uid_array.append(iden["identifier"])
    return mesh_uid_array
        
def get_mesh_name(drug):
    mesh_name_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["mesh name", "mesh term"]:
            mesh_name_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["mesh id", "mesh identifier"]:
            url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&retmode=xml&id="
            r = requests.get(url + str(ident["identifier"]), headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()
            
            matches = re.findall(r'(?:[0-9]{1,}: )(?P<name>[A-Za-z0-9]{1,})(?:\n)', r.text, re.DOTALL)
            for match in matches:
                if match not in mesh_name_array:
                    drug.identifiers.append({
                        'identifier': match,
                        'language': "en",
                        'identifier_type': "MeSH Term",
                        'source': "PubMed"
                    })
                    mesh_name_array.append(match)
                    
    return mesh_name_array

#   UNIT TESTS
def mesh_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()