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
#   Get MeSH identifiers.
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
    mesh_unit_tests("H00218", "219700", "2394")

#   Get MeSH.
def get_mesh(dis):
    mesh_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code"]:
            mesh_array.append(ident["identifier"])
            
    if mesh_array:
        return mesh_array
            
    ids_completed = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["kegg", "kegg id", "kegg identifier", "kegg disease id"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                for mesh in gnomics.objects.disease.Disease.kegg_disease(dis)["DBLINKS"]["MeSH"].split(" "):
                    if mesh not in mesh_array:
                        gnomics.objects.disease.Disease.add_identifier(dis, identifier=mesh, identifier_type="MeSH", source="MeSH", language=None, name=None)
                        mesh_array.append(mesh)

        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                server = "http://ctdbase.org/tools/batchQuery.go"
                ext = "?inputType=disease&inputTerms=OMIM:" + str(ident["identifier"]) + "&report=pathways_inferred&format=JSON"

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for entry in decoded:
                    if "MESH:" in entry["DiseaseID"]:
                        if entry["DiseaseID"].split("MESH:")[1] not in mesh_array:
                            mesh_array.append(entry["DiseaseID"].split("MESH:")[1])
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=entry["DiseaseID"].split("MESH:")[1], identifier_type="MeSH", source="MeSH", language=None, name=None)
                        
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
                    if split_xref[0] == "MESH":
                        if split_xref[1] not in mesh_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], identifier_type="MeSH", source="MeSH", language=None, name=None)
                            mesh_array.append(split_xref[1])
                        
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
                        if "MeSH:" in xref:
                            mesh_uid = xref.split("MeSH:")[1]
                            if mesh_uid not in mesh_array:
                                mesh_array.append(mesh_uid)
                                gnomics.objects.disease.Disease.add_identifier(phen, identifier=mesh_uid, identifier_type="MeSH UID", source="OLS")

    return mesh_array

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