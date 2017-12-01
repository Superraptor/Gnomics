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
#   Perform NLP.
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
from bioservices import *
import json
import re
import requests
import shutil
import subprocess
import tempfile

#   MAIN
def main():
    noble_unit_tests("28723805")
    
# Perform NLP.
def nlp(pubmed_ref = None, pmid = None):
    if pmid is not None:
        pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
        abstract_text = gnomics.objects.reference.Reference.abstract(pubmed_ref)
        print("NLP at BioLink has not yet been implemented, further details available here: %s" % ("https://api.monarchinitiative.org/api/#/nlp/annotate"))
        return ""
    elif pubmed_ref is not None:
        for ident in pubmed_ref.identifiers:
            if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed identifier" or ident["identifier_type"].lower() == "pubmed":
                abstract_text = gnomics.objects.reference.Reference.abstract(pubmed_ref)
                print("NLP at BioLink has not yet been implemented, further details available here: %s" % ("https://api.monarchinitiative.org/api/#/nlp/annotate"))
                return ""
    elif pubmed_ref is None and pmid is None:
        print("A PubMed reference object or a PMID must be provided in order to use PubTator.")
        return ""
    else:
        print("An unknown error occurred.")
        return ""
        
#   UNIT TESTS
def noble_unit_tests(pmid):
    print("Getting Noble results from raw PMID...")
    for thing in nlp(pmid = pmid):
        print("- %s" % thing)
    print("\nGetting Noble results from PubMed reference...")
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for thing in nlp(pubmed_ref = pubmed_ref):
        print("- %s" % thing)

#   MAIN
if __name__ == "__main__": main()