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
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#

#
#   Get ChEBI identifier.
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
from bioservices import *
from libchebipy import ChebiEntity, ChebiException, Comment, CompoundOrigin, DatabaseAccession, Formula, Name, Reference, Relation, Structure
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    chebi_unit_tests("C01576", "6918092")
    
# Get ChEBI entity.
def get_chebi_entity(compound, user=None):
    chebi_array = []
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['chebi entity', 'chebi', 'chebi object']:
                chebi_array.append(com_obj['object'])
                
    if chebi_array:
        return chebi_array
            
    for chebi_id in get_chebi_id(compound, user = user):
        chebi_object = ChebiEntity(chebi_id.upper())
        gnomics.objects.compound.Compound.add_object(compound, obj = chebi_object, object_type = "ChEBI Entity")
        chebi_array.append(chebi_object)

    return chebi_array

#   Get ChEBI ID.
def get_chebi_id(com, user=None):
    chebi_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in chebi_array:
            chebi_array.append(iden["identifier"])
            
    if chebi_array:
        return chebi_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            kegg = KEGG(verbose = False)
            map_kegg_chebi = kegg.conv("chebi", "compound")
            gnomics.objects.compound.Compound.add_identifier(com, identifier = map_kegg_chebi["cpd:" + iden["identifier"]], language = None, identifier_type = "ChEBI", source = "KEGG")
            chebi_array.append(map_kegg_chebi["cpd:" + iden["identifier"]])

    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        for cid in gnomics.objects.compound.Compound.pubchem_cid(com):
            if iden["identifier"] not in ids_completed:
                ids_completed.append(iden["identifier"])
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/compound/cid/" + str(cid) + "/xrefs/RegistryID/JSONP"
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong while trying to attain a PubChem PUG REST connection...")
                else:
                    str_r = r.text

                    try:
                        l_index = str_r.index("(") + 1
                        r_index = str_r.index(")")
                        res = str_r[l_index:r_index]
                        decoded = json.loads(res)
                        for xref in decoded["InformationList"]["Information"][0]["RegistryID"]:
                            split_xref = xref.split(":")
                            if split_xref[0] == "CHEBI" and xref not in chebi_array:
                                chebi_array.append(xref)
                                gnomics.objects.compound.Compound.add_identifier(com, identifier = xref, language = None, identifier_type = "ChEBI", source = "PubChem")

                    except ValueError:
                        print("Input is not in a JSONP format.")

    return chebi_array

#   UNIT TESTS
def chebi_unit_tests(kegg_compound_id, pubchem_cid):
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting ChEBI ID from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    chebi_array = get_chebi_id(kegg_compound_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in chebi_array:
        print("\t- %s" % str(com))
    
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting ChEBI ID from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    chebi_array = get_chebi_id(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in chebi_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()