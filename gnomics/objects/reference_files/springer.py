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
#   Get references from Springer.
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
from lxml import html
import json
import re
import requests
import xml.etree.ElementTree

#   MAIN
def main():
    springer_unit_tests("glioblastoma", "Frontiers of Physics", "919807c0eaa0117d93f56d80b875ce70")
    
#   Get Springer Journal ID.
def get_springer_journal_id(journal_name):
    match_array = []
        
    server = "https://link.springer.com"
    ext = "/search?query=" + str(journal_name) + "&facet-content-type=%22Journal%22"

    r = requests.get(server+ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        #r.raise_for_status()
        #sys.exit()
        print("Something went wrong.")

    else:
        text = r.text
        journal_id_regex = re.compile('<a class="title" href="\/journal\/([0-9]+)">'+str(journal_name)+'<\/a>')
        for match in re.findall(journal_id_regex, text):
            match_array.append(match)
            
    return match_array

#   Springer Metadata Service.
#
#   "Allows users to retrieve metadata for more than 10 million
#   online documents."
#
#   Parameters:
#   - api_key: the API access key.
#   - q: the query string.
#   - output: the result format (either JSON or PAM).
#   - s: the index of the first hit to return (default is 1).
#   - p: the maximum number of hits to return (default is 10).
def springer_metadata_service(query, user=None, output="json", s=1, p=10):
    if user is not None:
        if user.springer_api_key is not None:
            if output.lower() == "json":
            
                base = "http://api.springer.com/metadata/"
                ext = "json?api_key=" + str (user.springer_api_key) + "&q=" + str(query) + "&s=" + str(s) + "&p=" + str(p)

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = json.loads(r.text)
                    
                    temp_obj = {}
                    for record in decoded["records"]:
                        if record["identifier"] != "":
                            identifier = record["identifier"]
                        else:
                            identifier = None
                            
                        if record["title"] != "":
                            title = record["title"]
                        else:
                            title = None
                        
                        if record["publicationName"] != "":
                            publication = record["publicationName"]
                        else:
                            publication = None
                            
                        if record["openaccess"] != "":
                            openaccess = record["openaccess"]
                        else:
                            openaccess = None
                            
                        if record["doi"] != "":
                            doi = record["doi"]
                        else:
                            doi = None
                        
                        if record["printIsbn"] != "":
                            print_isbn = record["printIsbn"]
                        else:
                            print_isbn = None
                        
                        if record["electronicIsbn"] != "":
                            electronic_isbn = record["electronicIsbn"]
                        else:
                            electronic_isbn = None
                            
                        if record["isbn"] != "":
                            isbn = record["isbn"]
                        else:
                            isbn = None
                            
                        if record["publisher"] != "":
                            publisher = record["publisher"]
                        else:
                            publisher = None
                            
                        if record["publicationDate"] != "":
                            publication_date = record["publicationDate"]
                        else:
                            publication_date = None
                            
                        if record["onlineDate"] != "":
                            online_date = record["onlineDate"]
                        else:
                            online_date = None
                            
                        if record["printDate"] != "":
                            print_date = record["printDate"]
                        else:
                            print_date = None
                            
                        if record["volume"] != "":
                            volume = record["volume"]
                        else:
                            volume = None
                            
                        if record["number"] != "":
                            number = record["number"]
                        else:
                            number = None
                            
                        if record["startingPage"] != "":
                            starting_page = record["startingPage"]
                        else:
                            starting_page = None
                            
                        if record["copyright"] != "":
                            copyright = record["copyright"]
                        else:
                            copyright = None
                            
                        if record["genre"] != "":
                            genre = record["genre"]
                        else:
                            genre = None
                            
                        if record["abstract"] != "":
                            abstract = record["abstract"]
                        else:
                            abstract = None
                        
                        creators = []
                        for creator in record["creators"]:
                            creators.append(creator["creator"])
                            
                        temp_obj[identifier] = {
                            'title': title,
                            'publication': publication,
                            'openaccess': openaccess,
                            'doi': doi,
                            'electronic_isbn': electronic_isbn,
                            'print_isbn': print_isbn,
                            'isbn': isbn,
                            'publisher': publisher,
                            'publication_date': publication_date,
                            'online_date': online_date,
                            'print_date': print_date,
                            'volume': volume,
                            'number': number,
                            'starting_page': starting_page,
                            'copyright': copyright,
                            'genre': genre,
                            'abstract': abstract,
                            'creators': creators
                        }
                        
                    ref_list = []
                    for obj_iden, obj_dict in temp_obj.items():
                        
                        if obj_dict["doi"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["doi"], identifier_type = "DOI", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["electronic_isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["electronic_isbn"], identifier_type = "Electronic ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["print_isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["print_isbn"], identifier_type = "Print ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["electronic_isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["electronic_isbn"], identifier_type = "Electronic ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["print_isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["print_isbn"], identifier_type = "Print ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["print_isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["print_isbn"], identifier_type = "Print ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["print_isbn"], identifier_type = "Print ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            ref_list.append(temp_ref)
                            
                        else:
                            print("Cannot find appropriate identifier for object, '%s'." % str(obj_iden))
                            
                    return ref_list
                
            elif output.lower() == "pam":
                print("PAM output is not currently supported.")
            else:
                print("The provided output (%s) is not supported." % str(output))
        else:
            print("A valid Springer API is required to access the Springer API.")
    else:
        print("A valid user object with a valid Springer API key is required to access the Springer API.")
    
#   Springer Meta API Service.
#
#   "Allows users to retrieve metadata for more than 11
#   million online documents."
#
#   Parameters:
#   - api_key: the API access key.
#   - q: the query string.
#   - output: the result format (either JSON or PAM).
#   - s: the index of the first hit to return (default is 1).
#   - p: the maximum number of hits to return (default is 10).
def springer_meta_api_service(query, user = None, output = "json", s = 1, p = 10):
    
    if user is not None:
        if user.springer_api_key is not None:
            if output.lower() == "json":
            
                base = "http://api.springer.com/meta/v1/"
                ext = "json?api_key=" + str (user.springer_api_key) + "&q=" + str(query) + "&s=" + str(s) + "&p=" + str(p)

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = json.loads(r.text)
                    
                    temp_obj = {}
                    for record in decoded["records"]:
                        if record["identifier"] != "":
                            identifier = record["identifier"]
                        else:
                            identifier = None
                            
                        if record["title"] != "":
                            title = record["title"]
                        else:
                            title = None
                        
                        if record["publicationName"] != "":
                            publication = record["publicationName"]
                        else:
                            publication = None
                            
                        if record["openaccess"] != "":
                            openaccess = record["openaccess"]
                        else:
                            openaccess = None
                            
                        if record["doi"] != "":
                            doi = record["doi"]
                        else:
                            doi = None
                            
                        if record["electronicIsbn"] != "":
                            electronic_isbn = record["electronicIsbn"]
                        else:
                            electronic_isbn = None
                            
                        if record["isbn"] != "":
                            isbn = record["isbn"]
                        else:
                            isbn = None
                            
                        if record["publisher"] != "":
                            publisher = record["publisher"]
                        else:
                            publisher = None
                            
                        if record["publicationDate"] != "":
                            publication_date = record["publicationDate"]
                        else:
                            publication_date = None
                            
                        if record["onlineDate"] != "":
                            online_date = record["onlineDate"]
                        else:
                            online_date = None
                            
                        if record["printDate"] != "":
                            print_date = record["printDate"]
                        else:
                            print_date = None
                            
                        if record["volume"] != "":
                            volume = record["volume"]
                        else:
                            volume = None
                            
                        if record["number"] != "":
                            number = record["number"]
                        else:
                            number = None
                            
                        if record["startingPage"] != "":
                            starting_page = record["startingPage"]
                        else:
                            starting_page = None
                            
                        if record["copyright"] != "":
                            copyright = record["copyright"]
                        else:
                            copyright = None
                            
                        if record["genre"] != "":
                            genre = record["genre"]
                        else:
                            genre = None
                            
                        if record["abstract"] != "":
                            abstract = record["abstract"]
                        else:
                            abstract = None
                        
                        creators = []
                        for creator in record["creators"]:
                            creators.append(creator["creator"])
                            
                        temp_obj[identifier] = {
                            'title': title,
                            'publication': publication,
                            'openaccess': openaccess,
                            'doi': doi,
                            'electronic_isbn': electronic_isbn,
                            'isbn': isbn,
                            'publisher': publisher,
                            'publication_date': publication_date,
                            'online_date': online_date,
                            'print_date': print_date,
                            'volume': volume,
                            'number': number,
                            'starting_page': starting_page,
                            'copyright': copyright,
                            'genre': genre,
                            'abstract': abstract,
                            'creators': creators
                        }
                        
                    ref_list = []
                    for obj_iden, obj_dict in temp_obj.items():
                        
                        if obj_dict["doi"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["doi"], identifier_type = "DOI", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["electronic_isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["electronic_isbn"], identifier_type = "Electronic ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["electronic_isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["electronic_isbn"], identifier_type = "Electronic ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            ref_list.append(temp_ref)
                            
                        else:
                            print("Cannot find appropriate identifier for object, '%s'." % str(obj_iden))
                            
                    return ref_list
                
            elif output.lower() == "pam":
                print("PAM output is not currently supported.")
            else:
                print("The provided output (%s) is not supported." % str(output))
        else:
            print("A valid Springer API is required to access the Springer API.")
    else:
        print("A valid user object with a valid Springer API key is required to access the Springer API.")
    
#   Springer OpenAccess API.
#
#   "Provides metadata, full-text content, and images for over
#   80,000 open access articles from BioMed Central and
#   SpringerOpen journals."
#
#   Parameters:
#   - api_key: the API access key.
#   - q: the query string.
#   - output: the result format (either JSON or PAM).
#   - s: the index of the first hit to return (default is 1).
#   - p: the maximum number of hits to return (default is 10).
def springer_openaccess_api(query, user = None, output = "json", s = 1, p = 10):
    
    if user is not None:
        if user.springer_api_key is not None:
            if output.lower() == "json":
            
                base = "http://api.springer.com/openaccess/"
                ext = "json?api_key=" + str (user.springer_api_key) + "&q=" + str(query) + "&s=" + str(s) + "&p=" + str(p)

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = json.loads(r.text)
                    
                    temp_obj = {}
                    for record in decoded["records"]:
                        if record["identifier"] != "":
                            identifier = record["identifier"]
                        else:
                            identifier = None
                            
                        if record["title"] != "":
                            title = record["title"]
                        else:
                            title = None
                        
                        if record["publicationName"] != "":
                            publication = record["publicationName"]
                        else:
                            publication = None
                            
                        if record["doi"] != "":
                            doi = record["doi"]
                        else:
                            doi = None
                        
                        if record["issn"] != "":
                            issn = record["issn"]
                        else:
                            issn = None
                        
                        if record["isbn"] != "":
                            isbn = record["isbn"]
                        else:
                            isbn = None
                            
                        if record["publisher"] != "":
                            publisher = record["publisher"]
                        else:
                            publisher = None
                            
                        if record["publicationDate"] != "":
                            publication_date = record["publicationDate"]
                        else:
                            publication_date = None
                            
                        if record["volume"] != "":
                            volume = record["volume"]
                        else:
                            volume = None
                            
                        if record["number"] != "":
                            number = record["number"]
                        else:
                            number = None
                            
                        if record["startingPage"] != "":
                            starting_page = record["startingPage"]
                        else:
                            starting_page = None
                            
                        if record["endingPage"] != "":
                            ending_page = record["endingPage"]
                        else:
                            ending_page = None
                            
                        if record["copyright"] != "":
                            copyright = record["copyright"]
                        else:
                            copyright = None
                            
                        temp_obj[identifier] = {
                            'title': title,
                            'publication': publication,
                            'doi': doi,
                            'issn': issn,
                            'isbn': isbn,
                            'publisher': publisher,
                            'publication_date': publication_date,
                            'volume': volume,
                            'number': number,
                            'starting_page': starting_page,
                            'ending_page': ending_page,
                            'copyright': copyright
                        }
                        
                    ref_list = []
                    for obj_iden, obj_dict in temp_obj.items():
                        
                        if obj_dict["doi"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["doi"], identifier_type = "DOI", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["isbn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            if obj_dict["issn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["issn"], identifier_type = "ISSN", language = None, source = "Springer", name = obj_dict["title"])
                                
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["isbn"], identifier_type = "ISBN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            if obj_dict["issn"]:
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = obj_dict["issn"], identifier_type = "ISSN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            ref_list.append(temp_ref)
                            
                        elif obj_dict["isbn"]:
                            temp_ref = gnomics.objects.reference.Reference(identifier = obj_dict["issn"], identifier_type = "ISSN", language = None, source = "Springer", name = obj_dict["title"])
                            
                            ref_list.append(temp_ref)
                            
                        else:
                            print("Cannot find appropriate identifier for object, '%s'." % str(obj_iden))
                            
                    return ref_list
                
            elif output.lower() == "pam":
                print("PAM output is not currently supported.")
            else:
                print("The provided output (%s) is not supported." % str(output))
        else:
            print("A valid Springer API is required to access the Springer API.")
    else:
        print("A valid user object with a valid Springer API key is required to access the Springer API.")
    
#   Springer Integro API.
#
#   "Provides journal-level metadata for Springer Journals".
#
#   Parameters:
#   - api_key: API access key.
#   - journal_id: a journal id.
#
#   Journal IDs may be found here:
#   http://link.springer.com/search?facet-content-type=%22Journal%22
def springer_integro_api(journal_name, user = None):
    print("NOT FUNCTIONAL.")
    
    find_url = "https://link.springer.com/search?query=%22" + str(journal_name) + "%22&facet-content-type=%22Journal%22"
    
    r = requests.get(find_url, headers={"Content-Type": "application/json"})
    
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    else:

        soup = BeautifulSoup(r.text, 'html.parser')
        soup.prettify()

        results = []
        for result in soup.find_all("a", {"class": "title"}):
            journal_title = result.text
            if "/journal/" in result["href"]:
                journal_id = result["href"].split("/journal/")[1]
                results.append({
                    'title': journal_title,
                    'journal_id': journal_id
                })
            
        secondary_results = {}
        for result in results:
            if user is not None:
                if user.springer_api_key is not None:

                    base = "http://integro.nkb3.org/v1/journaltitlesheet/"
                    ext = result["journal_id"] + "?api_key=" + str(user.springer_api_key)

                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        
                        e = xml.etree.ElementTree.fromstring(r.text)
                        
                        publisher_obj = e.find("Publisher")
                        online_first_article_count = int(e.find("OnlineFirstArticleCount").text)
                        article_count = int(e.find("ArticleCount").text)
                        
                        result_dict = {}
                        
                        for child in publisher_obj.getchildren():
                            print(child.tag)
                            if child.tag == "PublisherInfo":
                                for subchild in child:
                                    if subchild.tag == "PublisherName":
                                        result_dict["publisher"] = subchild.text.strip()
                                    elif subchild.tag == "PublisherLocation":
                                        result_dict["publisher_location"] = subchild.text.strip()
                                    elif subchild.tag == "PublisherImprintName":
                                        result_dict["publisher_imprint_name"] = subchild.text.strip()
                                
                            elif child.tag == "Journal":
                                for subchild in child:
                                    if subchild.tag == "JournalInfo":
                                        for infrachild in subchild:
                                            if infrachild.tag == "JournalID":
                                                result_dict["journal_id"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalDOI":
                                                result_dict["journal_doi"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalPrintISSN":
                                                result_dict["journal_print_issn"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalElectronicISSN":
                                                result_dict["journal_electronic_issn"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalTitle":
                                                result_dict["journal_title"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalSubTitle":
                                                result_dict["journal_subtitle"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalAbbreviatedTitle":
                                                result_dict["journal_abbreviated_title"] = infrachild.text.strip()
                                            elif infrachild.tag == "JournalSubjectGroup":
                                                subject_group = {}
                                                subject_collection = {}
                                                for subinfrachild in infrachild:
                                                    if subinfrachild.tag == "JournalSubject":
                                                        code = subinfrachild.attrib["Code"]
                                                        subject_group[code] = {}
                                                        
                                                        subj_type = subinfrachild.attrib["Type"]
                                                        subject_group[code]["type"] = subj_type
                                                        
                                                        subj = subinfrachild.text.strip()
                                                        subject_group[code]["subject"] = subj
                                                        
                                                        if "Priority" in subinfrachild.attrib:
                                                            priority = subinfrachild.attrib["Priority"]
                                                            subject_group[code]["priority"] = priority
                                                    elif subinfrachild.tag == "JournalSubjectGroup":
                                                        subject_collection[subinfrachild.attrib["Code"]] = subinfrachild.text.strip()
                                                        
                                                result_dict["subject_group"] = subject_group
                                                result_dict["subject_collection"] = subject_collection
                                
                            elif child.tag == "{http://www.springer.com/app/meta}Info":
                                for subchild in child:
                                    # TODO: Finish this!
                                    print()
                        
                        return result_dict
                    
                else:
                    print("A valid Springer API is required to access the Springer API.")
            else:
                print("A valid user object with a valid Springer API key is required to access the Springer API.")
    
#   UNIT TESTS
def springer_unit_tests(query, journal_name, springer_api_key):
    user = User(springer_api_key = springer_api_key)
    
    print("\nObtaining information from journal query '%s'...\n" % str(journal_name))
    print(springer_integro_api(journal_name, user = user))

    print("Obtaining Springer documents from metadata query '%s'...\n" % str(query))
    for ref in springer_metadata_service(query, user = user):
        for iden in ref.identifiers:
            print("- %s (%s) [%s]" % (iden["name"].encode("ascii", errors="ignore").decode(), iden["identifier"], iden["identifier_type"]))
            
    print("\nObtaining Springer documents from meta query '%s'...\n" % str(query))
    for ref in springer_meta_api_service(query, user = user):
        for iden in ref.identifiers:
            print("- %s (%s) [%s]" % (iden["name"].encode("ascii", errors="ignore").decode(), iden["identifier"], iden["identifier_type"]))
            
    print("\nObtaining Springer documents from open-access query '%s'...\n" % str(query))
    for ref in springer_openaccess_api(query, user = user):
        for iden in ref.identifiers:
            print("- %s (%s) [%s]" % (iden["name"].encode("ascii", errors="ignore").decode(), iden["identifier"], iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()