#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYBTEX
#           https://docs.pybtex.org/
#

#
#   Get BibTeXML.
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
from pybtex.database import parse_file

#   MAIN
def main():
    bibtexml_unit_tests()
    
#   UNIT TESTS
def bibtexml_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()