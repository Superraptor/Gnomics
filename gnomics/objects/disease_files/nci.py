#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get NCI Thesaurus Codes.
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
    nci_unit_tests("2394")

#   Get NCI thesaurus codes.
def get_nci_thesaurus_code(dis):
    nci_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "nci" or ident["identifier_type"].lower() == "nci id" or ident["identifier_type"].lower() == "nci identifier" or ident["identifier_type"].lower() == "nci code" or ident["identifier_type"].lower() == "nci thesaurus code":
            nci_array.append(ident["identifier"])
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
                if split_xref[0] == "NCI":
                    if split_xref[1] not in nci_array:
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "NCI Thesaurus Code",
                            'source': "Disease Ontology"
                        })
                        nci_array.append(split_xref[1])
    return nci_array

#   UNIT TESTS
def nci_unit_tests(doid):
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    print("\nGetting NCI Thesaurus Codes from DOID (%s):" % doid)
    for nci in get_nci_thesaurus_code(doid_dis):
        print("- " + str(nci))

#   MAIN
if __name__ == "__main__": main()