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
#   Get enzyme from protein.
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
import gnomics.objects.enzyme
import gnomics.objects.protein

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_enzyme_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get enzyme identifier for a protein.
def get_enzyme(prot):
    enzyme_id_array = []
    enzyme_obj_array = []
            
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["uniprotkb id", "uniprotkb identifier", "uniprot id", "uniprot identifier"]:
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "EC":
                        enzyme_id_array.append(xref["identifier"])
                        temp_enzyme = gnomics.objects.enzyme.Enzyme(identifier = xref["identifier"], identifier_type = "EC Number", source = "UniProt")
                        enzyme_obj_array.append(temp_enzyme)
            
        elif ident["identifier_type"].lower() in ["uniprotkb ac", "uniprotkb acc", "uniprotkb accession", "uniprot accession"]:
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "EC":
                        enzyme_id_array.append(xref["identifier"])
                        temp_enzyme = gnomics.objects.enzyme.Enzyme(identifier = xref["identifier"], identifier_type = "EC Number", source = "UniProt")
                        enzyme_obj_array.append(temp_enzyme)
            
    return enzyme_obj_array
    
#   UNIT TESTS
def protein_enzyme_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting references from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_enzyme(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting references from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_enzyme(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()