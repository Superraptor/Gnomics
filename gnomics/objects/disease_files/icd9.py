#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get ICD-9-CM.
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
import requests

#   MAIN
def main():
    icd9_unit_tests("219700", "2394", "")

#   Get ICD-9-CM.
def get_icd9(dis, user = None):
    icd9_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "icd9" or ident["identifier_type"].lower() == "icd-9" or ident["identifier_type"].lower() == "icd-9-cm":
            if ident["identifier"] not in icd9_array:
                icd9_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim"
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "icd9cmIDs" in ext_links:
                        split_up = ext_links["icd9cmIDs"].split(",")
                        for s in split_up:
                            if s not in icd9_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "ICD-9-CM ID", source = "OMIM")
                                icd9_array.append(s)
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
                if split_xref[0] == "ICD9CM":
                    if split_xref[1] not in icd9_array:
                        dis.identifiers.append(
                            {
                                'identifier': split_xref[1],
                                'language': None,
                                'identifier_type': "ICD-9-CM ID",
                                'source': "Disease Ontology"
                            }
                        )
                        icd9_array.append(split_xref[1])
    return icd9_array
    
#   UNIT TESTS
def icd9_unit_tests(omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting ICD-9-CM IDs from MIM Number (%s):" % omim_disease_id)
        for icd in get_icd9(omim_disease, user = user):
            print("- " + str(icd))
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-9-CM IDs from DOID (%s):" % doid)
        for icd9 in get_icd9(doid_dis):
            print("- " + str(icd9))
    else:
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-9-CM IDs from DOID (%s):" % doid)
        for icd9 in get_icd9(doid_dis):
            print("- " + str(icd9))

#   MAIN
if __name__ == "__main__": main()