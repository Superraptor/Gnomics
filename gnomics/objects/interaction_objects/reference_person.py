#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       ORCID
#           https://pypi.python.org/pypi/orcid/
#

#
#   Get people from reference.
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
import gnomics.objects.person
import gnomics.objects.reference

#   Other imports.
import json
import orcid
import requests
import timeit

#   MAIN
def main():
    reference_person_unit_tests("28723805", "10.1038/171737a0", "", "", "")
     
#   Get authors.
def get_authors(reference, user=None):
    auth_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["library of congress control number", "lccn"]):
        for obj in Reference.openlibrary(reference, user=user):
            temp_auth_array = obj["authors"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="OpenLibrary")
                auth_array.append(temp_person)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["olid", "openlibrary", "openlibrary id", "openlibrary identifier"]):
        for obj in Reference.openlibrary(reference, user=user):
            temp_auth_array = obj["authors"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="OpenLibrary")
                auth_array.append(temp_person)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["oclc", "oclc control number", "oclc number"]):
        for obj in Reference.openlibrary(reference, user=user):
            temp_auth_array = obj["authors"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="OpenLibrary")
                auth_array.append(temp_person)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn10", "isbn-10", "isbn 10", "isbn13", "isbn-13", "isbn 13", "isbn"]):
        for obj in Reference.google_book(reference, user=user):
            temp_auth_array = obj["Author"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="Google Books")
                auth_array.append(temp_person)
                
        for obj in Reference.openlibrary(reference, user=user):
            temp_auth_array = obj["authors"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="OpenLibrary")
                auth_array.append(temp_person)
                
        for obj in Reference.isbndb_books(reference, user=user):
            temp_auth_array = obj["authors"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="ISBNdb")
                auth_array.append(temp_person)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["chembl", "chembl document", "chembl document id", "chembl document identifier", "chembl id", "chembl identifier"]):
        
        for doc in gnomics.objects.reference.Reference.chembl_document(reference, user=user):
            author_array = doc["authors"].split(", ")
            for author in authors:
                temp_person = gnomics.objects.person.Person(identifier=author, identifier_type="Full Name", language=None, source="ChEMBL", name=author)
                auth_array.append(temp_person)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["pmid", "pubmed", "pubmed id", "pubmed identifier"]):
        
        for article in gnomics.objects.reference.Reference.pmid_article(reference, user=user):
            temp_auth_array = article.authors
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth, identifier_type="Full Name", language=None, source="PubMed", name=temp_auth)
                auth_array.append(temp_person)
        if user:
            if user.orcid_client_id and user.orcid_client_secret:
                api = orcid.SearchAPI(sandbox=True)
                search_results = api.search_public("pmid-self:"+iden["identifier"])

                for result in search_results["orcid-search-results"]["orcid-search-result"]:
                    if result["orcid-profile"]["orcid"] is not None:
                        temp_person = gnomics.objects.person.Person(identifier=result["orcid-profile"]["orcid"], identifier_type="ORCID", language=None, source="ORCID")
                        auth_array.append(temp_person)

            if user.elsevier_api_key:
                base = "https://api.elsevier.com/content/search/"
                ext = "scopus?query=PMID(" + str(iden["identifier"]) + ")&apiKey=" + str(user.elsevier_api_key) + "&field=orcid,dc:creator,author,author-url,authid,authname,given-name,surname,initials,afid"

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                
                if not r.ok:
                    print("Something went wrong.")
                else:
                    if "search-results" in r.json():
                        if "entry" in r.json()["search-results"]:
                            for sub_entry in r.json()["search-results"]["entry"]:
                                if "dc:creator" in sub_entry:
                                    temp_person = gnomics.objects.person.Person(identifier=sub_entry["dc:creator"], identifier_type="dc:creator", source="Elsevier", language=None)
                                    auth_array.append(temp_person)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["doi", "digital object id", "digital object identifier"]):
        
        for article in gnomics.objects.reference.Reference.doi_object(reference, user=user):
            temp_auth_array = article["message"]["author"]
            for temp_auth in temp_auth_array:
                temp_person = gnomics.objects.person.Person(identifier=temp_auth["given"], identifier_type="Given Name", language=None, source="CrossRef")
                gnomics.objects.person.Person.add_identifier(temp_person, identifier=temp_auth["family"], identifier_type="Family Name", language=None, source="CrossRef")
                auth_array.append(temp_person)
        
        if user:
            if user.orcid_client_id and user.orcid_client_secret:
                api = orcid.SearchAPI(sandbox=True)
                search_results = api.search_public("doi-self:"+iden["identifier"])

                for result in search_results["orcid-search-results"]["orcid-search-result"]:
                    if result["orcid-profile"]["orcid"] is not None:
                        temp_person = gnomics.objects.person.Person(identifier=result["orcid-profile"]["orcid"], identifier_type="ORCID", language=None, source="ORCID")
                        auth_array.append(temp_person)
                
            if user.elsevier_api_key:
                base = "https://api.elsevier.com/content/search/"
                ext = "scopus?query=DOI(" + str(iden["identifier"]) + ")&apiKey=" + str(user.elsevier_api_key) + "&field=orcid,dc:creator,author,author-url,authid,authname,given-name,surname,initials,afid"

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    if "search-results" in r.json():
                        if "entry" in r.json()["search-results"]:
                            for sub_entry in r.json()["search-results"]["entry"]:
                                if "dc:creator" in sub_entry:
                                    temp_person = gnomics.objects.person.Person(identifier=sub_entry["dc:creator"], identifier_type="dc:creator", source="Elsevier", language=None)
                                    auth_array.append(temp_person)
        
    return auth_array
    
#   UNIT TESTS
def reference_person_unit_tests(pmid, doi, orcid_client_id, orcid_client_secret, elsevier_api_key):
    user = User(elsevier_api_key = elsevier_api_key)
    
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    print("Getting authors from PMID (%s):" % pmid)
    for auth in get_authors(pubmed_ref, user=user):
        for iden in auth.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

    doi_ref = gnomics.objects.reference.Reference(identifier = doi, identifier_type = "DOI", language = None, source = "Nature")
    print("\nGetting authors from DOI (%s):" % doi)
    for auth in get_authors(doi_ref, user=user):
        for iden in auth.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
#   MAIN
if __name__ == "__main__": main()