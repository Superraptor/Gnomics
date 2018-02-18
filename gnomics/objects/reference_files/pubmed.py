#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       METAPUB
#           https://pypi.python.org/pypi/metapub
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
import gnomics.objects.disease
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
from metapub import FindIt
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
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(ref.identifiers, ["pmid", "pubmed", "pubmed id", "pubmed identifier"]):
        if iden["identifier"] not in pmid_array:
            pmid_array.append(iden["identifier"])
        
    if pmid_array:
        return pmid_array
    
    for ident in ref.identifiers:   
        if ident["identifier_type"].lower() in ["chembl", "chembl document", "chembl document id", "chembl document identifier", "chembl id", "chembl identifier"]:
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