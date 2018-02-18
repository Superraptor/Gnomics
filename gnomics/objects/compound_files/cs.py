#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMSPIPY
#           http://chemspipy.readthedocs.io/en/latest/
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get ChemSpider identifier.
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
from chemspipy import ChemSpider as chemspider
import pubchempy as pubchem
import timeit

#   MAIN
def main():
    chemspider_unit_tests("LIQODXNTTZAGID-OCBXBXKTSA-N", "")
    
#   Get ChemSpider compound.
def get_chemspider_compound(compound, user=None):
    
    chemspider_array = []
    
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['chemspider compound', 'chemspider']:
                chemspider_array.append(com_obj['object'])
            
    if chemspider_array:
        return chemspider_array
            
    if user is not None and user.chemspider_security_token is not None:
        for chemspider_id in gnomics.objects.compound.Compound.chemspider_id(compound, user = user):
            cs = chemspider(user.chemspider_security_token)
            chemspider_compound = cs.get_compound(chemspider_id)
            chemspider_array.append(chemspider_compound)
            gnomics.objects.compound.Compound.add_object(compound, obj=chemspider_compound, object_type = "ChemSpider Compound")
            
    else:
        print("Cannot obtain a ChemSpider compound object without a valid user and ChemSpider security token. Please try again after provided such a user object.")
        
    return chemspider_array

#   Get ChemSpider ID.
def get_chemspider_id(com, user=None):
    
    cs_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in cs_array:
            cs_array.append(iden["identifier"])
            
    if cs_array:
        return cs_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["inchi", "standard inchi", "iupac international chemical", "iupac international chemical id", "iupac international chemical identifier", "standard iupac international chemical", "standard iupac international chemical id", "standard iupac international chemical identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            cs = chemspider(user.chemspider_security_token)
            for result in cs.search(iden["identifier"]):
                if result.csid not in cs_array:
                    cs_array.append(result.csid)
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = result.csid, identifier_type = "ChemSpider ID", source = "ChemSpider", language = None)
            
        elif user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
            
    return cs_array

#   UNIT TESTS
def chemspider_unit_tests(inchi_id, chemspider_security_token):
    user = User(chemspider_security_token=chemspider_security_token)
    
    inchi_compound = gnomics.objects.compound.Compound(identifier = str(inchi_id), identifier_type = "InChi", source = "PubChem")
    print("Getting ChemSpider ID from InChI (%s):" % inchi_id)
    start = timeit.timeit()
    cs_array = get_chemspider_id(inchi_compound, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in cs_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()