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
import re
import requests
import timeit

#   MAIN
def main():
    smiles_unit_tests("33419-42-0", "68005047")
	
#   Get MeSH RN
def get_mesh_rn(com, user=None):
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["mesh rn", "mesh registry", "mesh registry number", "mesh number"]):
        if iden["identifier"] not in mesh_array:
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
    
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=mesh&retmode=xml&retmax=20&sort=relevance&term="
            
            r = requests.get(url + str(iden["identifier"]), headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong while utilizing the E-utilities.")

            else:
                matches = re.findall(r'(?:<Id>)(?P<id>[0-9]{1,})(?:<\/Id>)', r.text, re.DOTALL)

                for match in matches:
                    if match not in mesh_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = match, identifier_type = "MeSH Registry Number", language = None, source = "PubMed")
                        
                        mesh_array.append(match)
    
    return mesh_array
    
#	Get MeSH UID.
def get_mesh_uid(com, user=None):
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["mesh", "mesh uid", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]):
        if iden["identifier"] not in mesh_array:
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            mesh_id_array = get_mesh_rn(com)
            
            for match in mesh_id_array:
                request = Request("https://www.ncbi.nlm.nih.gov/mesh/" + match)
                try:
                    response = urlopen(request)
                    req_byte = response.read()
                    req_dec = req_byte.decode("utf8", "ignore")
                    new_matches = re.findall(r'<p>MeSH Unique ID: ([A-Z][0-9][0-9][0-9][0-9][0-9][0-9])<\/p>', str(req_dec))
                    
                    for new_match in new_matches:
                        if new_match not in mesh_array:
                            mesh_array.append(new_match)
                            gnomics.objects.compound.Compound.add_identifier(com, identifier=new_match, identifier_type="MeSH UID", source="PubMed", language=None)

                except HTTPError as e:
                    print("Error code: ", e.code)
                except URLError as e:
                    print("Error code: ", e.reason)
                except:
                    print("Some other error occurred while requesting MeSH page.")
                else:
                    break

    return mesh_array
        
# Get English MeSH Term.
def get_mesh_term_english(com, user=None):
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "en":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["mesh rn", "mesh registry", "mesh registry number", "mesh number"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&retmode=xml&id="
            r = requests.get(url + str(iden["identifier"]), headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong while utilizing the E-utilities.")
            else:
                matches = re.findall(r'(?:[0-9]{1,}: )(?P<name>[A-Za-z0-9]{1,})(?:\n)', r.text, re.DOTALL)
            
                for match in matches:
                    if match not in mesh_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier=match, identifier_type="MeSH Term", language="en", source="PubMed")
                        mesh_array.append(match)
                        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            mesh_id_array = get_mesh_rn(com)
            
            for mesh_id in mesh_id_array:
                url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=mesh&retmode=xml&id="
            
                r = requests.get(url + str(mesh_id), headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong while utilizing the E-utilities.")
                else:
                    submatches = re.findall(r'(?:[0-9]{1,}: )(?P<name>[A-Za-z0-9]{1,})(?:\n)', r.text, re.DOTALL)
                    for submatch in submatches:
                        if submatch not in mesh_array:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier=submatch, identifier_type="MeSH Term", language="en", source="PubMed")
                            mesh_array.append(submatch)
    
    return mesh_array

#   UNIT TESTS
def smiles_unit_tests(cas_rn, mesh_id):
        
    cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
    print("\nGetting MeSH UID from CAS RN (%s):" % cas_rn)
    start = timeit.timeit()
    mesh_array = get_mesh_uid(cas_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in mesh_array:
        print("\t- %s" % str(com))
        
    cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
    print("\nGetting MeSH RN from CAS RN (%s):" % cas_rn)
    start = timeit.timeit()
    mesh_array = get_mesh_rn(cas_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in mesh_array:
        print("\t- %s" % str(com))
        
    cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
    print("\nGetting MeSH term from CAS RN (%s):" % cas_rn)
    start = timeit.timeit()
    mesh_array = get_mesh_term_english(cas_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in mesh_array:
        print("\t- %s" % str(com))
    
    mesh_com = gnomics.objects.compound.Compound(identifier = str(mesh_id), identifier_type = "MeSH RN", source = "PubMed")
    print("\nGetting MeSH name from MeSH ID (%s):" % mesh_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_english(mesh_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in mesh_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()