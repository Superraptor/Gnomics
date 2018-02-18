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
#   Get MedDRA IDs.
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
    meddra_unit_tests()

#   Get MedDRA ID.
def get_meddra_id(dis):
    meddra_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["meddra", "meddra id", "meddra identifier", "meddra code"]:
            meddra_array.append(ident["identifier"])
            
    if meddra_array:
        return meddra_array
            
    ids_completed = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["ordo", "ordo id", "ordo identifier", "ordo code", "orphanet id", "ophanet identifier"]:
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
                        if "MedDRA:" in xref:
                            meddra_id = xref.split("MedDRA:")[1]
                            if meddra_id not in meddra_array:
                                meddra_array.append(meddra_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=meddra_id, identifier_type="MedDRA ID", source="OLS")

    return meddra_array

#   UNIT TESTS
def mesh_unit_tests(kegg_disease_id, omim_id, doid):
    kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
    print("Getting MeSH identifiers from KEGG Disease ID (%s):" % kegg_disease_id)
    for mesh in get_mesh(kegg_disease):
        print("- " + str(mesh))
        
    omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_id), identifier_type = "MIM Number", source = "OMIM")
    print("\nGetting MeSH identifiers from MIM number (%s):" % omim_id)
    for mesh in get_mesh(omim_disease):
        print("- " + str(mesh))
        
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    print("\nGetting MeSH identifiers from DOID (%s):" % doid)
    for mesh in get_mesh(doid_dis):
        print("- " + str(mesh))

#   MAIN
if __name__ == "__main__": main()