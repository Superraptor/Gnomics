#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get various KEGG compound identifiers.
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
import gnomics.objects.drug

#   MAIN
def main():
    kegg_unit_tests()

#	Get KEGG drug identifier.
def get_kegg_drug_id(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg drug" or ident["identifier_type"].lower() == "kegg drug id" or ident["identifier_type"].lower() == "kegg drug accession":
            return ident["identifier"]

#   UNIT TESTS
def kegg_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()