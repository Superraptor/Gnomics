#!/usr/bin/env python

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
#   Cephalopod Ontology (CEPH).
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
import gnomics.objects.anatomical_structure
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    ceph_unit_tests()
    
# Return CEPH ID.
def get_ceph_id(anat, user=None):
    ceph_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["ceph", "ceph id", "ceph identifier"]):
        if iden["identifier"] not in ceph_array:
            ceph_array.append(iden["identifier"])
    return ceph_array
    
#   UNIT TESTS
def ceph_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()