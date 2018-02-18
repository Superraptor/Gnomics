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
#   Get MeSH UIDs.
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    mesh_unit_tests("TS-0171", "", "")
    
#   Get MeSH UID.
def get_mesh_uid(tissue, user = None):
    mesh_array = []
    for ident in tissue.identifiers:
        if (ident["identifier_type"].lower() in ["mesh", "mesh uid", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]) and ident["identifier"] not in mesh_array:
            mesh_array.append(ident["identifier"])

    if mesh_array:
        return mesh_array
    
    ids_completed = []
    for ident in tissue.identifiers:
        if (ident["identifier_type"].lower() in ["caloha", "caloha id", "caloha identifier"]) and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            for xref in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user)["primaryTopic"]["hasDbXref"]:
                if "MESH" in xref:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref.split(":")[1], identifier_type = "MeSH UID", source = "OpenPHACTS")
                    mesh_array.append(xref.split(":")[1])
    
    return mesh_array

#   UNIT TESTS
def mesh_unit_tests(caloha_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    for mesh in get_mesh_uid(caloha_tiss, user = user):
        print("- %s" % mesh)
        
#   MAIN
if __name__ == "__main__": main()