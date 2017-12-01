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
#   Get PII.
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
import pdfx
import re
import requests
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree

#   MAIN
def main():
    pii_unit_tests("28723805")

#   Get PII (Publisher Item Identifier).
def get_pii(ref): 
    pii_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "pii" or ident["identifier_type"].lower() == "publisher item id" or ident["identifier_type"].lower() == "publisher item identifier":
            pii_array.append(ident["identifier"])
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier":
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
                            if subinfrachild.attrib["IdType"] == "pii":
                                if subinfrachild.text not in pii_array:
                                    pii_array.append(subinfrachild.text)
                                    gnomics.objects.reference.Reference.add_identifier(ref, identifier=subinfrachild.text, identifier_type="PII", source="PubMed")
    return pii_array
        
#   UNIT TESTS
def pii_unit_tests(pmid):
    print("Getting DOI from PubMed ID (%s):" % pmid)
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for pii in get_pii(pubmed_ref):
        print("- %s" % pii)

#   MAIN
if __name__ == "__main__": main()