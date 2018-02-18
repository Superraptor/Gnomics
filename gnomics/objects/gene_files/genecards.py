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
#   Get GeneCards.
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
import gnomics.objects.gene

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    genecards_unit_tests("HGNC:23487", "ENSG00000148377", "hsa:91734")
    
#   Get GeneCards ID.
def get_genecards_id(gene):
    genecards_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["genecards", "genecards id", "genecards identifier"]:
            genecards_array.append(ident["identifier"])
    
    if genecards_array:
        return genecards_array
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl gene", "ensembl gene id", "ensembl gene identifier", "ensembl"]:
            
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ENSEMBL_ID",
                "to": "ID",
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
            
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "GENECARDS_ID",
                "format": "tab",
                "query": new_id,
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
            for counter, line in enumerate(newline_sp):
                if (counter > 0) and (len(newline_sp[1].split("\t")) > 1):
                    orig_id = newline_sp[1].split("\t")[0].strip()
                    new_id = newline_sp[1].split("\t")[1].strip()
                    if new_id not in genecards_array:
                        genecards_array.append(new_id)
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = new_id, identifier_type = "HGNC ID", source = "UniProt")
            
        elif ident["identifier_type"].lower() in ["kegg", "kegg gene", "kegg gene id", "kegg gene identifier", "kegg id", "kegg identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "KEGG_ID",
                "to": "ID",
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
            
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "GENECARDS_ID",
                "format": "tab",
                "query": new_id,
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
            for counter, line in enumerate(newline_sp):
                if (counter > 0) and (len(newline_sp[1].split("\t")) > 1):
                    orig_id = newline_sp[1].split("\t")[0].strip()
                    new_id = newline_sp[1].split("\t")[1].strip()
                    if new_id not in genecards_array:
                        genecards_array.append(new_id)
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = new_id, identifier_type = "HGNC ID", source = "UniProt")
                
        elif ident["identifier_type"].lower() in ["hgnc id", "hgnc identifier", "hgnc gene id", "hgnc gene identifier"]:
            
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "HGNC_ID",
                "to": "ID",
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
            
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "GENECARDS_ID",
                "format": "tab",
                "query": new_id,
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
            for counter, line in enumerate(newline_sp):
                if (counter > 0) and (len(newline_sp[1].split("\t")) > 1):
                    orig_id = newline_sp[1].split("\t")[0].strip()
                    new_id = newline_sp[1].split("\t")[1].strip()
                    if new_id not in genecards_array:
                        genecards_array.append(new_id)
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = new_id, identifier_type = "HGNC ID", source = "UniProt")

    return genecards_array
    
#   UNIT TESTS
def genecards_unit_tests(hgnc_id, ensembl_id, kegg_id):
    hgnc_gene = gnomics.objects.gene.Gene(identifier = hgnc_id, language = None, identifier_type = "HGNC ID", source = "UniProt", taxon = "Homo sapiens")
    print("Getting GeneCards ID from HGNC ID (%s):" % hgnc_id)
    for iden in get_genecards_id(hgnc_gene):
        print("- " + str(iden))
    
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_id, language = None, identifier_type = "Ensembl Gene ID", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting GeneCards ID from Ensembl Gene identifier (%s):" % ensembl_id)
    for iden in get_genecards_id(ensembl_gene):
        print("- " + str(iden))
        
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_id, language = None, identifier_type = "KEGG GENE ID", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting GeneCards ID from KEGG GENE identifier (%s):" % kegg_id)
    for iden in get_genecards_id(kegg_gene):
        print("- " + str(iden))
        
#   MAIN
if __name__ == "__main__": main()