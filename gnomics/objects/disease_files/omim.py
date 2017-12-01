#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get MIM numbers.
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
import json
import requests

#   MAIN
def main():
    omim_unit_tests("H00218", "2394")
    
# Return OMIM disease object.
def get_omim_disease(disease, user = None):
    omim_dis_array = []
    omim_id_array = []
    for dis_obj in disease.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() == 'omim' or dis_obj['object_type'].lower() == 'omim disease':
                omim_dis_array.append(dis_obj['object'])
                omim_id_array.append(dis_obj['identifier'])
    for ident in disease.identifiers:
        if (ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim") and user is not None:
            if ident["identifier"] not in omim_id_array:     
                base_url = "http://api.omim.org"
                ext = "/api/entry?format=jsonp&mimNumber=" + str(ident["identifier"]) + "&include=all"
                api_key_str = "&apiKey=" + user.omim_api_key
                r = requests.get(base_url+ext+api_key_str, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.rfind(")")
                except ValueError:
                    print("Input is not in a JSONP format.")
                    exit()
                res = str_r[l_index:r_index]
                decoded = json.loads(res)
                temp_obj = {
                    'object': decoded,
                    'object_type': "OMIM disease",
                    'identifier': ident["identifier"]
                }
                disease.disease_objects.append(temp_obj)
                omim_dis_array.append(temp_obj)
                omim_id_array.append(ident["identifier"])
        elif (ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim") and user is None:
            print("A user with a valid OMIM API key is necessary to retrieve an OMIM object.")
    return omim_dis_array

#   Get MIM numbers.
def get_omim(dis):
    omim_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim":
            if ident["identifier"] not in omim_array:
                omim_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "doid" or ident["identifier_type"].lower() == "disease ontology id" or ident["identifier_type"].lower() == "disease ontology identifier":
            server = "http://www.disease-ontology.org/api"
            ext = "/metadata/DOID:" + ident["identifier"]
            r = requests.get(server+ext)
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for xref in decoded["xrefs"]:
                split_xref = xref.split(":")
                if split_xref[0] == "OMIM":
                    if split_xref[1] not in omim_array:
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "MIM Number",
                            'source': "OMIM"
                        })
                        omim_array.append(split_xref[1])
        elif ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg disease id":
            for mim in gnomics.objects.disease.Disease.kegg_disease(dis)["DBLINKS"]["OMIM"].split(" "):
                if mim not in omim_array:
                    dis.identifiers.append({
                        'identifier': mim,
                        'language': None,
                        'identifier_type': "MIM Number",
                        'source': "OMIM"
                    })
                    omim_array.append(mim)
    return omim_array

#   UNIT TESTS
def omim_unit_tests(kegg_disease_id, doid):
    kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
    print("Getting MIM numbers from KEGG Disease ID (%s):" % kegg_disease_id)
    for mim in get_omim(kegg_disease):
        print("- " + str(mim))
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    print("\nGetting MIM numbers from DOID (%s):" % doid)
    for mim in get_omim(doid_dis):
        print("- " + str(mim))
    
#   MAIN
if __name__ == "__main__": main()