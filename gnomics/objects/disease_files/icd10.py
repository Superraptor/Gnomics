#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get ICD-10.
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
    icd10_unit_tests("H00218", "219700", "2394", "")

# Return ICD-10 disease object.
def get_icd_10_disease(dis):
    icd_10_disease_array = []
    icd_10_codes_array = []
    for dis_obj in dis.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() == 'icd-10' or dis_obj['object_type'].lower() == 'icd-10 code':
                icd_10_disease_array.append(dis_obj['object'])
                icd_10_codes_array.append(dis_obj['object_identifier'])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "icd-10" or ident["identifier_type"].lower() == "icd10" or ident["identifier_type"].lower() == "icd-10 identifier" or ident["identifier_type"].lower() == "icd-10 id" or ident["identifier_type"].lower() == "icd-10 code":
            if ident["identifier"] not in icd_10_codes_array:
                disease = ICD10[ident["identifier"]]
                dis.disease_objects.append({
                    'object': disease,
                    'object_type': "ICD-10 code",
                    'object_identifier': ident["identifier"]
                })
                icd_10_disease_array.append(disease)
    return icd_10_disease_array
    
#   Get ICD-10 codes.
def get_icd10(dis, user = None):
    icd10_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "icd10" or ident["identifier_type"].lower() == "icd10 code" or ident["identifier_type"].lower() == "icd10 id" or ident["identifier_type"].lower() == "icd10 identifier":
            icd10_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg disease" or ident["identifier_type"].lower() == "kegg disease identifier" or ident["identifier_type"].lower() == "kegg disease id":
            for new_id in gnomics.objects.disease.Disease.kegg_disease(dis)["DBLINKS"]["ICD-10"].split(" "):
                if new_id not in icd10_array:
                    dis.identifiers.append({
                            'identifier': new_id,
                            'language': None,
                            'identifier_type': "ICD10 Code",
                            'source': "ICD-10"
                        }
                    )
                    icd10_array.append(new_id)
        elif user is not None and (
            ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim"
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "icd10cmIDs" in ext_links:
                        split_up = ext_links["icd10cmIDs"].split(",")
                        for s in split_up:
                            if s not in icd10_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "ICD-10-CM ID", source = "OMIM")
                                icd10_array.append(s)
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
                if split_xref[0] == "ICD10CM":
                    if split_xref[1] not in icd10_array:
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "ICD-10-CM ID",
                            'source': "Disease Ontology"
                        })
                        icd10_array.append(split_xref[1])
            
    return icd10_array

#   UNIT TESTS
def icd10_unit_tests(kegg_disease_id, omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting ICD-10-CM IDs from MIM Number (%s):" % omim_disease_id)
        for icd in get_icd10(omim_disease, user = user):
            print("- " + str(icd))
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
        print("\nGetting ICD-10-CM IDs from KEGG Disease ID (%s):" % kegg_disease_id)
        for icd10 in get_icd10(kegg_disease):
            print("- " + str(icd10))
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-10-CM IDs from DOID (%s):" % doid)
        for icd10 in get_icd10(doid_dis):
            print("- " + str(icd10))
    else:
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG Disease ID", source = "KEGG")
        print("\nGetting ICD-10-CM IDs from KEGG Disease ID (%s):" % kegg_disease_id)
        for icd10 in get_icd10(kegg_disease):
            print("- " + str(icd10))
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting ICD-10-CM IDs from DOID (%s):" % doid)
        for icd10 in get_icd10(doid_dis):
            print("- " + str(icd10))
        
#   MAIN
if __name__ == "__main__": main()