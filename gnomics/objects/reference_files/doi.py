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
#   Get DOI.
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
import gnomics.objects.disease
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
import isbnlib
import json
import re
import requests
import xml.etree.ElementTree

#   MAIN
def main():
    doi_unit_tests("28723805", "CHEMBL1128639")

#   Get DOI object.
def get_doi_object(ref):
    doi_obj_array = []
    
    for ref_obj in ref.reference_objects:
        if 'object_type' in ref_obj:
            if ref_obj['object_type'].lower() in ["doi", "digital object", "digital object id", "digital object identifier", "doi object"]:
                doi_obj_array.append(ref_obj['object'])
    
    if doi_obj_array:
        return doi_obj_array
    
    for doi in get_doi(ref):
        base = "https://api.crossref.org/works/"
        ext = str(doi)

        r = requests.get(base+ext, headers={"Content-Type": "application/xml"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = json.loads(r.text)
            
            gnomics.objects.reference.Reference.add_object(ref, obj=decoded, object_type="DOI")
            doi_obj_array.append(decoded)
            
    return doi_obj_array
    
#   Get DOI.
def get_doi(ref): 
    doi_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["doi", "digital object id", "digital object identifier"]:
            doi_array.append(ident["identifier"])
            
    if doi_array:
        return doi_array
    
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["pmid", "pubmed id", "pubmed identifier"]:
            
            base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
            ext = "db=pubmed&id=" + str(ident["identifier"]) + "&retmode=xml"
        
            r = requests.get(base+ext, headers={"Content-Type": "application/xml"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            e = xml.etree.ElementTree.fromstring(r.text)
            for child in e.findall("PubmedArticle"):
                for subchild in child.findall("PubmedData"):
                    for infrachild in subchild.findall("ArticleIdList"):
                        for subinfrachild in infrachild.findall("ArticleId"):
                            if subinfrachild.attrib["IdType"] == "doi":
                                if subinfrachild.text not in doi_array:
                                    doi_array.append(subinfrachild.text)
                                    gnomics.objects.reference.Reference.add_identifier(ref, identifier=subinfrachild.text, identifier_type="DOI", source="PubMed")
                                    
        elif ident["identifier_type"].lower() in ["chembl", "chembl id", "chembl identifier"]:
            for obj in gnomics.objects.reference.Reference.chembl_document(ref):
                if "doi" in obj:
                    doi_array.append(obj["doi"])
                    
        elif ident["identifier_type"].lower() == "isbn-13" or ident["identifier_type"].lower() == "isbn13":
            doi_array.append(isbnlib.doi(ident["identifier"]))
            
    return doi_array
        
#   UNIT TESTS
def doi_unit_tests(pmid, chembl_id):
    print("Getting DOI from PubMed ID (%s):" % pmid)
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for doi in get_doi(pubmed_ref):
        print("- %s" % doi)
        
    print("\nGetting DOI from ChEMBL ID (%s):" % chembl_id)
    chembl_ref = gnomics.objects.reference.Reference(identifier = chembl_id, identifier_type = "ChEMBL ID", language = None, source = "ChEMBL")
    for doi in get_doi(chembl_ref):
        print("- %s" % doi)
    

#   MAIN
if __name__ == "__main__": main()