#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get DOIDs (Disease Ontology IDs).
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

#   MAIN
def main():
    doid_unit_tests("219700", "2394", "")

#   Get DOIDs.
def get_doid(dis, user = None):
    doid_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "doid" or ident["identifier_type"].lower() == "disease ontology id" or ident["identifier_type"].lower() == "disease ontology identifier":
            if ident["identifier"] not in doid_array:
                doid_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim"
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "diseaseOntologyIDs" in ext_links:
                        split_up = ext_links["diseaseOntologyIDs"].split(",")
                        for s in split_up:
                            if s not in doid_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "Disease Ontology ID", source = "OMIM")
                                doid_array.append(s)
    return doid_array
    
#   UNIT TESTS
def doid_unit_tests(omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting Disease Ontology IDs from MIM Number (%s):" % omim_disease_id)
        for doid in get_doid(omim_disease, user = user):
            print("- " + str(doid))

#   MAIN
if __name__ == "__main__": main()