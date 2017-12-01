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

#   MAIN
def main():
    chemspider_unit_tests("LIQODXNTTZAGID-OCBXBXKTSA-N", "")
    
#   Get ChemSpider compound.
def get_chemspider_compound(compound, user = None):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'chemspider compound' or com_obj['object_type'].lower() == 'chemspider':
                return com_obj['object']
    if user is not None and user.chemspider_security_token is not None:
        cs = chemspider(user.chemspider_security_token)
        chemspider_compound = cs.get_compound(gnomics.objects.compound.Compound.chemspider_id(compound, user = user))
        compound.compound_objects.append(
            {
                'object': chemspider_compound,
                'object_type': "ChemSpider compound"
            }
        )
        return chemspider_compound
    else:
        print("Cannot obtain a ChemSpider compound object without a valid user and ChemSpider security token. Please try again after provided such a user object.")

#   Get ChemSpider ID.
def get_chemspider_id(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "inchi" and user is not None:
            result_set = []
            cs = chemspider(user.chemspider_security_token)
            for result in cs.search(ident["identifier"]):
                temp_com = gnomics.objects.compound.Compound(identifier = result.csid, identifier_type = "ChemSpider ID", source = "ChemSpider")
                result_set.append(result.csid)
            return result_set
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")

#   UNIT TESTS
def chemspider_unit_tests(inchi_id, chemspider_security_token):
    user = User(chemspider_security_token = chemspider_security_token)
    inchi_compound = gnomics.objects.compound.Compound(identifier = str(inchi_id), identifier_type = "InChi", source = "PubChem")
    print("Getting ChemSpider ID from InChI (%s):" % inchi_id)
    for com in get_chemspider_id(inchi_compound, user = user):
        print("- " + str(com))

#   MAIN
if __name__ == "__main__": main()