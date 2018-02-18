#!/usr/bin/env python

#  
#   NOTE: Unfortunately, ISBNdb has upgraded to a new
#   pay-per-call system which cannot be implemented
#   due to cost based restrictions. However, this code
#   will be kept in place as legacy code.
#

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
#   Get references from the ISBNdb.
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
from bs4 import BeautifulSoup
import json
import requests

#   MAIN
def main():
    isbndb_unit_tests("9780849303159", "")
    
#   Books endpoint.
#   https://isbndb.com/api/v2/docs/books
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def get_isbndb_books(ref, user=None, response_format="json"):
    result_array = []
    
    for ref_obj in ref.reference_objects:
        if 'object_type' in ref_obj:
            if ref_obj['object_type'].lower() in ["isbndb book", "isbndb book object", "isbndb books", "isbndb books object"]:
                result_array.append(ref_obj['object'])
    
    if result_array:
        return result_array
    
    if user is not None:
    
        for ident in ref.identifiers:
            if ident["identifier_type"].lower() in ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]:

                base = "http://api.isbndb.com"
                ext = "/book/" + ident["identifier"] + "&x-api-key=" + user.isbndb_api_key

                r = requests.get(base+ext, headers={"Content-Type": "application/json", "x-api-key": user.isbndb_api_key})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    for x in r.json()["data"]:
                        authors = []
                        isbndb_author_ids = []
                        for y in x["author_data"]:
                            authors.append(y["name"])
                            isbndb_author_ids.append(y["id"])
                        if x["awards_text"] != "":
                            awards_text = x["awards_text"]
                        else:
                            awards_text = None
                        if x["marc_enc_level"] != "":
                            marc_encoding_level = x["marc_enc_level"]
                        else:
                            marc_encoding_level = None
                        if x["summary"] != "":
                            summary = x["summary"]
                        else:
                            summary = None
                        if x["isbn13"] != "":
                            isbn_13 = x["isbn13"]
                        else:
                            isbn_13 = None
                        if x["dewey_normal"] != "":
                            ddc_norm = x["dewey_normal"]
                        else:
                            ddc_norm = None
                        if x["title_latin"] != "":
                            title_ascii = x["title_latin"]
                        else:
                            title_ascii = None
                        if x["publisher_id"] != "":
                            isbndb_publisher_id = x["publisher_id"]
                        else:
                            isbndb_publisher_id = None
                        if x["dewey_decimal"] != "":
                            ddc = x["dewey_decimal"]
                        else:
                            ddc = None
                        if x["publisher_text"] != "":
                            publisher_text = x["publisher_text"]
                        else:
                            publisher_text = None
                        if x["language"] != "":
                            language = x["language"]
                        else:
                            language = None
                        if x["physical_description_text"] != "":
                            physical_description = x["physical_description_text"]
                        else:
                            physical_description = None
                        if x["isbn10"] != "":
                            isbn_10 = x["isbn10"]
                        else:
                            isbn_10 = None
                        if x["edition_info"] != "":
                            edition_information = x["edition_info"]
                        else:
                            edition_information = None
                        if x["urls_text"] != "":
                            url_text = x["urls_text"]
                        else:
                            url_text = None
                        if x["lcc_number"] != "":
                            lcc = x["lcc_number"]
                        else:
                            lcc = None
                        if x["publisher_name"] != "":
                            publisher = x["publisher_name"]
                        else:
                            publisher = None
                        isbndb_book_id = x["book_id"]
                        if x["notes"] != "":
                            notes = x["notes"]
                        else:
                            notes = None
                        if x["title"] != "":
                            title = x["title"]
                        else:
                            title = None
                        if x["title_long"] != "":
                            title_full = x["title_long"]
                        else:
                            title_full = None
                             
                        result = {
                            "isbndb_book_id": isbndb_book_id,
                            "authors": authors,
                            "isbndb_author_ids":
                            isbndb_author_ids,
                            "awards": awards_text,
                            "marc_encoding_level": marc_encoding_level,
                            "summary": summary,
                            "isbn_10": isbn_10,
                            "isbn_13": isbn_13,
                            "ddc": ddc,
                            "ddc_norm": ddc_norm,
                            "lcc": lcc,
                            "title": title,
                            "title_ascii": title_ascii,
                            "title_full": title_full,
                            "publisher": publisher,
                            "publisher_text": publisher_text,
                            "isbndb_publisher_id": isbndb_publisher_id,
                            "language": language,
                            "physical_description": physical_description,
                            "edition_information": edition_information,
                            "url_text": url_text,
                            "notes": notes
                        }
                             
                        gnomics.objects.reference.Reference.add_object(ref, obj=result, object_type="ISBNdb Books")
                        
                        result_array.append(result)
                            
            elif ident["identifier_type"].lower() in ["isbndb", "isbndb id", "isbndb identifier", "isbndb book id", "isbndb book identifier"]:
                print("NOT FUNCTIONAL.")
                
    else:
        print("For this function, a valid user with a valid ISBNdb API key is necessary.")
        
    return result_array

#   Return ISBNdb Book ID.
def get_isbndb_book_id(reference, user=None):
    
    isbndb_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbndb book", "isbndb book id", "isbndb book identifier"]):
        if iden["identifier"] not in isbndb_array:
            isbndb_array.append(iden["identifier"])
    
    if isbndb_array:
        return isbndb_array
    
    for ident in reference.identifiers:
        if ident["identifier_type"].lower() in ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]:
            for obj in get_isbndb_books(ref, user=user):
                if obj["isbndb_book_id"] not in isbndb_array:
                    isbndb_book_id = obj["isbndb_book_id"]
                    gnomics.objects.reference.Reference.add_identifier(reference, identifier=isbndb_book_id, identifier_type="ISBNdb Book ID", source="ISBNdb", language=None)
                    isbndb_array.append(isbndb_book_id)
            
    return isbndb_array
    
#   Authors endpoint.
#   http://isbndb.com/api/v2/docs/authors
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def isbndb_authors():
    print("NOT FUNCTIONAL.")
    
#   Publishers endpoint.
#   http://isbndb.com/api/v2/docs/publishers
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def isbndb_publishers():
    print("NOT FUNCTIONAL.")
    
#   Subjects endpoint.
#   http://isbndb.com/api/v2/docs/subjects
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def isbndb_subjects():
    print("NOT FUNCTIONAL.")
    
#   Categories endpoint.
#   http://isbndb.com/api/v2/docs/categories
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def isbndb_categories():
    print("NOT FUNCTIONAL.")
    
#   Prices endpoint.
#   http://isbndb.com/api/v2/docs/prices
#
#   Response formats:
#   - JSON
#   - YAML
#   - XML
def isbndb_prices():
    print("NOT FUNCTIONAL.")
        
#   UNIT TESTS
def isbndb_unit_tests(isbn, isbndb_api_key):
    user = User(isbndb_api_key = isbndb_api_key)
    isbn_ref = gnomics.objects.reference.Reference(identifier = isbn, identifier_type = "ISBN-13")
    print("Getting book information for ISBN '%s'..." % str(isbn))
    for x in get_isbndb_books(isbn_ref, user = user):
        for field, field_info in x.items():
            print("- %s: %s" % (str(field), str(field_info)))

#   MAIN
if __name__ == "__main__": main()