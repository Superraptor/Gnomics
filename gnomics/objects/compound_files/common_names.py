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
import timeit

#   MAIN
def main():
    common_names_unit_tests("33510", "fd4ce40f-23e5-44be-91f5-a40b92ab1580")
	
#	Get common names.
def get_common_names(com, user=None):
    common_name_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["common name", "vernacular name"]):
        if iden["identifier"] not in common_name_array:
            common_name_array.append(iden["identifier"])
            
    if common_name_array:
        return common_name_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                temp_common = sub_com.common_name
                if temp_common not in common_name_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier=temp_common, language="en", identifier_type="Common Name", source="ChemSpider")
                    common_name_array.append(temp_common)
    
        elif user is None:
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
        start = timeit.timeit()
        common_name_array = get_common_names(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in common_name_array:
            print("\t- %s" % str(com))
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.")

#   MAIN
if __name__ == "__main__": main()