#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get diseases from a compound.
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
import gnomics.objects.compound
import gnomics.objects.disease

#   Other imports.
import pubchempy as pubchem
import json
import requests

#   MAIN
def main():
    disease_unit_tests("36462")
    
# Get diseases.
def get_diseases(com):
    dis_array = []
    dis_id_array = []
    for related_obj in com.related_objects:
        if 'object_type' in related_obj:
            if related_obj['object_type'].lower() == "disease":
                any_in = 0
                for iden in related_obj['object'].identifiers:
                    if iden not in dis_array:
                        dis_id_array.append(iden)
                        dis_array.append(related_obj["object"])
                    else:
                        any_in = any_in + 1
                if any_in == 0:
                    gen_array.append(related_obj["object"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/MIMID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                print("URL not found.")
            else:
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.index(")")
                except ValueError:
                    print("Input is not in a JSONP format.")
                    exit()
                res = str_r[l_index:r_index]
                decoded = json.loads(res)
                for result in decoded["InformationList"]["Information"]:
                    dises = result["MIMID"]
                    for dis in dises:
                        if dis not in dis_array:
                            temp_dis = gnomics.objects.disease.Disease(identifier = dis, language = None, identifier_type = "MIM Number", source = "OMIM")
                            dis_array.append(temp_dis)
                            com.related_objects.append({
                                "object": temp_dis,
                                "object_type": "Disease",
                                "identifier": dis,
                                "source": "OMIM"
                            })
                            dis_id_array.append(dis)
    return dis_array

#   UNIT TESTS
def disease_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting diseases from PubChem CID (%s):" % pubchem_cid)
    for dis in get_diseases(pubchem_com):
        for iden in dis.identifiers:
            print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    
#   MAIN
if __name__ == "__main__": main()