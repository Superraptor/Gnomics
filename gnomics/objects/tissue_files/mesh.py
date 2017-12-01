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
        if ident["identifier_type"].lower() == "mesh" or ident["identifier_type"].lower() == "mesh uid" or ident["identifier_type"].lower() == "mesh unique identifier":
            mesh_array.append(ident["identifier"])
    if mesh_array:
        return mesh_array
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "caloha" or ident["identifier_type"].lower() == "caloha id" or ident["identifier_type"].lower() == "caloha identifier":
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