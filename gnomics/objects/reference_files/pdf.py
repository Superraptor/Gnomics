#
#
#
#
#

#
#   IMPORT SOURCES:
#       METAPUB
#           https://pypi.python.org/pypi/metapub
#       PDFX
#           https://pypi.python.org/pypi/pdfx
#

#
#   Get reference PDF (if it exists).
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
from metapub import FindIt
import json
import pdfx
import re
import requests
import shutil
import subprocess
import tempfile

#   MAIN
def main():
    pdf_unit_tests("28723805", "10.1038/nature23305")

#   Get PDF URL.
def get_pdf(ref): 
    pdf_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier":
            src = FindIt(ident["identifier"])
            if src.url is None:
                print(src.reason)
            elif src.url not in pdf_array:
                pdf_array.append(src.url)
        elif ident["identifier_type"].lower() == "doi" or ident["identifier_type"].lower() == "digital object id" or ident["identifier_type"].lower() == "digital object identifier":
            src = FindIt(doi=ident["identifier"])
            if src.url is None:
                print(src.reason)
            elif src.url not in pdf_array:
                pdf_array.append(src.url)
    return pdf_array

#   Extract information from PDF.
def pdf_metadata(pdf_url):
    pdf = pdfx.PDFx(pdf_url)
    metadata = pdf.get_metadata()
    return metadata

#   Extract references from PDF.
def pdf_references(pdf_url, return_type="dict"):
    pdf = pdfx.PDFx(pdf_url)
    if return_type is None or return_type == "list":
        reference_list = pdf.get_references()
        return reference_list
    elif return_type == "dict":
        reference_dict = pdf.get_references_as_dict()
        return reference_dict
    else:
        print("The given return type, '%s', is not available... Returning a dictionary instead...")
        pdf_references(pdf_url, return_type="dict")
        
#   Download all reference PDFs.
def pdf_reference_pdfs(pdf_url, target_directory="../../data")
    pdf = pdfx.PDFx(pdf_url)
    pdf.download_pdfs(target_directory)
        
#   UNIT TESTS
def pdf_unit_tests(pmid, doi):
    print("Getting PDF from PubMed ID (%s):" % pmid)
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for pdf in get_pdf(pubmed_ref):
        print("- %s" % pdf)
    print("Getting PDF from DOI (%s):" % doi)
    doi_ref = gnomics.objects.reference.Reference(identifier = doi, identifier_type = "DOI", language = None, source = "PubMed")
    for pdf in get_pdf(doi_ref):
        print("- %s" % pdf)

#   MAIN
if __name__ == "__main__": main()