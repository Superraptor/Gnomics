#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices
#

#
#   Get KEGG GENE.
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
import gnomics.objects.gene
import gnomics.objects.taxon

#   Other imports.
from bioservices import *
import re
import requests
import urllib
import urllib3

#   MAIN
def main():
    kegg_unit_tests("675")

# Get KEGG gene object.
def get_kegg_gene(gene):
    
    kegg_gene_array = []
    
    for gene_obj in gene.gene_objects:
        if 'object_type' in gene_obj:
            if gene_obj['object_type'].lower() in ["kegg", "kegg gene", "kegg gene object", "kegg object"]:
                gene_obj['object']
            
    if kegg_gene_array:
        return kegg_gene_array
            
    s = KEGG()
    for temp_gen in gnomics.objects.gene.Gene.kegg_gene_id(gene):
        gene_array = []
        if ":" in temp_gen:
            gene_array = temp_gen.split(":")
        else:
            gene_array = re.findall(r"[^\W\d_]+|\d+", temp_gen)
            
        if gene_array:
            final_gene_from_array = gene_array[0] + ":" + gene_array[1]
            res = s.get(final_gene_from_array)
            gene_res = s.parse(res)
            if res != 404:
                gnomics.objects.gene.Gene.add_object(gene, obj=gene_res, object_type="KEGG GENE")
                kegg_gene_array.append(gene_res)
        
    return kegg_gene_array

# Returns KEGG gene identifier.
def get_kegg_gene_id(gene):
    kegg_gene_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["kegg", "kegg id", "kegg identifier", "kegg gene", "kegg gene id", "kegg gene identifier"]):
        if iden["identifier"] not in kegg_gene_array:
            kegg_gene_array.append(iden["identifier"])
            
    if kegg_gene_array:
        return kegg_gene_array
    
    ids_completed = []
          
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["uniprot", "uniprot id", "uniprot identifier"]:
            u = UniProt(verbose = False)
            u_dict = u.mapping(fr="ACC+ID", to="KEGG_ID", query=ident["identifier"])
            u_gene = u_dict[ident["identifier"]]
            for gen in u_gene:
                prefix = (''.join([i for i in gen if not i.isdigit()])).replace(":", "")
                sp = gnomics.objects.taxon.Taxon(identifier = prefix, identifier_type = "KEGG")
                gene.identifiers.append({
                    'identifier': gen,
                    'language': None,
                    'identifier_type': "UniProt identifier",
                    'taxon': sp.scientific_name,
                    'source': "UniProt"
                })
                kegg_gene_array.append(gen.replace(":", ""))
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi-geneid", "entrez id", "entrez identifier", "ncbi id", "ncbi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
        
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "P_ENTREZGENEID",
                "to": "ID",
                "format": "tab",
                "query": iden["identifier"],
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
            if new_id != "null":

                url = "http://www.uniprot.org/uploadlists/"
                params = {
                    "from": "ID",
                    "to": "KEGG_ID",
                    "format": "tab",
                    "query": new_id,
                }

                data = urllib.parse.urlencode(params)
                data = data.encode("utf-8")
                try:
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

                    if new_id not in kegg_gene_array:
                        kegg_gene_array.append(new_id)
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier=new_id, identifier_type="KEGG GENE ID", source="UniProt", language=None)
                except requests.exceptions.ConnectionError:
                    print("A connection error occurred.")
                except urllib3.exceptions.NewConnectionError:
                    print("A new connection error occurred.")
                except urllib3.exceptions.MaxRetryError:
                    print("A max retry error occurred.")
                        
    return kegg_gene_array
    
#   UNIT TESTS
def kegg_unit_tests(ncbi_entrez_gene_id):
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_entrez_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("\nGetting KEGG GENE IDs from NCBI Entrez Gene ID (%s):" % ncbi_entrez_gene_id)
    for kegg in get_kegg_gene_id(ncbi_gene):
        print("- %s" % kegg)
    
#   MAIN
if __name__ == "__main__": main()