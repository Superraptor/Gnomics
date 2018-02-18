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
#   Get UMLS.
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
from gnomics.objects.disease_files.disgenet import get_disgenet
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
    umls_unit_tests("219700", "2394", "")

#   Get UMLS IDs.
def get_umls(dis, user=None):
    umls_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in umls_array:
                umls_array.append(ident["identifier"])
                
    if umls_array:
        return umls_array
                
    ids_completed = []
    for ident in dis.identifiers:
        
        if user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "umlsIDs" in ext_links:
                        split_up = ext_links["umlsIDs"].split(",")
                        for s in split_up:
                            if s not in umls_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=str(s), language=None, identifier_type="UMLS ID", source="OMIM")
                                umls_array.append(s)
                                
        elif ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                doid = ident["identifier"]
                if ":" in doid:
                    doid = doid.replace(":", "_")
                elif "DOID" not in doid:
                    doid = "DOID_" + doid

                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + doid
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()

                    found = False
                    for xref in decoded["annotation"]["database_cross_reference"]:
                        if "UMLS:" in xref:
                            umls_id = xref.split("UMLS:")[1]
                            if umls_id not in umls_array:
                                umls_array.append(umls_id)
                                gnomics.objects.disease.Disease.add_identifier(phen, identifier=umls_id, identifier_type="UMLS CUI", source="OLS")
                                found = True
                            
                    if found == False:
                        for iden, value in get_disgenet(dis).items():
                            for term in value:
                                if "umls" in term:
                                    if term["umls"]["value"] not in umls_array:
                                        um = term["umls"]["value"].split("/")[-1]
                                        umls_array.append(um)
                                        gnomics.objects.disease.Disease.add_identifier(
                                            dis, identifier=um, language=None, identifier_type="UMLS ID", source="DisGeNET"
                                        )

                        server = "http://www.disease-ontology.org/api"
                        ext = "/metadata/DOID:" + ident["identifier"]
                        
                        try:
                            r = requests.get(server+ext)
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()
                            for xref in decoded["xrefs"]:
                                split_xref = xref.split(":")
                                if split_xref[0] == "UMLS_CUI":
                                    if split_xref[1] not in umls_array:
                                        gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], identifier_type="UMLS ID", source="Disease Ontology", language=None, name=None)
                                        umls_array.append(split_xref[1])
                        except:
                            print("Something went wrong.")
        
        elif ident["identifier_type"].lower() in ["ordo", "ordo id", "ordo identifier", "ordo code", "orphanet id", "ophanet identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                ordo_id = ident["identifier"]
                if ":" in ordo_id:
                    ordo_id = ordo_id.replace(":", "_")

                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/ordo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + ordo_id
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    for xref in decoded["annotation"]["database_cross_reference"]:
                        if "UMLS:" in xref:
                            umls_id = xref.split("UMLS:")[1]
                            if umls_id not in umls_array:
                                umls_array.append(umls_id)
                                gnomics.objects.disease.Disease.add_identifier(phen, identifier=umls_id, identifier_type="UMLS CUI", source="OLS")
                        
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
                        if "UMLS:" in xref:
                            umls_cui = xref.split("UMLS:")[1]
                            if umls_cui not in umls_array:
                                umls_array.append(umls_cui)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=umls_cui, identifier_type="UMLS CUI", source="OLS")
        
    return umls_array
    
#   Get UMLS terms.
def get_umls_terms(dis):
    umls_term_array = []
    umls_id_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["umls term"]:
            if ident["identifier"] not in umls_term_array and ident["identifier"] not in umls_id_array:
                umls_term_array.append(ident["identifier"])
                umls_id_array.append(ident["identifier"])
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["name"] not in umls_term_array and ident["identifier"] not in umls_id_array:
                umls_term_array.append(ident["name"])
                umls_id_array.append(ident["identifier"])
            
    return umls_term_array
    
#   UNIT TESTS
def umls_unit_tests(omim_disease_id, doid, omim_api_key=None):
    if omim_api_key is not None:
        
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")

        print("Getting UMLS IDs from MIM Number (%s):" % omim_disease_id)
        for sno in get_umls(omim_disease, user = user):
            print("- " + str(sno))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting UMLS IDs from Disease Ontology ID (%s):" % doid)
        for iden in get_umls(doid_dis):
            print("- " + str(iden))
        
        print("\nGetting UMLS terms from Disease Ontology ID (%s):" % doid)
        for term in get_umls_terms(doid_dis):
            print("- " + str(term))

#   MAIN
if __name__ == "__main__": main()