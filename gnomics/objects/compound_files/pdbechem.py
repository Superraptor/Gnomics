#
#
#
#
#

#
#   IMPORT SOURCES:
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get PDBeChem IDs.
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
from libchebipy import ChebiEntity, ChebiException, Comment, CompoundOrigin, DatabaseAccession, Formula, Name, Reference, Relation, Structure
import pubchempy as pubchem

#   MAIN
def main():
    pdbechem_unit_tests("CHEBI:16125", "C00823")

# Returns PDBeChem accession.
def get_pdbechem_id(com):
    pdbechem_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pdbechem accession" or ident["identifier_type"].lower() == "pdbechem":
            if ident["identifier"] not in pdbechem_array:
                pdbechem_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "pdbechem accession":
                    if ident["identifier"] not in pdbechem_array:
                        com.identifiers.append({
                            'identifier': accession._DatabaseAccession__accession_number,
                            'language': None,
                            'identifier_type': "PDBeChem accession",
                            'source': "ChEBI"
                        })
                        pdbechem_array.append(accession._DatabaseAccession__accession_number)
            return pdbechem_array
    if pdbechem_array:
        return pdbechem_array
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_pdbechem_id(com)

#   UNIT TESTS
def pdbechem_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting PDBeChem accession from ChEBI ID (%s):" % chebi_id)
    for com in get_pdbechem_id(chebi_com):
        print("- %s" % str(com))
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting PDBeChem accession from KEGG Compound ID (%s):" % kegg_compound_id)
    for com in get_pdbechem_id(kegg_compound_com):
        print("- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()