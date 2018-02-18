#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
#

#
#   Get ICD-9-CM.
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

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import json
import requests

#   MAIN
def main():
    icd9_unit_tests("219700", "2394", "")

#   Get ICD-9-CM.
def get_icd9(dis, user = None):
    icd9_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in icd9_array:
                icd9_array.append(ident["identifier"])
                
    if icd9_array:
        return icd9_array
                
    ids_completed = []
    for ident in dis.identifiers:
        
        if user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "icd9cmIDs" in ext_links:
                        split_up = ext_links["icd9cmIDs"].split(",")
                        for s in split_up:
                            if s not in icd9_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "ICD-9-CM ID", source = "OMIM")
                                icd9_array.append(s)
                                
        elif ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                server = "http://www.disease-ontology.org/api"
                ext = "/metadata/DOID:" + ident["identifier"]
                r = requests.get(server+ext)

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for xref in decoded["xrefs"]:
                    split_xref = xref.split(":")
                    if split_xref[0] == "ICD9CM":
                        if split_xref[1] not in icd9_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier = split_xref[1], language = None, name = None, identifier_type = "ICD-9-CM ID", source = "Disease Ontology")
                            icd9_array.append(split_xref[1])
                        
        elif ident["identifier_type"].lower() in ["mondo id", "mondo identifier", "monarch disease ontology identifier", "monarch disease ontology id"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                mondo_id = ident["identifier"]
                if ":" in mondo_id:
                    mondo_id = mondo_id.replace(":", "_")

                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/mondo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + mondo_id
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    for xref in decoded["annotation"]["database_cross_reference"]:
                        if "ICD9:" in xref:
                            icd9_id = xref.split("ICD9:")[1]
                            if icd9_id not in icd9_array:
                                icd9_array.append(icd9_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = icd9_id, identifier_type = "ICD-9-CM Code", source = "OLS")
                        
    return icd9_array
    
#   UNIT TESTS
def icd9_unit_tests(omim_disease_id, doid, omim_api_key=None):
    
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting ICD-9-CM IDs from MIM Number (%s):" % omim_disease_id)
        for icd in get_icd9(omim_disease, user = user):
            print("- " + str(icd))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-9-CM IDs from DOID (%s):" % doid)
        for icd9 in get_icd9(doid_dis):
            print("- " + str(icd9))
    
    else:
        
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-9-CM IDs from DOID (%s):" % doid)
        for icd9 in get_icd9(doid_dis):
            print("- " + str(icd9))

#   MAIN
if __name__ == "__main__": main()