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
#   Get KEGG Disease ID.
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
    kegg_disease_unit_tests()
    
# Return KEGG disease object.
def get_kegg_disease(dis):
    for dis_obj in dis.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() in ['kegg', 'kegg disease']:
                return dis_obj['object']
    s = KEGG()
    res = s.get(gnomics.objects.disease.Disease.kegg_disease_id(dis))
    disease = s.parse(res)
    dis.disease_objects.append({
        'object': disease,
        'object_type': "KEGG disease"
    })
    return disease

#   Get KEGG disease ID.
def get_kegg_disease_id(dis):
    dis_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(dis.identifiers, ["kegg", "kegg id", "kegg identifier", "kegg disease", "kegg disease accession", "kegg accession", "kegg disease id", "kegg disease identifier"]):
        if iden["identifier"] not in dis_array:
            dis_array.append(iden["identifier"])
    return dis_array

#   UNIT TESTS
def kegg_disease_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()