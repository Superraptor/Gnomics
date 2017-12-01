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

#   MAIN
def main():
    formula_unit_tests("33510", "36462", "")

#   Get molecular formula.
def get_molecular_formula(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "molecular formula":
            return ident["identifier"]
    for ident in com.identifiers:
        # Note that ChemSpider includes formatting, for example:
        # C_{29}H_{32}O_{13}
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user).molecular_formula,
                'language': None,
                'identifier_type': "Molecular formula",
                'source': "ChemSpider"
            })
            return get_molecular_formula(com, user)
        # Note that PubChem includes no formatting, for example:
        # C29H32O13
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.pubchem_compound(com, user).molecular_formula,
                'language': None,
                'identifier_type': "Molecular formula",
                'source': "PubChem"
            })
            return get_molecular_formula(com, user)

#   UNIT TESTS
def formula_unit_tests(chemspider_id, pubchem_cid, chemspider_security_token):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting molecular formula from ChemSpider ID (%s):" % chemspider_id)
        print("- %s" % str(get_molecular_formula(chemspider_com, user = user)))
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting molecular formula from PubChem CID (%s):" % pubchem_cid)
        print("- %s" % str(get_molecular_formula(pubchem_com)))
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with PubChem CID conversion...\n")
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("Getting molecular formula from PubChem CID (%s):" % pubchem_cid)
        print("- %s" % str(get_molecular_formula(pubchem_com)))

#   MAIN
if __name__ == "__main__": main()