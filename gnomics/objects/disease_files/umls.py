#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get UMLS.
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
    umls_unit_tests("219700", "2394", "6GhdwGFBTzaxHZ75MWOJ-w")

#   Get UMLS IDs.
def get_umls(dis, user = None):
    umls_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "umls" or ident["identifier_type"].lower() == "umls id" or ident["identifier_type"].lower() == "umls identifier":
            if ident["identifier"] not in umls_array:
                umls_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim"
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "umlsIDs" in ext_links:
                        split_up = ext_links["umlsIDs"].split(",")
                        for s in split_up:
                            if s not in umls_array:
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = str(s), language = None, identifier_type = "UMLS ID", source = "OMIM")
                                umls_array.append(s)
    return umls_array
    
#   Get UMLS terms.
def get_umls_terms(dis):
    umls_term_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "umls term":
            if ident["identifier"] not in do_term_array:
                umls_term_array.append(ident["identifier"])
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "doid" or ident["identifier_type"].lower() == "disease ontology id" or ident["identifier_type"].lower() == "disease ontology identifier":
            for iden, value in get_disgenet(dis).items():
                for term in value:
                    if "umlsTerm" in term:
                        if term["umlsTerm"]["value"] not in umls_term_array:
                            umls_term_array.append(term["umlsTerm"]["value"])
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier = term["umlsTerm"]["value"], language = term["umlsTerm"]["xml:lang"], identifier_type = "UMLS Term", source = "DisGeNET")
    return umls_term_array
    
#   UNIT TESTS
def umls_unit_tests(omim_disease_id, doid, omim_api_key = None):
    if omim_api_key is not None:
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting UMLS IDs from MIM Number (%s):" % omim_disease_id)
        for sno in get_umls(omim_disease, user = user):
            print("- " + str(sno))
        print("\nGetting UMLS terms from Disease Ontology ID (%s):" % doid)
        for term in get_umls_terms(doid_dis):
            print("- " + str(term))

#   MAIN
if __name__ == "__main__": main()