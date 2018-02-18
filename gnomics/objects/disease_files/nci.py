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
    nci_unit_tests("2394")

#   Get NCI thesaurus codes.
def get_nci_thesaurus_code(dis):
    nci_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["nci", "nci id", "nci identifier", "nci code", "nci thesaurus code", "nci thesaurus id", "nci thesaurus identifier"]:
            nci_array.append(ident["identifier"])
            
    if nci_array:
        return nci_array
            
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
                    if split_xref[0] == "NCI":
                        if split_xref[1] not in nci_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier=split_xref[1], identifier_type="NCI Thesaurus Code", language=None, source="Disease Ontology", name=None)
                            nci_array.append(split_xref[1])
                        
        elif ident["identifier_type"].lower() in ["mondo id", "mondo identifier", "monarch disease ontology identifier", "monarch disease ontology id"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
            
                mondo_id = ident["identifier"]
                if ":" in mondo_id:
                    mondo_id = mondo_id.replace(":", "_")

                url = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/mondo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + mondo_id

                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    for xref in decoded["annotation"]["database_cross_reference"]:
                        if "NCIT:" in xref:
                            nci_id = xref.split("NCIT:")[1]
                            if nci_id not in nci_array:
                                nci_array.append(nci_id)
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier=nci_id, identifier_type="NCI Thesaurus Code", source="OLS")

    return nci_array

#   UNIT TESTS
def nci_unit_tests(doid):
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    print("\nGetting NCI Thesaurus Codes from DOID (%s):" % doid)
    for nci in get_nci_thesaurus_code(doid_dis):
        print("- " + str(nci))

#   MAIN
if __name__ == "__main__": main()