#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

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
#   Convert to and from MeSH.
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
import gnomics.objects.adverse_event

#   Other imports.
import json
import requests
import time
import timeit

#   MAIN
def main():
    mesh_unit_tests("10051097", "", "")

#   Get MeSH UID.
def get_mesh_uid(adverse_event, user=None):
    mesh_array = []
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["mesh", "mesh uid", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]):
        if iden["identifier"] not in mesh_array:
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["mdr", "mdr code", "mdr id", "mdr identifier", "meddra", "meddra code", "meddra id", "meddra identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            if user.umls_api_key is not None:
    
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/MDR/" + str(iden["identifier"]) + "?targetSource=MSH"

                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    if not r.ok:
                        break
                    else:
                        items = json.loads(r.text)
                        json_data = items["result"]
                        
                        for er in json_data:
                            if er["ui"] not in mesh_array and er["ui"] != "NONE":
                                mesh_uid = er["ui"]
                                mesh_name = er["name"]
                                mesh_array.append(mesh_uid)
                                gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = mesh_uid, identifier_type = "MeSH UID", source = "UMLS", name = mesh_name)

                        if not json_data:
                            break
                            
            if user.ncbo_api_key is not None:
                    
                base = "http://data.bioontology.org/ontologies/"
                ext = "MEDDRA/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F" + str(iden["identifier"]) + "/mappings/?apikey=" + user.ncbo_api_key

                r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

                if not r.ok:
                    continue
                else:
                    decoded = json.loads(r.text)
                    for result in decoded:
                        for subresult in result["classes"]:
                            if "http://purl.bioontology.org/ontology/MESH" in subresult["@id"]:
                                mesh_uid = subresult["@id"].split("/MESH/")[1]
                                if mesh_uid not in mesh_array:
                                    mesh_array.append(mesh_uid)
                                    gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = mesh_uid, identifier_type = "MeSH UID", source = "NCBO BioPortal", name = subresult["prefLabel"])
                    
        elif user is None:
            print("A valid user with a valid UMLS API Key or valid NCBO BioPortal API Key is necessary for this transaction.")
        
    return mesh_array

#   UNIT TESTS
def mesh_unit_tests(meddra_id, umls_api_key, ncbo_api_key):
    user = User(umls_api_key = umls_api_key, ncbo_api_key = ncbo_api_key)
    
    meddra_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_id, identifier_type = "MedDRA ID", source = "UMLS")
    print("Getting MeSH UIDs from MedDRA ID (%s):" % meddra_id)
    start = timeit.timeit()
    mesh_array = get_mesh_uid(meddra_ae, user=user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- %s" % str(mesh))

#   MAIN
if __name__ == "__main__": main()