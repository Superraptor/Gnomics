#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get molecular formula.
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
import timeit

#   MAIN
def main():
    formula_unit_tests("33510", "36462", "")

#   Get molecular formula.
def get_molecular_formula(com, user=None):
    molec_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["molecular formula"]):
        if iden["identifier"] not in molec_array:
            molec_array.append(iden["identifier"])
            
    if molec_array:
        return molec_array
    
    ids_completed = []
    
    # Note that ChemSpider includes formatting, for example:
    # C_{29}H_{32}O_{13}
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                temp_molec = sub_com.molecular_formula
                if temp_molec not in molec_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier=temp_molec, identifier_type="Molecular Formula", language=None, source="ChemSpider")
                    molec_array.append(temp_molec)
                
        elif user is None:
            
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    
    # Note that PubChem includes no formatting, for example:
    # C29H32O13
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
    
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com, user):
                temp_molec = sub_com.molecular_formula
                if temp_molec not in molec_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier=temp_molec, identifier_type="Molecular Formula", language=None, source="PubChem")
                    molec_array.append(temp_molec)
        
    return molec_array

#   UNIT TESTS
def formula_unit_tests(chemspider_id, pubchem_cid, chemspider_security_token):
    if chemspider_security_token is not None:
        
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("\nGetting molecular formula from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        molec_array = get_molecular_formula(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in molec_array:
            print("\t- %s" % str(com))
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting molecular formula from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        molec_array = get_molecular_formula(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in molec_array:
            print("\t- %s" % str(com))
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with PubChem CID conversion...\n")
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting molecular formula from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        molec_array = get_molecular_formula(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in molec_array:
            print("\t- %s" % str(com))
        

#   MAIN
if __name__ == "__main__": main()