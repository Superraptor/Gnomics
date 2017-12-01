#
#
#
#
#

#
#   IMPORT SOURCES:
#
#

#
#   Get PMID.
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
import gnomics.objects.reference

#   Other imports.
import json
import pdfx
import re
import requests
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree

#   MAIN
def main():
    pmid_unit_tests("CHEMBL1128639")

#   Get PMID.
def get_pmid(ref): 
    pmid_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier":
            pmid_array.append(ident["identifier"])
    for ident in ref.identifiers:   
        if ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            for obj in gnomics.objects.reference.Reference.chembl_document(ref):
                if "pubmed_id" in obj:
                    pmid_array.append(obj["pubmed_id"])
    return pmid_array
        
#   UNIT TESTS
def pmid_unit_tests(chembl_id):
    print("\nGetting PMID from ChEMBL ID (%s):" % chembl_id)
    chembl_ref = gnomics.objects.reference.Reference(identifier = chembl_id, identifier_type = "ChEMBL ID", language = None, source = "ChEMBL")
    for pmid in get_pmid(chembl_ref):
        print("- %s" % pmid)

#   MAIN
if __name__ == "__main__": main()