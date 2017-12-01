#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get SNOMED.
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
import gnomics.objects.gene
import gnomics.objects.pathway

#   Other imports.
import json
import requests

#   MAIN
def main():
    snomed_unit_tests("219700", "2394", "")

#   Get SNOMED-CT IDs.
def get_snomed(dis, user = None):
    snomed_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "snomed" or ident["identifier_type"].lower() == "snomed id" or ident["identifier_type"].lower() == "snomed identifier" or ident["identifier_type"].lower() == "snomed-ct id" or ident["identifier_type"].lower() == "snomed-ct" or ident["identifier_type"].lower() == "snomed-ct identifier":
            if ident["identifier"] not in snomed_array:
                snomed_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim"
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "snomedctIDs" in ext_links:
                        split_up = ext_links["snomedctIDs"].split(",")
                        for s in split_up:
                            if s not in snomed_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "SNOMED-CT ID", source = "OMIM")
                                snomed_array.append(s)
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
                if "SNOMEDCT" in split_xref[0]:
                    if split_xref[1] not in snomed_array:
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "SNOMED-CT ID",
                            'source': "Disease Ontology"
                        })
                        snomed_array.append(split_xref[1])             
    return snomed_array
    
#   UNIT TESTS
def snomed_unit_tests(omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting SNOMED-CT IDs from MIM Number (%s):" % omim_disease_id)
        for sno in get_snomed(omim_disease, user = user):
            print("- " + str(sno))
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting SNOMED-CT IDs from DOID (%s):" % doid)
        for sno in get_snomed(doid_dis):
            print("- " + str(sno))
    else:
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting SNOMED-CT IDs from DOID (%s):" % doid)
        for sno in get_snomed(doid_dis):
            print("- " + str(sno))

#   MAIN
if __name__ == "__main__": main()