#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMSPIPY
#           http://chemspipy.readthedocs.io/en/latest/
#

#
#   Get various common names.
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
import gnomics.objects.compound

#   Other imports.
import pubchempy as pubchem

#   MAIN
def main():
    common_names_unit_tests("33510", "")
	
#	Get common names.
def get_common_names(com, user = None):
    common_name_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "common name":
            common_name_array.append(ident["identifier"])
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            temp_common = gnomics.objects.compound.Compound.chemspider_compound(com, user).common_name
            if temp_common not in common_name_array:
                com.identifiers.append(
                    {
                        'identifier': temp_common,
                        'language': "English",
                        'identifier_type': "Common Name",
                        'source': "ChemSpider"
                    }
                )
                common_name_array.append(temp_common)
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    return common_name_array

#   UNIT TESTS
def common_names_unit_tests(chemspider_id, chemspider_security_token = None):
    if chemspider_security_token:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting common names from ChemSpider ID (%s):" % chemspider_id)
        for com in get_common_names(chemspider_com, user = user):
            print("- %s" % str(com))
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.")

#   MAIN
if __name__ == "__main__": main()