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
#   Get PDB.
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
import gnomics.objects.protein

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    pdb_unit_tests("P69905", "INSR_HUMAN")
    
#   Get PDB ID.
def get_pdb_id(prot):
    pdb_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "pdb" or ident["identifier_type"].lower() == "pdb identifier" or ident["identifier_type"].lower() == "pdb id" or ident["identifier_type"].lower() == "protein data bank id":
            pdb_array.append(ident["identifier"])
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "PDB_ID",
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
            for x in range(1, len(newline_sp) - 1):
                orig_id = newline_sp[x].split("\t")[0].strip()
                new_id = newline_sp[x].split("\t")[1].strip()
                if new_id not in pdb_array:
                    pdb_array.append(new_id)
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "PDB_ID",
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
            for x in range(1, len(newline_sp) - 1):
                orig_id = newline_sp[x].split("\t")[0].strip()
                new_id = newline_sp[x].split("\t")[1].strip()
                if new_id not in pdb_array:
                    pdb_array.append(new_id)
    return pdb_array
    
#   UNIT TESTS
def pdb_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting PDB ID from UniProtKB accession (%s):" % uniprot_kb_ac)
    for iden in get_pdb_id(uniprot_kb_ac_prot):
        print("- " + str(iden))
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting PDB ID from UniProtKB identifier (%s):" % uniprot_kb_id)
    for iden in get_pdb_id(uniprot_kb_id_prot):
        print("- " + str(iden))
        
#   MAIN
if __name__ == "__main__": main()