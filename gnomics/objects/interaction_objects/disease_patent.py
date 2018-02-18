#!/usr/bin/env python

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
#   Get patents from a disease.
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
import gnomics.objects.disease
import gnomics.objects.patent
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    disease_patent_unit_tests("D011658", "", "")

#   Get patents.
#
#   score
#   min-score
#   minEx-score
#   max-score
#   maxEx-score
#   frequency
#   min-frequency
#   minEx-frequency
#   max-frequency
#   maxEx-frequency
#   classification
#   title
#   abstract
#   description
#   claims
#   _page
#   _pageSize
#   _orderBy
#   _format
#   _callback
#   _metadata
def get_patents(disease, user=None, count_only=False):
    
    if count_only:
        patent_array = []
        for ident in disease.identifiers:
            if ident["identifier_type"].lower() in ["mesh uid"]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "patent/byDisease?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fsurechembl%2Findication%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for subitem in decoded["result"]["items"]:
                    if "_about" in subitem:
                        if "http://rdf.ebi.ac.uk/resource/surechembl/patent/" in subitem["_about"]:
                            temp_pat = gnomics.objects.patent.Patent(identifier = subitem["_about"].split("/patent/")[1], identifier_type = "Patent Number", source = "OpenPHACTS")
                            patent_array.append(temp_pat)

        return patent_array
    else:
        patent_dict = {}
        
        for ident in disease.identifiers:
            if ident["identifier_type"].lower() in ["mesh uid"]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "patent/byDisease/count?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fsurechembl%2Findication%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)
                patent_dict[ident["identifier"]] = decoded["result"]["primaryTopic"]["patent_count"]
            
        return patent_dict
        
    
#   UNIT TESTS
def disease_patent_unit_tests(mesh_uid, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    mesh_disease = gnomics.objects.disease.Disease(identifier = mesh_uid, identifier_type = "MeSH UID", source = "OpenPHACTS")
    
    print("\nGetting patent identifiers from MeSH UID (%s):" % mesh_uid)
    for pat in get_patents(mesh_disease, user = user):
        print(pat)
            
    start = timeit.timeit()
    all_pats = get_patents(mesh_disease, user = user, count_only = True)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
            
    print("\nGetting number of patent identifiers from MeSH UID (%s):" % mesh_uid)
    for pat in all_pats:
        print("- %s" % str(pat))
    
#   MAIN
if __name__ == "__main__": main()