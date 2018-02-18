#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       
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
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
import timeit

#   MAIN
def main():
    beilstein_unit_tests("CHEBI:2663", "C06823")

#   Get Beilstein registry number.
def get_beilstein_rn(com, user=None):
    beilstein_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["beilstein", "beilstein registry", "beilstein registry number", "beilstein rn"]):
        if iden["identifier"] not in beilstein_array:
            beilstein_array.append(iden["identifier"])
    
    if beilstein_array:
        return beilstein_array
    
    ids_completed = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "beilstein registry number":
                        beilstein_array.append(accession._DatabaseAccession__accession_number)

                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, language = None, identifier_type = "Beilstein Registry Number", source = "ChEBI")
            
    if beilstein_array:
        return beilstein_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_beilstein_rn(com)
            
    return beilstein_array

#   UNIT TESTS
def beilstein_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("\nGetting Beilstein registry number from ChEBI ID (%s):" % chebi_id)
    start = timeit.timeit()
    beilstein_array = get_beilstein_rn(chebi_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for beilstein in beilstein_array:
        print("\t- " + str(beilstein))
    
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting Beilstein registry number from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    beilstein_array = get_beilstein_rn(kegg_compound_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for beilstein in beilstein_array:
        print("\t- " + str(beilstein))

#   MAIN
if __name__ == "__main__": main()