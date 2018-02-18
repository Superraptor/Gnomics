#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#

#
#   Get various KEGG compound identifiers.
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
import timeit

#   MAIN
def main():
    kegg_unit_tests("CHEBI:4911", "C01576")
    
#   KEGG database entry (for compound).
def get_kegg_compound_db_entry(compound, user=None):
    kegg_array = []
    
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['kegg compound', 'kegg compound object']:
                kegg_array.append(com_obj['object'])
                
    if kegg_array:
        return kegg_array
    
    for kegg_id in gnomics.objects.compound.Compound.kegg_compound_id(compound):
                
        s = KEGG()
        res = s.get("cpd:" + str(kegg_id))
        parsed_obj = s.parse(res)
        gnomics.objects.compound.Compound.add_object(compound, obj=parsed_obj, object_type="KEGG COMPOUND")
        kegg_array.append(parsed_obj)
        
    return kegg_array

#   Get KEGG compound identifier.
def get_kegg_compound_id(com, user=None):
    kegg_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in kegg_array:
            kegg_array.append(iden["identifier"])
            
    if kegg_array:
        return kegg_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "kegg compound accession" and accession._DatabaseAccession__accession_number not in kegg_array:

                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, identifier_type = "KEGG COMPOUND Accession", language = None, source = "ChEBI")

                        kegg_array.append(accession._DatabaseAccession__accession_number)

    return kegg_array

#   UNIT TESTS
def kegg_unit_tests(chebi_id, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    
    print("\nGetting KEGG Compound ID from ChEBI ID (%s):" % chebi_id)
    start = timeit.timeit()
    kegg_array = get_kegg_compound_id(chebi_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in kegg_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()