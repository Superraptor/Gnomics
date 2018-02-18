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
#   Parse and create citations.
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
import tempfile
import xml.etree.ElementTree

#   MAIN
def main():
    citation_unit_tests()

#   Get identifiers from citation.
#
#   Parameters:
#   - score_threshold
#   - normalized_score_threshold
def parse_citation(citation, score_threshold=None, normalized_score_threshold=100): 
    
    # Find DOI from CrossRef.
    base = "http://search.crossref.org"
    ext = "/dois?q=" + citation
    
    r = requests.get(base+ext, headers = {"Content-Type": "application/json"})
        
    if not r.ok:
        r.raise_for_status()
        sys.ext()

    decoded = r.json()
    
    doi_list = []
    for potential_ref in decoded:
        if normalized_score_threshold is not None and score_threshold is None:
            if potential_ref["normalizedScore"] >= normalized_score_threshold:
                print(potential_ref["normalizedScore"])
                doi_list.append(potential_ref["doi"].split("http://dx.doi.org/")[1])
        elif score_threshold is not None and normalized_score_threshold is None:
            if potential_ref["score"] >= score_threshold:
                print(potential_ref["score"])
                doi_list.append(potential_ref["doi"].split("http://dx.doi.org/")[1])
        else:
            if potential_ref["score"] >= score_threshold and potential_ref["normalizedScore"] >= normalized_score_threshold:
                print(potential_ref["score"])
                doi_list.append(potential_ref["doi"].split("http://dx.doi.org/")[1])
            
    final_refs = []
    for doi in doi_list:
        temp_ref = gnomics.objects.reference.Reference(identifier = doi, identifier_type = "DOI", source = "CrossRef")
        final_refs.append(temp_ref)
                    
    return final_refs
        
#   UNIT TESTS
def citation_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()