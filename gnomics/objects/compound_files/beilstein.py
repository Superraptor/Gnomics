#
#
#
#
#

#
#   IMPORT SOURCES:
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#

#
#   Get Beilstein registry number.
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
import gnomics.objects.compound

#   Other imports.

#   MAIN
def main():
    beilstein_unit_tests("CHEBI:2663", "C06823")

#   Get Beilstein registry number.
def get_beilstein(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "beilstein" or ident["identifier_type"].lower() == "beilstein registry number":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "beilstein registry number":
                    beilstein_rn = accession._DatabaseAccession__accession_number
                    com.identifiers.append(
                        {
                            'identifier': beilstein_rn,
                            'language': None,
                            'identifier_type': "Beilstein Registry Number",
                            'source': "ChEBI"
                        }
                    )
                    return beilstein_rn
            print("No corresponding Beilstein registry number was found.")
            return ""
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_beilstein(com)

#   UNIT TESTS
def beilstein_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting Beilstein registry number from ChEBI ID (%s):" % chebi_id)
    print("- " + str(get_beilstein(chebi_com)) + "\n")
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("Getting Beilstein registry number from KEGG Compound ID (%s):" % kegg_compound_id)
    print("- " + str(get_beilstein(kegg_compound_com)))

#   MAIN
if __name__ == "__main__": main()