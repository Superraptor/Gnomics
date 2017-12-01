#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get MeSH term.
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
import gnomics.objects.compound

#   Other imports.
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pubchempy as pubchem
import re
import requests

#   MAIN
def main():
    smiles_unit_tests("33419-42-0", "68005047")
	
#	Get MeSH UID.
def get_mesh_uid(com):
    mesh_uid_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "mesh uid" or ident["identifier_type"].lower() == "mesh unique identifier":
            mesh_uid_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas" or ident["identifier_type"].lower() == "cas rn":
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&retmode=xml&retmax=20&sort=relevance&term="
            r = requests.get(url + str(ident["identifier"]), headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            matches = re.findall(r'(?:<Id>)(?P<id>[0-9]{1,})(?:<\/Id>)', r.text, re.DOTALL)
            mesh_id_array = []
            for match in matches:
                if match not in mesh_id_array:
                    mesh_id_array.append(match)
            for match in mesh_id_array:
                request = Request("https://www.ncbi.nlm.nih.gov/mesh/" + match)
                try:
                    response = urlopen(request)
                    req_byte = response.read()
                    req_dec = req_byte.decode("utf8", "ignore")
                    new_matches = re.findall(r'<p>MeSH Unique ID: ([A-Z][0-9][0-9][0-9][0-9][0-9][0-9])<\/p>', str(req_dec))
                    for new_match in new_matches:
                        if new_match not in mesh_uid_array:
                            mesh_uid_array.append(new_match)
                            com.identifiers.append({
                                'identifier': new_match,
                                'language': None,
                                'identifier_type': "MeSH UID",
                                'source': "PubMed"
                            })
                except HTTPError as e:
                    print("Error code: ", e.code)
                except URLError as e:
                    print("Error code: ", e.reason)
    return mesh_uid_array
        
def get_mesh_name(com):
    mesh_name_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "mesh name" or ident["identifier_type"].lower() == "mesh term":
            mesh_name_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "mesh id" or ident["identifier_type"].lower() == "mesh identifier":
            url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&retmode=xml&id="
            r = requests.get(url + str(ident["identifier"]), headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            matches = re.findall(r'(?:[0-9]{1,}: )(?P<name>[A-Za-z0-9]{1,})(?:\n)', r.text, re.DOTALL)
            for match in matches:
                if match not in mesh_name_array:
                    com.identifiers.append({
                        'identifier': match,
                        'language': "en",
                        'identifier_type': "MeSH Term",
                        'source': "PubMed"
                    })
                    mesh_name_array.append(match)
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas" or ident["identifier_type"].lower() == "cas rn":
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&retmode=xml&retmax=20&sort=relevance&term="
            r = requests.get(url + str(ident["identifier"]), headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            matches = re.findall(r'(?:<Id>)(?P<id>[0-9]{1,})(?:<\/Id>)', r.text, re.DOTALL)
            for match in matches:
                url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&retmode=xml&id="
                r = requests.get(url + str(match), headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                submatches = re.findall(r'(?:[0-9]{1,}: )(?P<name>[A-Za-z0-9]{1,})(?:\n)', r.text, re.DOTALL)
                for submatch in submatches:
                    if submatch not in mesh_name_array:
                        com.identifiers.append({
                            'identifier': submatch,
                            'language': "en",
                            'identifier_type': "MeSH Term",
                            'source': "PubMed"
                        })
                        mesh_name_array.append(submatch)
    return mesh_name_array

#   UNIT TESTS
def smiles_unit_tests(cas_rn, mesh_id):
    cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
    print("Getting MeSH UID from CAS RN (%s):" % cas_rn)
    for mesh in get_mesh_id(cas_com):
        print("- " + str(mesh) + "\n")
    cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
    print("Getting MeSH term from CAS RN (%s):" % cas_rn)
    for mesh in get_mesh_name(cas_com):
        print("- " + str(mesh) + "\n")
    mesh_com = gnomics.objects.compound.Compound(identifier = str(mesh_id), identifier_type = "MeSH ID", source = "PubMed")
    print("Getting MeSH name from MeSH ID (%s):" % mesh_id)
    for mesh in get_mesh_name(mesh_com):
        print("- " + str(mesh) + "\n")

#   MAIN
if __name__ == "__main__": main()