#
#
#
#
#

#
#   IMPORT SOURCES:
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    ceph_unit_tests()
    
# Return CEPH ID.
def get_ceph_id(anat):
    ceph_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "ceph id" or ident["identifier_type"].lower() == "ceph identifier":
            ceph_array.append(ident["identifier"])
    return ceph_array
    
#   UNIT TESTS
def ceph_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()