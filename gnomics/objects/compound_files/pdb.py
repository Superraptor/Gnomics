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
#   Get PBD Ligand ID.
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
import json
import requests
import timeit

#   MAIN
def main():
    pdb_unit_tests("Q418817")

#   Get PDB Ligand ID.
def get_pdb_ligand_id(com, user=None):
    pdb_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["pdb ligand", "pdb ligand id", "pdb ligand identifier", "protein data bank ligand", "protein data bank ligand id", "protein data bank ligand identifier", "protein databank ligand", "protein databank ligand id", "protein databank ligand identifier"]):
        if iden["identifier"] not in pdb_array:
            pdb_array.append(iden["identifier"])
            
    if pdb_array:
        return pdb_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in gnomics.objects.compound.Compound.wikidata(com):
                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "pdb ligand id", wikidata_property_language = "en")
                for x in found_array:
                    if x not in pdb_array:
                        pdb_array.append(x)
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = x, identifier_type = "PDB Ligand ID", language = None, source = "Wikidata")

    return pdb_array

#   UNIT TESTS
def pdb_unit_tests(wikidata_accession):
    wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
    
    print("\nGetting PDB Ligand IDs from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    pdb_array = get_pdb_ligand_id(wikidata_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in pdb_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()