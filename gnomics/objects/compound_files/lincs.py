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
import timeit

#   MAIN
def main():
    lincs_unit_tests("CHEBI:4911", "C01576")

#   Get LINCS ID.
def get_lincs_id(com, user=None):
    
    lincs_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["lincs", "lincs accession", "lincs id", "lincs identifier"]):
        if iden["identifier"] not in lincs_array:
            lincs_array.append(iden["identifier"])
            
    if lincs_array:
        return lincs_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
            
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "lincs accession" and accession._DatabaseAccession__accession_number not in lincs_array:

                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, identifier_type = "LINCS Accession")
                        lincs_array.append(accession._DatabaseAccession__accession_number)
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com)
    
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "lincs accession" and accession._DatabaseAccession__accession_number not in lincs_array:

                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, identifier_type = "LINCS Accession")
                        lincs_array.append(accession._DatabaseAccession__accession_number)
                    
    return lincs_array

#   UNIT TESTS
def lincs_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting LINCS accession from ChEBI ID (%s):" % chebi_id)
    start = timeit.timeit()
    lincs_array = get_lincs_id(chebi_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in lincs_array:
        print("\t- %s" % str(com))
        
    kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting LINCS accession from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    lincs_array = get_lincs_id(kegg_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in lincs_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()