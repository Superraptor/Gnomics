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
#   Get OCLC.
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
import bs4
import json
import re
import requests
import xml.etree.ElementTree

#   MAIN
def main():
    oclc_unit_tests("0679442723", "57358293", "0027-1535", "2011588147", "", "", "potato")
    
#   Return OCLC Control Number.
def oclc_control_number(reference):
    oclc_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["oclc control number", "oclc number", "oclc"]):
        if iden["identifier"] not in oclc_array:
            oclc_array.append(iden["identifier"])
    
    if oclc_array:
        return oclc_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["openlibrary", "openlibrary id", "openlibrary identifier", "olid"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["oclc"] not in oclc_array:
                oclc_array.append(obj["oclc"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["oclc"], identifier_type="OCLC Control Number", source="OpenLibrary", language=None)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["oclc"] not in oclc_array:
                oclc_array.append(obj["oclc"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["oclc"], identifier_type="OCLC Control Number", source="OpenLibrary", language=None)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(reference.identifiers, ["lccn", "library of congress control number"]):
        for obj in gnomics.reference.Reference.openlibrary(ref):
            if obj["oclc"] not in oclc_array:
                oclc_array.append(obj["oclc"])
                gnomics.objects.reference.Reference.add_identifier(reference, identifier=obj["oclc"], identifier_type="OCLC Control Number", source="OpenLibrary", language=None)
    
    return oclc_array

#   Availability Query.
def availability_query():
    print("NOT FUNCTIONAL.")
    
#   Find a Library.
def find_a_library():
    print("NOT FUNCTIONAL.")
    
#   WorldCat Knowledge Base API.
#
#   Currently, only search queries
#   are available for this function
#   (specifically the entry search
#   functionality).
def worldcat_knowledge_base_api(query, user=None):
    print("NOT FUNCTIONAL.")
    
#   WorldCat Search API.
def worldcat_search_api(query, user=None):
    result_array = []
    
    if user is not None:
        base = "http://www.worldcat.org/webservices"
        ext = "/catalog/search/worldcat/opensearch?q=" + str(query) + "&wskey=" + user.oclc_api_key
        r = requests.get(base+ext, headers={"Content-Type": "application/xml"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            soup = BeautifulSoup(r.text, 'xml')
            soup.prettify()
            
            entries = soup.find_all("entry")
            
            if entries:
                for entry in entries:
                    temp_ref = gnomics.objects.reference.Reference()
                    for child in entry:
                        if isinstance(child, bs4.Tag):
                            if "urn:ISBN:" in child.text:
                                isbn = child.text.split("urn:ISBN:")[1]
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=isbn, identifier_type="ISBN", source="OCLC", language=None)
                            elif "http://worldcat.org/oclc/" in child.text:
                                oclc = child.text.split("http://worldcat.org/oclc/")[1]
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=oclc, identifier_type="OCLC Control Number", source="OCLC", language=None)
                            elif "urn:LCCN:" in child.text:
                                lccn = child.text.split("urn:LCCN:")[1]
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=lccn, identifier_type="LCCN", source="OCLC", language=None)
                            elif "urn:ISSN:" in child.text:
                                issn = child.text.split("urn:ISSN:")[1]
                                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier=issn, identifier_type="ISSN", source="OCLC", language=None)
                                
                    result_array.append(temp_ref)
                        
    return result_array
    
#   WorldCat Metadata API.
def worldcat_metadata_api():
    print("NOT FUNCTIONAL.")
    
#   Classify books, videos, CDs, and other materials.
#
#   For more information, see API docs here:
#   https://www.oclc.org/developer/develop/web-services/classify/classification.en.html
def classify(ref, return_type="ddc"):
    ddc_array = []
    lcc_array = []
    
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["isbn", "isbn10", "isbn13", "isbn-10", "isbn-13"]:
            
            base = "http://classify.oclc.org/classify2/"
            ext = "Classify?isbn=" + re.sub("[^0-9]", "", ident["identifier"]) + "&summary=true"
            r = requests.get(base+ext, headers={"Content-Type": "application/xml"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                
                soup = BeautifulSoup(r.text, 'xml')
                soup.prettify()
                
                ddc = soup.find("ddc")
                if ddc:
                    for child in ddc.findChildren():
                        code = child.attrs["sfa"]
                        ddc_array.append(code)
                
                lcc = soup.find("lcc")
                if lcc:
                    for child in lcc.findChildren():
                        code = child.attrs["sfa"]
                        lcc_array.append(code)
            
        elif ident["identifier_type"].lower() in ["oclc", "oclc number", "oclc control number"]:
            
            base = "http://classify.oclc.org/classify2/"
            ext = "Classify?oclc=" + re.sub("[^0-9]", "", ident["identifier"]) + "&summary=true"
            r = requests.get(base+ext, headers={"Content-Type": "application/xml"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                
                soup = BeautifulSoup(r.text, 'html.parser')
                soup.prettify()
                
                ddc = soup.find("ddc")
                if ddc:
                    for child in ddc.findChildren():
                        code = child.attrs["sfa"]
                        ddc_array.append(code)
                
                lcc = soup.find("lcc")
                if lcc:
                    for child in lcc.findChildren():
                        code = child.attrs["sfa"]
                        lcc_array.append(code)
                        
        elif ident["identifier_type"].lower() in ["issn"]:
            
            base = "http://classify.oclc.org/classify2/"
            ext = "Classify?oclc=" + re.sub("[^0-9]", "", ident["identifier"]) + "&summary=true"
            r = requests.get(base+ext, headers={"Content-Type": "application/xml"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                
                soup = BeautifulSoup(r.text, 'html.parser')
                soup.prettify()
                
                ddc = soup.find("ddc")
                if ddc:
                    for child in ddc.findChildren():
                        code = child.attrs["sfa"]
                        ddc_array.append(code)
                
                lcc = soup.find("lcc")
                if lcc:
                    for child in lcc.findChildren():
                        code = child.attrs["sfa"]
                        lcc_array.append(code)
                        
        elif ident["identifier_type"].lower() in ["lccn", "library of congress control number"]:
            
            base = "http://classify.oclc.org/classify2/"
            ext = "Classify?oclc=" + re.sub("[^0-9]", "", ident["identifier"]) + "&summary=true"
            r = requests.get(base+ext, headers={"Content-Type": "application/xml"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                
                soup = BeautifulSoup(r.text, 'html.parser')
                soup.prettify()
                
                ddc = soup.find("ddc")
                if ddc:
                    for child in ddc.findChildren():
                        code = child.attrs["sfa"]
                        ddc_array.append(code)
                
                lcc = soup.find("lcc")
                if lcc:
                    for child in lcc.findChildren():
                        code = child.attrs["sfa"]
                        lcc_array.append(code)
    
    if return_type.lower() == "lcc":
        return lcc_array
    else:
        return ddc_array
        
#   UNIT TESTS
def oclc_unit_tests(isbn, oclc, issn, lccn, oclc_wskey, oclc_wskey_secret, query):
    user = User(oclc_api_key=oclc_wskey)
    
    for result in worldcat_search_api(query, user=user):
        for iden in result.identifiers:
            print("- %s [%s]" % (iden["identifier"], iden["identifier_type"]))
    
    isbn_ref = gnomics.objects.reference.Reference(identifier = isbn, identifier_type = "ISBN", language = None, source = "Open Library")
    print(classify(isbn_ref))
    
    oclc_ref = gnomics.objects.reference.Reference(identifier = oclc, identifier_type = "OCLC Control Number", language = None, source = "Open Library")
    print(classify(oclc_ref))
    
    issn_ref = gnomics.objects.reference.Reference(identifier = oclc, identifier_type = "ISSN", language = None, source = "Open Library")
    print(classify(issn_ref))
    
    lccn_ref = gnomics.objects.reference.Reference(identifier = oclc, identifier_type = "LCCN", language = None, source = "Open Library")
    print(classify(lccn_ref))

#   MAIN
if __name__ == "__main__": main()