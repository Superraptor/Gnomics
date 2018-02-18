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
#   Get references from Elsevier.
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
import requests
import scholarly

#   MAIN
def main():
    elsevier_unit_tests("CDK4 Amplification", "")
    
#   Get Elsevier ID (EID).
def get_eid(reference):
    elsevier_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["eid", "elsevier id", "elsevier identifier"]):
        if iden["identifier"] not in elsevier_array:
            elsevier_array.append(iden["identifier"])
    return elsevier_array
    
#   Affiliation Search.
def affiliation_search():
    print("NOT FUNCTIONAL.")

#   Author Search.
#
#   For more information, see here:
#   - https://api.elsevier.com/documentation/AuthorSearchAPI.wadl
#   - https://dev.elsevier.com/tips/AuthorSearchTips.htm
#
#   Parameters:
#   - AF-ID (Affiliation ID)
#   - AFFIL (Affiliation)
#   - AU-ID (Author Identifier Number)
#   - AUTHFIRST (Author First Initial or First Name)
def author_search(query, user=None):
    if user is not None:
        if user.elsevier_api_key is not None:
            if query:
                base = "https://api.elsevier.com/content/search/"
                ext = "scidir?query=" + str(query) + "&apiKey=" + str(user.elsevier_api_key)
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    print(r.json())
            else:
                print("NOT FUNCTIONAL.")

#   Engineering Village Search.
def engineering_village_search():
    print("NOT FUNCTIONAL.")

#   ScienceDirect Search.
def sciencedirect_search(query, user=None):
    if user is not None:
        if user.elsevier_api_key is not None:
            base = "https://api.elsevier.com/content/search/"
            ext = "scidir?query=" + str(query) + "&apiKey=" + str(user.elsevier_api_key)

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                
                results_array = []
                for entry in r.json()["search-results"]["entry"]:
                    
                    eid = entry["eid"]
                    title = entry["dc:title"]
                    creator = entry["dc:creator"]
                    publication = entry["prism:publicationName"]
                    issn = entry["prism:issn"]
                    if "prism:volume" in entry:
                        volume = entry["prism:volume"]
                    else:
                        volume = None
                    issue = entry["prism:issueIdentifier"]
                    cover_display_date = entry["prism:coverDisplayDate"]
                    if "prism:startingPage" in entry:
                        start_page = entry["prism:startingPage"]
                    else:
                        start_page = None
                    if "prism:endingPage" in entry:
                        end_page = entry["prism:endingPage"]
                    else:
                        end_page = None
                    doi = entry["prism:doi"]
                    openaccess = entry["openaccess"]
                    pii = entry["pii"]
                    teaser = entry["prism:teaser"]
                    
                    result = {
                        'eid': eid,
                        'title': title,
                        'creator': creator,
                        'publication': publication,
                        'issn': issn,
                        'volume': volume,
                        'issue': issue,
                        'cover_display_date': cover_display_date,
                        'start_page': start_page,
                        'end_page': end_page,
                        'doi': doi,
                        'openaccess': openaccess,
                        'pii': pii,
                        'teaser': teaser
                    }
                    results_array.append(result)
                    
                return results_array
        else:
            print("A valid Elsevier API key is necessary to use this function.")
        
    else:
        print("A valid user with a valid Elsevier API key is necessary to use this function.")

#   Scopus Search.
def scopus_search():
    print("NOT FUNCTIONAL.")
    
#   UNIT TESTS
def elsevier_unit_tests(query, elsevier_api_key):
    user = User(elsevier_api_key = elsevier_api_key)
    
    for result in sciencedirect_search(query, user = user):
        print("- %s: %s" % (str(result["eid"]), str(result["title"].encode('ascii',errors='ignore').decode())))

#   MAIN
if __name__ == "__main__": main()