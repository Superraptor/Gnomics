#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIBGEN
#           https://github.com/etlapale/bibgen
#       BIOPYTHON
#           http://biopython.org/
#       METAPUB
#           https://pypi.python.org/pypi/metapub
#       PUBMED-LOOKUP
#           https://pypi.python.org/pypi/pubmed-lookup
#

#
#   Get PMC ID.
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
import xml.etree.ElementTree

#   MAIN
def main():
    pmc_unit_tests("28723805")

#   Get PMC ID.
def get_pmc_id(ref): 
    pmc_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["pmc", "pmcid", "pmc id", "pmc identifier"]:
            pmc_array.append(ident["identifier"])
            
    if pmc_array:
        return pmc_array
    
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["pmid", "pubmed", "pubmed id", "pubmed identifier"]:
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
                            if subinfrachild.attrib["IdType"] == "pmc":
                                if subinfrachild.text not in pmc_array:
                                    pmc_array.append(subinfrachild.text)
                                    gnomics.objects.reference.Reference.add_identifier(ref, identifier=subinfrachild.text, identifier_type="PMC ID", source="PubMed")
            
    return pmc_array
        
#   UNIT TESTS
def pmc_unit_tests(pmid):
    print("Getting DOI from PubMed ID (%s):" % pmid)
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for pmc in get_pmc_id(pubmed_ref):
        print("- %s" % pmc)

#   MAIN
if __name__ == "__main__": main()