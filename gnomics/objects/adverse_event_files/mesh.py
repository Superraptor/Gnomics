#
#
#
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

#   MAIN
def main():
    mesh_unit_tests("10051097", "")

#   Get MeSH UID.
def get_mesh_uid(adverse_event, user):
    mesh_array = []
    for ident in adverse_event.identifiers:
        if ident["identifier_type"].lower() == "mesh uid" or ident["identifier_type"].lower() == "mesh unique id" or ident["identifier_type"].lower() == "mesh unique identifier":
            mesh_array.append(ident["identifier"])
    if mesh_array:
        return mesh_array
    for ident in adverse_event.identifiers:
        if ident["identifier_type"].lower() == "meddra id" or ident["identifier_type"].lower() == "meddra identifier":
            umls_tgt = User.umls_tgt(user)
            page_num = 0
            base = "https://uts-ws.nlm.nih.gov/rest"
            ext = "/crosswalk/current/source/MDR/" + str(ident["identifier"]) + "?targetSource=MSH"
            while True:
                try:
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
                                mesh = er["ui"]
                                mesh_array.append(mesh)
                                gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = mesh, identifier_type = "MeSH UID", source = "UMLS")
                        if not json_data:
                            break
                except:
                    if not mesh_array:
                        base = "http://data.bioontology.org/ontologies/"
                        ext = "MEDDRA/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FMEDDRA%2F" + str(ident["identifier"]) + "/mappings/?apikey=" + user.ncbo_api_key
                        r = requests.get(base+ext, headers={"Content-Type": "application/json"})
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
                                            gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = mesh_uid, identifier_type = "MeSH UID", source = "NCBO BioPortal")
                    break
    return mesh_array

#   UNIT TESTS
def mesh_unit_tests(meddra_id, umls_api_key):
    print("NOT FUNCTIONAL.")
    user = User(umls_api_key = umls_api_key)
    meddra_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_id, identifier_type = "MedDRA ID", source = "UMLS")
    print("Getting MeSH UIDs from MedDRA ID (%s):" % meddra_id)
    for mesh in get_mesh_uid(meddra_ae, user):
        print("- %s" % str(mesh))

#   MAIN
if __name__ == "__main__": main()