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
#   Get ICD-10.
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
    icd10_unit_tests("H00218", "219700", "2394", "")

# Return ICD-10 disease object.
def get_icd_10_disease(dis):
    icd_10_disease_array = []
    icd_10_codes_array = []
    for dis_obj in dis.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() in ['icd-10', 'icd-10 code']:
                icd_10_disease_array.append(dis_obj['object'])
                icd_10_codes_array.append(dis_obj['object_identifier'])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["icd-10", "icd10", "icd-10 identifier", "icd-10 id", "icd-10 code"]:
            if ident["identifier"] not in icd_10_codes_array:
                disease = ICD10[ident["identifier"]]
                dis.disease_objects.append({
                    'object': disease,
                    'object_type': "ICD-10 code",
                    'object_identifier': ident["identifier"]
                })
                icd_10_disease_array.append(disease)
    return icd_10_disease_array
    
#   Get ICD-10 codes.
def get_icd10(dis, user = None):
    icd10_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            icd10_array.append(ident["identifier"])
            
    if icd10_array:
        return icd10_array
            
    ids_completed = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["kegg", "kegg disease", "kegg disease identifier", "kegg disease id"]:
            for new_id in gnomics.objects.disease.Disease.kegg_disease(dis)["DBLINKS"]["ICD-10"].split(" "):
                if new_id not in icd10_array:
                    gnomics.objects.disease.Disease.add_identifier(dis, identifier=new_id, identifier_type="ICD10 Code", source="ICD-10", language=None, name=None)
                    icd10_array.append(new_id)
                    
        elif user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "icd10cmIDs" in ext_links:
                        split_up = ext_links["icd10cmIDs"].split(",")
                        for s in split_up:
                            if s not in icd10_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=str(s), language=None, identifier_type="ICD-10-CM ID", source="OMIM")
                                icd10_array.append(s)
                                
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
                    if split_xref[0] == "ICD10CM":
                        if split_xref[1] not in icd10_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], language=None, name=None, identifier_type="ICD-10-CM ID", source="Disease Ontology")
                            icd10_array.append(split_xref[1])
                        
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
                        if "ICD-10:" in xref:
                            icd_id = xref.split("ICD-10:")[1]
                            if icd_id not in icd10_array:
                                icd10_array.append(icd_id)
                                gnomics.objects.disease.Disease.add_identifier(phen, identifier=icd_id, identifier_type="ICD-10 ID", source="OLS")
                        
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
                        if "ICD10:" in xref:
                            icd10_id = xref.split("ICD10:")[1]
                            if icd10_id not in icd10_array:
                                icd10_array.append(icd10_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = icd10_id, identifier_type = "ICD-10-CM Code", source = "OLS")

    return icd10_array

#   UNIT TESTS
def icd10_unit_tests(kegg_disease_id, omim_disease_id, doid, omim_api_key=None):
    if omim_api_key is not None:
        
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting ICD-10-CM IDs from MIM Number (%s):" % omim_disease_id)
        for icd in get_icd10(omim_disease, user = user):
            print("- " + str(icd))
    
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
        print("\nGetting ICD-10-CM IDs from KEGG Disease ID (%s):" % kegg_disease_id)
        for icd10 in get_icd10(kegg_disease):
            print("- " + str(icd10))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-10-CM IDs from DOID (%s):" % doid)
        for icd10 in get_icd10(doid_dis):
            print("- " + str(icd10))
    
    else:
        
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
        print("\nGetting ICD-10-CM IDs from KEGG Disease ID (%s):" % kegg_disease_id)
        for icd10 in get_icd10(kegg_disease):
            print("- " + str(icd10))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-10-CM IDs from DOID (%s):" % doid)
        for icd10 in get_icd10(doid_dis):
            print("- " + str(icd10))
        
#   MAIN
if __name__ == "__main__": main()