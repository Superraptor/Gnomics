#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get ORDO (Orphanet Rare Disease Ontology) codes.
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
    ordo_unit_tests("2394")

#   Get ORDO codes.
def get_ordo(dis):
    ordo_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "ordo" or ident["identifier_type"].lower() == "ordo id" or ident["identifier_type"].lower() == "ordo identifier" or ident["identifier_type"].lower() == "ordo code":
            ordo_array.append(ident["identifier"])
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
                if split_xref[0] == "ORDO":
                    if split_xref[1] not in ordo_array:
                        dis.identifiers.append({
                            'identifier': split_xref[1],
                            'language': None,
                            'identifier_type': "ORDO Code",
                            'source': "Disease Ontology"
                        })
                        ordo_array.append(split_xref[1])
    return ordo_array

#   UNIT TESTS
def ordo_unit_tests(doid):
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    print("\nGetting ORDO Codes from DOID (%s):" % doid)
    for ordo in get_ordo(doid_dis):
        print("- " + str(ordo))

#   MAIN
if __name__ == "__main__": main()