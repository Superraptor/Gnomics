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
#   Get RefSeq RNA.
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
    refseq_unit_tests()

# Returns RefSeq RNA ID.
def get_refseq_rna_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "refseq" or ident["identifier_type"].lower() == "refseq id" or ident["identifier_type"].lower() == "refseq identifier" or ident["identifier_type"].lower() == "refseq rna id" or ident["identifier_type"].lower() == "refseq rna identifier":
            return ident["identifier"]
        
#   UNIT TESTS
def refseq_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()