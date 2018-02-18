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
#   Get RefSeq Protein Accession.
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
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    refseq_unit_tests("P13368", "INSR_HUMAN")
    
#   Get RefSeq Protein Accession.
def get_refseq_acc(prot):
    acc_array = []
    
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["refseq", "refseq accession", "refseq id", "refseq identifier", "refseq protein", "refseq protein accession", "refseq protein id", "refseq protein identifier"]:
            acc_array.append(ident["identifier"])
            
    if acc_array:
        return acc_array
            
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["uniprotkb id", "uniprotkb identifier", "uniprot id", "uniprot identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "P_REFSEQ_AC",
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
            if new_id not in acc_array:
                acc_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["acc", "uniprot ac", "uniprot acc", "uniprot accession", "uniprotkb ac", "uniprotkb acc", "uniprotkb accession"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "P_REFSEQ_AC",
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
            if new_id not in acc_array:
                acc_array.append(new_id)
            
    return acc_array
    
#   UNIT TESTS
def refseq_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting RefSeq Protein Accession from UniProtKB accession (%s):" % uniprot_kb_ac)
    for iden in get_refseq_acc(uniprot_kb_ac_prot):
        print("- " + str(iden))
    
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting RefSeq Protein Accession from UniProtKB identifier (%s):" % uniprot_kb_id)
    for iden in get_refseq_acc(uniprot_kb_id_prot):
        print("- " + str(iden))
        
#   MAIN
if __name__ == "__main__": main()