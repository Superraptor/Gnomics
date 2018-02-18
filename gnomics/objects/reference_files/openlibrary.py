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
#   Get references from the Open Library.
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
import re
import requests

#   MAIN
def main():
    openlibrary_unit_tests("0451526538", "93005405", "297222669", "OL123M")
    
#   Return OpenLibrary ID (OLID).
def get_openlibrary_id(reference, user=None):
    openlibrary_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        if iden["identifier"] not in openlibrary_array:
            openlibrary_array.append(iden["identifier"])
    
    if openlibrary_array:
        return openlibrary_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in openlibrary_books_api(ref):
            if obj["openlibrary"] not in openlibrary_array:
                openlibrary_array.append(obj["openlibrary"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["openlibrary"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["lccn", "library of congress control number"]):
        for obj in openlibrary_books_api(ref):
            if obj["openlibrary"] not in openlibrary_array:
                openlibrary_array.append(obj["openlibrary"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["openlibrary"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["oclc", "oclc number", "oclc control number"]):
        for obj in openlibrary_books_api(ref):
            if obj["openlibrary"] not in openlibrary_array:
                openlibrary_array.append(obj["openlibrary"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["openlibrary"], identifier_type="OpenLibrary ID", source="OpenLibrary", language=None)
    
    return openlibrary_array
    
#   Open Library Books API.
#   https://openlibrary.org/dev/docs/api/books
#
#   Supports ISBNs, LCCNs, OCLC numbers, and OLIDs.
def openlibrary_books_api(ref, jscmd=False, user=None):
    result_array = []
    result_dict = {}
    
    if jscmd:
        for ref_obj in ref.reference_objects:
            if 'object_type' in ref_obj:
                if ref_obj['object_type'].lower() in ["openlibrary", "openlibrary book", "openlibrary books", "openlibrary books api", "openlibrary object", "openlibrary books object", "openlibrary book object", "openlibrary books api object"]:
                    result_array.append(ref_obj['object'])

        if result_array:
            return result_array

    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]:
            if jscmd:
                
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=ISBN:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json&jscmd=data"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    
                    for iden, sub_dict in decoded.items():
                    
                        title = sub_dict["title"]
                        publication_date = sub_dict["publish_date"]
                        if "by_statement" in sub_dict:
                            by_statement = sub_dict["by_statement"]
                        else:
                            by_statement = None
                        authors = []
                        for auth in sub_dict["authors"]:
                            authors.append(auth["name"])
                        pagination = sub_dict["pagination"]
                        number_of_pages = sub_dict["number_of_pages"]
                        publishers = []
                        for pub in sub_dict["publishers"]:
                            publishers.append(pub["name"])
                        subjects = []
                        for subj in sub_dict["subjects"]:
                            subjects.append(subj["name"])
                        if "cover" in sub_dict:
                            cover_images = {
                                'small': sub_dict["cover"]["small"],
                                'medium': sub_dict["cover"]["medium"],
                                'large': sub_dict["cover"]["large"]
                            }
                        else:
                            cover_images = {}
                        if "isbn_10" in sub_dict["identifiers"]:
                            isbn_10 = sub_dict["identifiers"]["isbn_10"]
                        else:
                            isbn_10 = None
                        if "isbn_13" in sub_dict["identifiers"]:
                            isbn_13 = sub_dict["identifiers"]["isbn_13"]
                        else:
                            isbn_13 = None
                        if "amazon" in sub_dict["identifiers"]:
                            amazon = sub_dict["identifiers"]["amazon"]
                        else:
                            amazon = None
                        if "google" in sub_dict["identifiers"]:
                            google = sub_dict["identifiers"]["google"]
                        else:
                            google = None
                        if "oclc" in sub_dict["identifiers"]:
                            oclc = sub_dict["identifiers"]["oclc"]
                        else:
                            oclc = None
                        openlibrary = sub_dict["identifiers"]["openlibrary"]
                        if "project_gutenberg" in sub_dict["identifiers"]:
                            project_gutenberg = sub_dict["identifiers"]["project_gutenberg"]
                        else:
                            project_gutenberg = None
                        if "librarything" in sub_dict["identifiers"]:
                            librarything = sub_dict["identifiers"]["librarything"]
                        else:
                            librarything = None
                        lccn = sub_dict["identifiers"]["lccn"]
                        if "goodreads" in sub_dict["identifiers"]:
                            goodreads = sub_dict["identifiers"]["goodreads"]
                        else:
                            goodreads = None
                        if "notes" in sub_dict:
                            notes = sub_dict["notes"]
                        else:
                            notes = None
                        subject_people = []
                        if "subject_people" in sub_dict:
                            for subj in sub_dict["subject_people"]:
                                subject_people.append(subj["name"])
                        subject_times = []
                        if "subject_times" in sub_dict:
                            for subj in sub_dict["subject_times"]:
                                subject_times.append(subj["name"])
                        key = sub_dict["key"]
                        url = sub_dict["url"]
                        subject_places = []
                        if "subject_places" in sub_dict:
                            for subj in sub_dict["subject_places"]:
                                subject_places.append(subj["name"])
                        lcc = sub_dict["classifications"]["lc_classifications"]
                        if "dewey_decimal_class" in sub_dict["classifications"]:
                            ddc = sub_dict["classifications"]["dewey_decimal_class"]
                        else:
                            ddc = None
                        if "weight" in sub_dict:
                            weight = sub_dict["weight"]
                        else:
                            weight = None

                        temp_obj = {
                            'title': title,
                            'publication_date': publication_date,
                            'by_statement': by_statement,
                            'authors': authors,
                            'pagination': pagination,
                            'number_of_pages': number_of_pages,
                            'publishers': publishers,
                            'subjects': subjects,
                            'cover_images': cover_images,
                            'isbn_10': isbn_10,
                            'isbn_13': isbn_13,
                            'amazon': amazon,
                            'google': google,
                            'oclc': oclc,
                            'openlibrary': openlibrary,
                            'project_gutenberg': project_gutenberg,
                            'librarything': librarything,
                            'lccn': lccn,
                            'goodreads': goodreads,
                            'notes': notes,
                            'subject_people': subject_people,
                            'subject_times': subject_times,
                            'key': key,
                            'url': url,
                            'subject_places': subject_places,
                            'lcc': lcc,
                            'ddc': ddc,
                            'weight': weight
                        }
                        result_array.append(temp_obj)
                        gnomics.objects.reference.Reference.add_object(ref, obj=temp_obj, object_type="OpenLibrary Book")
                
            else:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=ISBN:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    for iden, attrib in r.json().items():
                        preview = attrib["preview"]
                        result_dict["preview"] = preview
                        if "thumbnail_url" in attrib:
                            thumbnail_url = attrib["thumbnail_url"]
                            result_dict["thumbnail_url"] = thumbnail_url
                        bib_key = attrib["bib_key"]
                        result_dict["bib_key"] = bib_key
                        if "thumbnail_url" in attrib:
                            info_url = attrib["info_url"]
                            result_dict["info_url"] = info_url
                        preview_url = attrib["preview_url"]
                        result_dict["preview_url"] = preview_url
                
        elif ident["identifier_type"].lower() in ["lccn", "library of congress control number"]:
            if jscmd:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=LCCN:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json&jscmd=data"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    
                    for iden, sub_dict in decoded.items():
                    
                        title = sub_dict["title"]
                        publication_date = sub_dict["publish_date"]
                        if "by_statement" in sub_dict:
                            by_statement = sub_dict["by_statement"]
                        else:
                            by_statement = None
                        authors = []
                        for auth in sub_dict["authors"]:
                            authors.append(auth["name"])
                        pagination = sub_dict["pagination"]
                        number_of_pages = sub_dict["number_of_pages"]
                        publishers = []
                        for pub in sub_dict["publishers"]:
                            publishers.append(pub["name"])
                        subjects = []
                        for subj in sub_dict["subjects"]:
                            subjects.append(subj["name"])
                        if "cover" in sub_dict:
                            cover_images = {
                                'small': sub_dict["cover"]["small"],
                                'medium': sub_dict["cover"]["medium"],
                                'large': sub_dict["cover"]["large"]
                            }
                        else:
                            cover_images = {}
                        if "isbn_10" in sub_dict["identifiers"]:
                            isbn_10 = sub_dict["identifiers"]["isbn_10"]
                        else:
                            isbn_10 = None
                        if "isbn_13" in sub_dict["identifiers"]:
                            isbn_13 = sub_dict["identifiers"]["isbn_13"]
                        else:
                            isbn_13 = None
                        if "amazon" in sub_dict["identifiers"]:
                            amazon = sub_dict["identifiers"]["amazon"]
                        else:
                            amazon = None
                        if "google" in sub_dict["identifiers"]:
                            google = sub_dict["identifiers"]["google"]
                        else:
                            google = None
                        if "oclc" in sub_dict["identifiers"]:
                            oclc = sub_dict["identifiers"]["oclc"]
                        else:
                            oclc = None
                        openlibrary = sub_dict["identifiers"]["openlibrary"]
                        if "project_gutenberg" in sub_dict["identifiers"]:
                            project_gutenberg = sub_dict["identifiers"]["project_gutenberg"]
                        else:
                            project_gutenberg = None
                        if "librarything" in sub_dict["identifiers"]:
                            librarything = sub_dict["identifiers"]["librarything"]
                        else:
                            librarything = None
                        lccn = sub_dict["identifiers"]["lccn"]
                        if "goodreads" in sub_dict["identifiers"]:
                            goodreads = sub_dict["identifiers"]["goodreads"]
                        else:
                            goodreads = None
                        if "notes" in sub_dict:
                            notes = sub_dict["notes"]
                        else:
                            notes = None
                        subject_people = []
                        if "subject_people" in sub_dict:
                            for subj in sub_dict["subject_people"]:
                                subject_people.append(subj["name"])
                        subject_times = []
                        if "subject_times" in sub_dict:
                            for subj in sub_dict["subject_times"]:
                                subject_times.append(subj["name"])
                        key = sub_dict["key"]
                        url = sub_dict["url"]
                        subject_places = []
                        if "subject_places" in sub_dict:
                            for subj in sub_dict["subject_places"]:
                                subject_places.append(subj["name"])
                        lcc = sub_dict["classifications"]["lc_classifications"]
                        if "dewey_decimal_class" in sub_dict["classifications"]:
                            ddc = sub_dict["classifications"]["dewey_decimal_class"]
                        else:
                            ddc = None
                        if "weight" in sub_dict:
                            weight = sub_dict["weight"]
                        else:
                            weight = None

                        temp_obj = {
                            'title': title,
                            'publication_date': publication_date,
                            'by_statement': by_statement,
                            'authors': authors,
                            'pagination': pagination,
                            'number_of_pages': number_of_pages,
                            'publishers': publishers,
                            'subjects': subjects,
                            'cover_images': cover_images,
                            'isbn_10': isbn_10,
                            'isbn_13': isbn_13,
                            'amazon': amazon,
                            'google': google,
                            'oclc': oclc,
                            'openlibrary': openlibrary,
                            'project_gutenberg': project_gutenberg,
                            'librarything': librarything,
                            'lccn': lccn,
                            'goodreads': goodreads,
                            'notes': notes,
                            'subject_people': subject_people,
                            'subject_times': subject_times,
                            'key': key,
                            'url': url,
                            'subject_places': subject_places,
                            'lcc': lcc,
                            'ddc': ddc,
                            'weight': weight
                        }
                    
                        result_array.append(temp_obj)
                        gnomics.objects.reference.Reference.add_object(ref, obj=temp_obj, object_type="OpenLibrary Book")
                
            else:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=LCCN:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    for iden, attrib in r.json().items():
                        preview = attrib["preview"]
                        result_dict["preview"] = preview
                        if "thumbnail_url" in attrib:
                            thumbnail_url = attrib["thumbnail_url"]
                            result_dict["thumbnail_url"] = thumbnail_url
                        bib_key = attrib["bib_key"]
                        result_dict["bib_key"] = bib_key
                        if "thumbnail_url" in attrib:
                            info_url = attrib["info_url"]
                            result_dict["info_url"] = info_url
                        preview_url = attrib["preview_url"]
                        result_dict["preview_url"] = preview_url
                
        elif ident["identifier_type"].lower() in ["oclc", "oclc number", "oclc control number"]:
            if jscmd:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=OCLC:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json&jscmd=data"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    
                    for iden, sub_dict in decoded.items():
                    
                        title = sub_dict["title"]
                        publication_date = sub_dict["publish_date"]
                        if "by_statement" in sub_dict:
                            by_statement = sub_dict["by_statement"]
                        else:
                            by_statement = None
                        authors = []
                        for auth in sub_dict["authors"]:
                            authors.append(auth["name"])
                        pagination = sub_dict["pagination"]
                        number_of_pages = sub_dict["number_of_pages"]
                        publishers = []
                        for pub in sub_dict["publishers"]:
                            publishers.append(pub["name"])
                        subjects = []
                        for subj in sub_dict["subjects"]:
                            subjects.append(subj["name"])
                        if "cover" in sub_dict:
                            cover_images = {
                                'small': sub_dict["cover"]["small"],
                                'medium': sub_dict["cover"]["medium"],
                                'large': sub_dict["cover"]["large"]
                            }
                        else:
                            cover_images = {}
                        if "isbn_10" in sub_dict["identifiers"]:
                            isbn_10 = sub_dict["identifiers"]["isbn_10"]
                        else:
                            isbn_10 = None
                        if "isbn_13" in sub_dict["identifiers"]:
                            isbn_13 = sub_dict["identifiers"]["isbn_13"]
                        else:
                            isbn_13 = None
                        if "amazon" in sub_dict["identifiers"]:
                            amazon = sub_dict["identifiers"]["amazon"]
                        else:
                            amazon = None
                        if "google" in sub_dict["identifiers"]:
                            google = sub_dict["identifiers"]["google"]
                        else:
                            google = None
                        if "oclc" in sub_dict["identifiers"]:
                            oclc = sub_dict["identifiers"]["oclc"]
                        else:
                            oclc = None
                        openlibrary = sub_dict["identifiers"]["openlibrary"]
                        if "project_gutenberg" in sub_dict["identifiers"]:
                            project_gutenberg = sub_dict["identifiers"]["project_gutenberg"]
                        else:
                            project_gutenberg = None
                        if "librarything" in sub_dict["identifiers"]:
                            librarything = sub_dict["identifiers"]["librarything"]
                        else:
                            librarything = None
                        lccn = sub_dict["identifiers"]["lccn"]
                        if "goodreads" in sub_dict["identifiers"]:
                            goodreads = sub_dict["identifiers"]["goodreads"]
                        else:
                            goodreads = None
                        if "notes" in sub_dict:
                            notes = sub_dict["notes"]
                        else:
                            notes = None
                        subject_people = []
                        if "subject_people" in sub_dict:
                            for subj in sub_dict["subject_people"]:
                                subject_people.append(subj["name"])
                        subject_times = []
                        if "subject_times" in sub_dict:
                            for subj in sub_dict["subject_times"]:
                                subject_times.append(subj["name"])
                        key = sub_dict["key"]
                        url = sub_dict["url"]
                        subject_places = []
                        if "subject_places" in sub_dict:
                            for subj in sub_dict["subject_places"]:
                                subject_places.append(subj["name"])
                        lcc = sub_dict["classifications"]["lc_classifications"]
                        if "dewey_decimal_class" in sub_dict["classifications"]:
                            ddc = sub_dict["classifications"]["dewey_decimal_class"]
                        else:
                            ddc = None
                        if "weight" in sub_dict:
                            weight = sub_dict["weight"]
                        else:
                            weight = None

                        temp_obj = {
                            'title': title,
                            'publication_date': publication_date,
                            'by_statement': by_statement,
                            'authors': authors,
                            'pagination': pagination,
                            'number_of_pages': number_of_pages,
                            'publishers': publishers,
                            'subjects': subjects,
                            'cover_images': cover_images,
                            'isbn_10': isbn_10,
                            'isbn_13': isbn_13,
                            'amazon': amazon,
                            'google': google,
                            'oclc': oclc,
                            'openlibrary': openlibrary,
                            'project_gutenberg': project_gutenberg,
                            'librarything': librarything,
                            'lccn': lccn,
                            'goodreads': goodreads,
                            'notes': notes,
                            'subject_people': subject_people,
                            'subject_times': subject_times,
                            'key': key,
                            'url': url,
                            'subject_places': subject_places,
                            'lcc': lcc,
                            'ddc': ddc,
                            'weight': weight
                        }
                    
                        result_array.append(temp_obj)
                        gnomics.objects.reference.Reference.add_object(ref, obj=temp_obj, object_type="OpenLibrary Book")
                
            else:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=OCLC:" + re.sub("[^0-9]", "", ident["identifier"]) + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    for iden, attrib in r.json().items():
                        preview = attrib["preview"]
                        result_dict["preview"] = preview
                        if "thumbnail_url" in attrib:
                            thumbnail_url = attrib["thumbnail_url"]
                            result_dict["thumbnail_url"] = thumbnail_url
                        bib_key = attrib["bib_key"]
                        result_dict["bib_key"] = bib_key
                        if "thumbnail_url" in attrib:
                            info_url = attrib["info_url"]
                            result_dict["info_url"] = info_url
                        preview_url = attrib["preview_url"]
                        result_dict["preview_url"] = preview_url
                
        elif ident["identifier_type"].lower() in ["olid", "openlibrary id", "openlibrary identifier", "open library id", "open library identifier"]:
            if jscmd:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=OLID:" + ident["identifier"] + "&format=json&jscmd=data"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    
                    for iden, sub_dict in decoded.items():
                    
                        title = sub_dict["title"]
                        if "publish_date" in sub_dict:
                            publication_date = sub_dict["publish_date"]
                        else:
                            publication_date = None
                        if "by_statement" in sub_dict:
                            by_statement = sub_dict["by_statement"]
                        else:
                            by_statement = None
                        authors = []
                        if "authors" in sub_dict:
                            for auth in sub_dict["authors"]:
                                authors.append(auth["name"])
                        if "pagination" in sub_dict:
                            pagination = sub_dict["pagination"]
                        else:
                            pagination = None
                        if "number_of_pages" in sub_dict:
                            number_of_pages = sub_dict["number_of_pages"]
                        else:
                            number_of_pages = None
                        publishers = []
                        if "publishers" in sub_dict:
                            for pub in sub_dict["publishers"]:
                                publishers.append(pub["name"])
                        subjects = []
                        if "subjects" in sub_dict:
                            for subj in sub_dict["subjects"]:
                                subjects.append(subj["name"])
                        if "cover" in sub_dict:
                            cover_images = {
                                'small': sub_dict["cover"]["small"],
                                'medium': sub_dict["cover"]["medium"],
                                'large': sub_dict["cover"]["large"]
                            }
                        else:
                            cover_images = {}
                        if "isbn_10" in sub_dict["identifiers"]:
                            isbn_10 = sub_dict["identifiers"]["isbn_10"]
                        else:
                            isbn_10 = None
                        if "isbn_13" in sub_dict["identifiers"]:
                            isbn_13 = sub_dict["identifiers"]["isbn_13"]
                        else:
                            isbn_13 = None
                        if "amazon" in sub_dict["identifiers"]:
                            amazon = sub_dict["identifiers"]["amazon"]
                        else:
                            amazon = None
                        if "google" in sub_dict["identifiers"]:
                            google = sub_dict["identifiers"]["google"]
                        else:
                            google = None
                        if "oclc" in sub_dict["identifiers"]:
                            oclc = sub_dict["identifiers"]["oclc"]
                        else:
                            oclc = None
                        openlibrary = sub_dict["identifiers"]["openlibrary"]
                        if "project_gutenberg" in sub_dict["identifiers"]:
                            project_gutenberg = sub_dict["identifiers"]["project_gutenberg"]
                        else:
                            project_gutenberg = None
                        if "librarything" in sub_dict["identifiers"]:
                            librarything = sub_dict["identifiers"]["librarything"]
                        else:
                            librarything = None
                        if "lccn" in sub_dict["identifiers"]:
                            lccn = sub_dict["identifiers"]["lccn"]
                        else:
                            lccn = None
                        if "goodreads" in sub_dict["identifiers"]:
                            goodreads = sub_dict["identifiers"]["goodreads"]
                        else:
                            goodreads = None
                        if "notes" in sub_dict:
                            notes = sub_dict["notes"]
                        else:
                            notes = None
                        subject_people = []
                        if "subject_people" in sub_dict:
                            for subj in sub_dict["subject_people"]:
                                subject_people.append(subj["name"])
                        subject_times = []
                        if "subject_times" in sub_dict:
                            for subj in sub_dict["subject_times"]:
                                subject_times.append(subj["name"])
                        key = sub_dict["key"]
                        url = sub_dict["url"]
                        subject_places = []
                        if "subject_places" in sub_dict:
                            for subj in sub_dict["subject_places"]:
                                subject_places.append(subj["name"])
                        if "classifications" in sub_dict:
                            if "lc_classifications" in sub_dict["classifications"]:
                                lcc = sub_dict["classifications"]["lc_classifications"]
                            else:
                                lcc = None
                            if "dewey_decimal_class" in sub_dict["classifications"]:
                                ddc = sub_dict["classifications"]["dewey_decimal_class"]
                            else:
                                ddc = None
                        else:
                            lcc = None
                            ddc = None
                        if "weight" in sub_dict:
                            weight = sub_dict["weight"]
                        else:
                            weight = None

                        temp_obj = {
                            'title': title,
                            'publication_date': publication_date,
                            'by_statement': by_statement,
                            'authors': authors,
                            'pagination': pagination,
                            'number_of_pages': number_of_pages,
                            'publishers': publishers,
                            'subjects': subjects,
                            'cover_images': cover_images,
                            'isbn_10': isbn_10,
                            'isbn_13': isbn_13,
                            'amazon': amazon,
                            'google': google,
                            'oclc': oclc,
                            'openlibrary': openlibrary,
                            'project_gutenberg': project_gutenberg,
                            'librarything': librarything,
                            'lccn': lccn,
                            'goodreads': goodreads,
                            'notes': notes,
                            'subject_people': subject_people,
                            'subject_times': subject_times,
                            'key': key,
                            'url': url,
                            'subject_places': subject_places,
                            'lcc': lcc,
                            'ddc': ddc,
                            'weight': weight
                        }
                    
                        result_array.append(temp_obj)
                        gnomics.objects.reference.Reference.add_object(ref, obj=temp_obj, object_type="OpenLibrary Book")
            
            else:
                base = "https://openlibrary.org/api/"
                ext = "/books?bibkeys=OLID:" + ident["identifier"] + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    for iden, attrib in r.json().items():
                        preview = attrib["preview"]
                        result_dict["preview"] = preview
                        if "thumbnail_url" in attrib:
                            thumbnail_url = attrib["thumbnail_url"]
                            result_dict["thumbnail_url"] = thumbnail_url
                        bib_key = attrib["bib_key"]
                        result_dict["bib_key"] = bib_key
                        if "thumbnail_url" in attrib:
                            info_url = attrib["info_url"]
                            result_dict["info_url"] = info_url
                        preview_url = attrib["preview_url"]
                        result_dict["preview_url"] = preview_url
                
    if jscmd:
        return result_array
    else:
        return result_dict
        
#   UNIT TESTS
def openlibrary_unit_tests(isbn, lccn, oclc, olid):
    isbn_ref = gnomics.objects.reference.Reference(identifier = isbn, identifier_type = "ISBN", language = None, source = "Open Library")
    for key, entities in openlibrary_books_api(isbn_ref, jscmd = True).items():
        print("- %s" % str(key))
        for sub_key, sub_entities in entities.items():
            print(" - %s: %s" % (str(sub_key), str(sub_entities)))
    
    lccn_ref = gnomics.objects.reference.Reference(identifier = lccn, identifier_type = "LCCN", language = None, source = "Open Library")
    for key, entities in openlibrary_books_api(lccn_ref, jscmd = True).items():
        print("- %s" % str(key))
        for sub_key, sub_entities in entities.items():
            print(" - %s: %s" % (str(sub_key), str(sub_entities)))
    
    oclc_ref = gnomics.objects.reference.Reference(identifier = oclc, identifier_type = "OCLC Control Number", language = None, source = "Open Library")
    for key, entities in openlibrary_books_api(oclc_ref, jscmd = True).items():
        print("- %s" % str(key))
        for sub_key, sub_entities in entities.items():
            print(" - %s: %s" % (str(sub_key), str(sub_entities)))
    
    olid_ref = gnomics.objects.reference.Reference(identifier = olid, identifier_type = "OLID", language = None, source = "Open Library")
    for key, entities in openlibrary_books_api(olid_ref, jscmd = True).items():
        print("- %s" % str(key))
        for sub_key, sub_entities in entities.items():
            print(" - %s: %s" % (str(sub_key), str(sub_entities)))

#   MAIN
if __name__ == "__main__": main()