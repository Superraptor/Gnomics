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
#   Get LINCS accession.
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
    lincs_unit_tests("CHEBI:4911", "C01576")

#   Get LINCS ID.
def get_lincs_id(com):
    lincs_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "lincs accession" or ident["identifier_type"].lower() == "lincs":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "lincs accession":
                    com.identifiers.append({
                        'identifier': accession._DatabaseAccession__accession_number,
                        'language': None,
                        'identifier_type': "LINCS accession",
                        'source': "ChEBI"
                    })
                    lincs_array.append(accession._DatabaseAccession__accession_number)
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "lincs accession":
                    com.identifiers.append({
                        'identifier': accession._DatabaseAccession__accession_number,
                        'language': None,
                        'identifier_type': "LINCS accession",
                        'source': "ChEBI"
                    })
                    lincs_array.append(accession._DatabaseAccession__accession_number)
    return lincs_array

#   UNIT TESTS
def lincs_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting LINCS accession from ChEBI ID (%s):" % chebi_id)
    print("- %s" % str(get_lincs_id(chebi_com)))
    kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting LINCS accession from KEGG Compound ID (%s):" % kegg_compound_id)
    print("- %s" % str(get_lincs_id(kegg_com)))

#   MAIN
if __name__ == "__main__": main()