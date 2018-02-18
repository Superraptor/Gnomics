#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
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
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import json
import requests

#   MAIN
def main():
    ordo_unit_tests("2394")

#   Get ORDO codes.
def get_ordo(dis):
    ordo_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["ordo", "ordo id", "ordo identifier", "ordo code", "orphanet id", "ophanet identifier"]:
            ordo_array.append(ident["identifier"])
            
    if ordo_array:
        return ordo_array
            
    ids_completed = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
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
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], identifier_type="ORDO Code", language=None, source="Disease ontology", name=None)
                            ordo_array.append(split_xref[1])

    return ordo_array

#   UNIT TESTS
def ordo_unit_tests(doid):
    doid_dis = gnomics.objects.disease.Disease(identifier=str(doid), identifier_type="DOID", source="Disease Ontology")
    print("\nGetting ORDO Codes from DOID (%s):" % doid)
    for ordo in get_ordo(doid_dis):
        print("- " + str(ordo))
    
#   MAIN
if __name__ == "__main__": main()