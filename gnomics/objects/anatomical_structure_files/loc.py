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
#   Get Library of Congress Subject Headings.
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
    loc_unit_tests("21", "")

# Return Library of Congress Subject Heading.
def get_loc_sh(anat, user=None, source="umls"):
    
    loc_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["lch", "lcsh", "library of congress sh", "library of congress subject heading", "loc sh"] and ident["identifier"] not in loc_array:
            loc_array.append(ident["identifier"])
            
    if loc_array:
        return loc_array
    
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]:
    
            if source.lower() in ["umls", "all"]:

                anat_array = []

                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]

                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in loc_array and rep["ui"] != "NONE":

                            # Library of Congress.
                            if rep["rootSource"] == "LCH":
                                loc_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="Library of Congress Subject Heading", language=None, source="UMLS Metathesaurus")

                    if not json_data:
                        break

    return loc_array
    
#   UNIT TESTS
def loc_unit_tests(neu_id, umls_api_key):
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("Getting Library of Congress Subject Headings from NEU ID (%s):" % neu_id)
    for loc in get_loc_sh(neu_anat, user = user):
        print("- " + str(loc))
    
#   MAIN
if __name__ == "__main__": main()