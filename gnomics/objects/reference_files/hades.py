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
#   Get PII.
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
import re
import requests
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree

#   MAIN
def main():
    hades_unit_tests()

#   Get Hades Collection Guide ID.
def get_hades_collection_guide_id(ref): 
    hades_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["hades collection guide id", "hades collection guide identifier", "hades collection guide"]:
            hades_array.append(ident["identifier"])
    return hades_array
        
#   Get Hades Struc ID.
def get_hades_struc_id(ref): 
    hades_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["hades struc id", "hades struc", "hades struc identifier"]:
            hades_array.append(ident["identifier"])
    return hades_array
    
#   UNIT TESTS
def hades_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()