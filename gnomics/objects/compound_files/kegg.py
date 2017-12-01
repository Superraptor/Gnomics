#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get KEGG compound identifiers.
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
from bioservices import *
import pubchempy as pubchem

#   MAIN
def main():
    kegg_unit_tests("CHEBI:4911", "C01576")
    
#   KEGG database entry (for compound).
def get_kegg_compound_db_entry(compound):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'kegg compound':
                return com_obj['object']
    s = KEGG()
    res = s.get("cpd:" + gnomics.objects.compound.Compound.kegg_compound_id(compound))
    parsed_obj = s.parse(res)
    compound.compound_objects.append(
        {
            'object': parsed_obj,
            'object_type': "KEGG COMPOUND"
        }
    )
    return parsed_obj

#   Get KEGG compound identifier.
def get_kegg_compound_id(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "kegg compound accession":
                    com.identifiers.append(
                        {
                            'identifier': accession._DatabaseAccession__accession_number,
                            'language': None,
                            'identifier_type': "KEGG COMPOUND accession",
                            'source': "ChEBI"
                        }
                    )
                    return accession._DatabaseAccession__accession_number

#   UNIT TESTS
def kegg_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting KEGG Compound ID from ChEBI ID (%s):" % chebi_id)
    print("- %s" % str(get_kegg_compound_id(chebi_com)))

#   MAIN
if __name__ == "__main__": main()