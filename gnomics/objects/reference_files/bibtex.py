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
#   Get BibTeX.
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
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.customization import *
import bibtexparser
import isbnlib

#   MAIN
def main():
    bibtex_unit_tests("10.1055/s-0043-124191")
    
#   Return metadata as BibTeX.
def get_bibtex(ref):
    bibtex_array = []
    for ident in ref.identifiers:
        if ident["identifier_type"].lower() in ["doi", "digital object", "digital object id", "digital object identifier", "doi object"]:
            bibtex_array.append(isbnlib.doi2tex(ident["identifier"]))
    return bibtex_array
    
#   Open bibtex file.
def open_bibtex_file(filename):
    if os.path.exists(filename):
        with open(filename) as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
            return bib_database
    else:
        print("Provided file does not exist.")
        return
    
#   Write bibtex file.
def write_bibtex_file(bib_database, output_name):
    writer = BibTexWriter()
    with open(output_name, "w") as bibtex_file:
        bibtex_file.write(writer.write(bib_database))
    
#   UNIT TESTS
def bibtex_unit_tests(doi):
    print("Getting BibTeX from DOI (%s):" % doi)
    doi_ref = gnomics.objects.reference.Reference(identifier = doi, identifier_type = "DOI", language = None, source = "PubMed")
    for bibtex in get_bibtex(doi_ref):
        print(bibtex)

#   MAIN
if __name__ == "__main__": main()