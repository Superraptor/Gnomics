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
#   Get DPLA (Digital Public Library of America).
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
import requests

#   MAIN
def main():
    dpla_unit_tests("weasels", "")
    
#   Get DPLA UUID.
def get_dpla_uuid(ref, user=None):
    dpla_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["dpla", "dpla uuid"]:
            dpla_array.append(ident["identifier"])
    return dpla_array
    
#   DPLA search.
def dpla_search(query, user=None):
    search_results = []
    if user is not None:
        if user.dpla_api_key is not None:
            base = "https://api.dp.la/v2/"
            ext = "items?q=" + str(query) + "&api_key=" + str(user.dpla_api_key)

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:
                for doc in r.json()["docs"]:

                    if "originalRecord" in doc:
                        if "titleInfo" in doc["originalRecord"]:
                            temp_lang=None
                            if "lang" in doc["originalRecord"]["titleInfo"]:
                                temp_lang = doc["originalRecord"]["titleInfo"]["lang"]

                            title = doc["originalRecord"]["titleInfo"]["title"]
                            temp_ref = gnomics.objects.reference.Reference(identifier=title, identifier_type="Title", source="DPLA", language=temp_lang, name=title)

                            for sub_iden in doc["originalRecord"]["identifier"]:
                                if sub_iden["type"] == "local_hades_collection":
                                    gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=sub_iden["#text"], identifier_type="Hades Collection Guide ID", source="DPLA", name=title)

                                elif sub_iden["type"] == "local_hades":
                                    gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=sub_iden["#text"], identifier_type="Hades Struc ID", source="DPLA", name=title)

                                elif sub_iden["type"] == "uuid":
                                    gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=sub_iden["#text"], identifier_type="DPLA UUID", source="DPLA", name=title)            

                            search_results.append(temp_ref)

                    else:
                        print(doc)
                
    return search_results
    
#   UNIT TESTS
def dpla_unit_tests(query, dpla_api_key):
    user = User(dpla_api_key=dpla_api_key)
    
    print("Obtaining DPLA documents from query '%s'...\n" % str(query))
    for ref in dpla_search(query, user=user):
        for iden in ref.identifiers:
            print("- %s (%s) [%s]" % (iden["name"].encode("ascii", errors="ignore").decode(), iden["identifier"], iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()