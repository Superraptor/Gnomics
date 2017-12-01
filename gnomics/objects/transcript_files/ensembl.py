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
#   Get Ensembl transcript.
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
import gnomics.objects.transcript

#   Other imports.
import requests

#   MAIN
def main():
    ensembl_unit_tests()

# Returns Ensembl transcript identifier.
def get_ensembl_transcript_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl transcript" or ident["identifier_type"].lower() == "ensembl transcript id" or ident["identifier_type"].lower() == "ensembl transcript identifier" or ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id":
            return ident["identifier"]
        
#   UNIT TESTS
def ensembl_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()