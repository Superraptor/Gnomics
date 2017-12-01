#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get DrugCentral identifier.
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
import gnomics.objects.drug

#   MAIN
def main():
    drugcentral_unit_tests()

#   Get DrugCentral ID.
def get_drugcentral_id(drug):
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "drug central accession" or ident["identifier_type"].lower() == "drugcentral accession" or ident["identifier_type"].lower() == "drugcentral" or ident["identifier_type"].lower() == "drugcentral id" or ident["identifier_type"].lower() == "drugcentral identifier":
            return ident["identifier"]

#   UNIT TESTS
def drugcentral_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()