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
#   Get DOIDs (Disease Ontology IDs).
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
    doid_unit_tests("219700", "2394", "6GhdwGFBTzaxHZ75MWOJ-w")

#   Get DOIDs.
def get_doid(dis, user = None):
    doid_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(dis.identifiers, ["disease ontology", "disease ontology id", "disease ontology identifier", "do id", "do identifier", "doid"]):
        if iden["identifier"] not in doid_array:
            doid_array.append(iden["identifier"])
                
    if doid_array:
        return doid_array
                
    ids_completed = []
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "diseaseOntologyIDs" in ext_links:
                        split_up = ext_links["diseaseOntologyIDs"].split(",")
                        for s in split_up:
                            if s not in doid_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "Disease Ontology ID", source = "OMIM")
                                doid_array.append(s)
                                
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
                        if "DOID:" in xref:
                            doid = xref.split("DOID:")[1]
                            if doid not in doid_array:
                                doid_array.append(doid)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = doid, identifier_type = "DOID", source = "OLS")
        
    return doid_array

#   Get DO terms.
#
#   From DOID, provides all diseases which belong to that
#   class.
def get_do_terms(dis):
    do_term_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["do term"]:
            if ident["identifier"] not in do_term_array:
                do_term_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            for iden, value in get_disgenet(dis).items():
                for term in value:
                    if "doTerm" in term:
                        if term["doTerm"]["value"] not in do_term_array:
                            do_term_array.append(term["doTerm"]["value"])
                            gnomics.objects.disease.Disease.add_identifier(
                                dis, identifier = term["doTerm"]["value"], language = "en", identifier_type = "DO Term", source = "DisGeNET"
                            )
    return do_term_array

#   Get DO Synonyms
def get_do_synonyms(dis):

    do_syn_array = []
    do_id_array = []
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "doid" or ident["identifier_type"].lower() == "disease ontology id" or ident["identifier_type"].lower() == "disease ontology identifier":
            if ident["name"] not in do_syn_array and ident["identifier"] not in do_id_array:
                do_syn_array.append(ident["name"])
                
                do_id = ident["identifier"]
                if ":" in do_id:
                    do_id = do_id.replace(":", "_")
                
                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + do_id

                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    if decoded["synonyms"]:
                        for syn in decoded["synonyms"]:
                            if syn not in do_syn_array:
                                do_syn_array.append(syn)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = ident["identifier"], identifier_type = "DOID", source = "OLS", name = syn)
     
    return do_syn_array
    
#   UNIT TESTS
def doid_unit_tests(omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting Disease Ontology IDs from MIM Number (%s):" % omim_disease_id)
        for sno in get_doid(omim_disease, user = user):
            print("- " + str(sno))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting DO terms from Disease Ontology ID (%s):" % doid)
        for term in get_do_terms(doid_dis):
            print("- " + str(term))

#   MAIN
if __name__ == "__main__": main()