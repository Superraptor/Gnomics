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
#   Get compound from protein.
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
import pubchempy as pubchem
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    compound_unit_tests("P24592", "IBP6_HUMAN")
    
#   Get compounds.
def get_compounds(prot):
    com_array = []
    com_id_array = []
    
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["disprot", "disprot identifier", "disprot id"] and ident["identifier"] not in com_id_array:
            temp_com = gnomics.objects.compound.Compound(identifier=ident["identifier"], identifier_type="DisProt ID", source=ident["source"], language=ident["language"])
            com_array.append(temp_com)
            com_id_array.append(ident["identifier"])

        elif ident["identifier_type"].lower() in ["uniprotkb id", "uniprotkb identifier", "uniprot id", "uniprot identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "CHEMBL_ID",
                "format": "tab",
                "query": ident["identifier"],
            }
            
            data = urllib.parse.urlencode(params)
            data = data.encode("utf-8")
            request = urllib.request.Request(url, data)
            contact = ""
            request.add_header("User-Agent", "Python %s" % contact)
            response = urllib.request.urlopen(request)
            page = response.read(200000).decode("utf-8")
            
            newline_sp = page.split("\n")
            id_from = newline_sp[0].split("\t")[0].strip()
            id_to = newline_sp[0].split("\t")[1].strip()
            orig_id = newline_sp[1].split("\t")[0].strip()
            new_id = newline_sp[1].split("\t")[1].strip()
            if new_id not in com_id_array:
                com_id_array.append(new_id)
                temp_com = gnomics.objects.compound.Compound(identifier=new_id, identifier_type="ChEMBL ID", source="UniProt", language=None)
                com_array.append(temp_com)
            
        elif ident["identifier_type"].lower() in ["uniprotkb ac", "uniprotkb acc", "uniprotkb accession", "uniprot accession"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "CHEMBL_ID",
                "format": "tab",
                "query": ident["identifier"],
            }
            
            data = urllib.parse.urlencode(params)
            data = data.encode("utf-8")
            request = urllib.request.Request(url, data)
            contact = ""
            request.add_header("User-Agent", "Python %s" % contact)
            response = urllib.request.urlopen(request)
            page = response.read(200000).decode("utf-8")
            
            newline_sp = page.split("\n")
            id_from = newline_sp[0].split("\t")[0].strip()
            id_to = newline_sp[0].split("\t")[1].strip()
            orig_id = newline_sp[1].split("\t")[0].strip()
            new_id = newline_sp[1].split("\t")[1].strip()
            if new_id not in com_array:
                com_id_array.append(new_id)
                temp_com = gnomics.objects.compound.Compound(identifier=new_id, identifier_type="ChEMBL ID", source="UniProt", language=None)
                com_array.append(temp_com)
            
    return com_array
    
#   UNIT TESTS
def compound_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", species = "Homo sapiens")
    print("Getting ChEMBL ID from UniProtKB accession (%s):" % uniprot_kb_ac)
    for iden in get_compounds(uniprot_kb_ac_prot):
        print("- " + str(iden))
    
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", species = "Homo sapiens")
    print("\nGetting ChEMBL ID from UniProtKB identifier (%s):" % uniprot_kb_id)
    for iden in get_compounds(uniprot_kb_id_prot):
        print("- " + str(iden))
        
#   MAIN
if __name__ == "__main__": main()