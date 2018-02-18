#!/usr/bin/env python

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
import timeit

#   MAIN
def main():
    pdbechem_unit_tests("CHEBI:16125", "C00823")

# Returns PDBeChem accession.
def get_pdbechem_id(com, user=None):
    pdb_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["pdbechem", "pdbechem id", "pdbechem identifier", "pdbechem accession"]):
        if iden["identifier"] not in pdb_array:
            pdb_array.append(iden["identifier"])
            
    if pdb_array:
        return pdb_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "pdbechem accession" and accession._DatabaseAccession__accession_number not in pdb_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier=accession._DatabaseAccession__accession_number, identifier_type="PDBeChem Accession", language=None, source="ChEBI")
                        pdb_array.append(accession._DatabaseAccession__accession_number)
         
    if pdb_array:
        return pdb_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_pdbechem_id(com)
    
    return pdb_array

#   UNIT TESTS
def pdbechem_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("\nGetting PDBeChem accession from ChEBI ID (%s):" % chebi_id)
    start = timeit.timeit()
    pdb_array = get_pdbechem_id(chebi_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in pdb_array:
        print("\t- %s" % str(com))
        
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting PDBeChem accession from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    pdb_array = get_pdbechem_id(kegg_compound_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in pdb_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()