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
#   Get SNOMED.
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
import gnomics.objects.gene
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import json
import requests

#   MAIN
def main():
    snomed_unit_tests("219700", "2394", "")

#   Get SNOMED-CT IDs.
def get_snomed(dis, user = None):
    snomed_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["snomed", "snomed id", "snomed identifier", "snomed-ct id", "snomed-ct", "snomed-ct identifier", "sctid"]:
            if ident["identifier"] not in snomed_array:
                snomed_array.append(ident["identifier"])
                
    if snomed_array:
        return snomed_array
                
    ids_completed = []
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "snomedctIDs" in ext_links:
                        split_up = ext_links["snomedctIDs"].split(",")
                        for s in split_up:
                            if s not in snomed_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=str(s), language=None, identifier_type="SNOMED-CT ID", source="OMIM")
                                snomed_array.append(s)
                                
        elif ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                server = "http://www.disease-ontology.org/api"
                ext = "/metadata/DOID%3A" + ident["identifier"]
                r = requests.get(server+ext)

                if not r.ok:
                    print("Something went wrong.")

                decoded = r.json()

                for xref in decoded["xrefs"]:
                    split_xref = xref.split(":")
                    if "SNOMEDCT" in split_xref[0]:
                        if split_xref[1] not in snomed_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], identifier_type="SNOMED-CT ID", source="Disease Ontology", language=None, name=None)
                            snomed_array.append(split_xref[1])
                        
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
                        if "SCTID:" in xref:
                            snomed_id = xref.split("SCTID:")[1]
                            if snomed_id not in snomed_array:
                                snomed_array.append(snomed_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=snomed_id, identifier_type="SCTID", source="OLS")
                                
                        elif "SNOMEDCT_US:" in xref:
                            snomed_id = xref.split("SNOMEDCT_US:")[1]
                            if snomed_id not in snomed_array:
                                snomed_array.append(snomed_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=snomed_id, identifier_type="SNOMED-CT ID", source="OLS")
                                
    return snomed_array
    
#   UNIT TESTS
def snomed_unit_tests(omim_disease_id, doid, omim_api_key=None):
    if omim_api_key is not None:
        
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")

        print("Getting SNOMED-CT IDs from MIM Number (%s):" % omim_disease_id)
        for sno in get_snomed(omim_disease, user = user):
            print("- " + str(sno))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting SNOMED-CT IDs from DOID (%s):" % doid)
        for sno in get_snomed(doid_dis):
            print("- " + str(sno))
            
    else:
        
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting SNOMED-CT IDs from DOID (%s):" % doid)
        for sno in get_snomed(doid_dis):
            print("- " + str(sno))

#   MAIN
if __name__ == "__main__": main()