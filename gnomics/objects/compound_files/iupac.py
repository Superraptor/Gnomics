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
#   Get IUPAC name.
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
    iupac_unit_tests("36462")

#   Get IUPAC.
def get_iupac_name(com, user=None):
    
    iupac_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["iupac", "iupac name"]):
        if iden["identifier"] not in iupac_array:
            iupac_array.append(iden["identifier"])
            
    if iupac_array:
        return iupac_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com):
                temp_iupac = sub_com.iupac_name
                if temp_iupac not in iupac_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_iupac, identifier_type = "IUPAC Name", language = None, source = "PubChem")
                    iupac_array.append(temp_iupac)
                
    return iupac_array

#   UNIT TESTS
def iupac_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting IUPAC name from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    iupac_array = get_iupac_name(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in iupac_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()