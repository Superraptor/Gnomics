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
import pubchempy as pubchem

#   MAIN
def main():
    iupac_unit_tests("36462")

#   Get IUPAC.
def get_iupac_name(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "iupac name":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.pubchem_compound(com).iupac_name,
                    'language': None,
                    'identifier_type': "IUPAC name",
                    'source': "PubChem"
                }
            )
            return gnomics.objects.compound.Compound.pubchem_compound(com).iupac_name

#   UNIT TESTS
def iupac_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting IUPAC name from PubChem CID (%s):" % pubchem_cid)
    print("- %s" % str(get_iupac_name(pubchem_com)))

#   MAIN
if __name__ == "__main__": main()