#
#
#
#
#

#
#   IMPORT SOURCES:
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

#   Other imports.
from bioservices import *
import json
import requests

#   MAIN
def main():
    mesh_unit_tests("H00218", "219700", "2394")

#   Get MeSH.
def get_mesh(dis):
    mesh_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "mesh" or ident["identifier_type"].lower() == "mesh id" or ident["identifier_type"].lower() == "mesh identifier" or ident["identifier_type"].lower() == "mesh code":
            mesh_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg disease id":
            for mesh in gnomics.objects.disease.Disease.kegg_disease(dis)["DBLINKS"]["MeSH"].split(" "):
                if mesh not in mesh_array:
                    dis.identifiers.append(
                        {
                            'identifier': mesh,
                            'language': None,
                            'identifier_type': "MeSH",
                            'source': "MeSH"
                        }
                    )
                    mesh_array.append(mesh)
        elif ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim":
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
                        mesh_array.append( entry["DiseaseID"].split("MESH:")[1])
                        dis.identifiers.append({
                            'identifier':  entry["DiseaseID"].split("MESH:")[1],
                            'language': None,
                            'identifier_type': "MeSH",
                            'source': "MeSH"
                        })
        elif ident["identifier_type"].lower() == "doid" or ident["identifier_type"].lower() == "disease ontology id" or ident["identifier_type"].lower() == "disease ontology identifier":
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
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "MeSH",
                            'source': "MeSH"
                        })
                        mesh_array.append(split_xref[1])
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