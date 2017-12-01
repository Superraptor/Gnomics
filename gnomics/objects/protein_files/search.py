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
#   Search for protein.
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
import gnomics.objects.protein

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("breast cancer")
    
# Return search.
#
# Various parameters available here:
# http://www.uniprot.org/help/api_queries
# http://www.uniprot.org/help/query-fields
#
# RESULT PARAMS
# result_format: html, tab, xls, fasta, gff, txt, xml, rdf, list, rss
# columns: citation, clusters, comments, domains, domain, ec, id, entry name, existence, families, features, genes, go, go-id, interactor, keywords, last-modified, length, organism, organism-id, pathway, protein names, reviewed, sequence, 3d, version, virus hosts
# include: yes, no
# compress: yes, no
# limit: [int]
# offset: [int]
#
# QUERY PARAMS
# accession
# active
# annotation
# author
# cdantigen
# citation
# cluster
# count
# created
# database
# ec
# evidence
# existence
# family
# fragment
# gene
# gene_exact
# goa
# host
# id
# inn
# interactor
# keyword
# length
# lineage
# mass
# method
# mnemonic
# modified
# name
# organelle
# organism
# plasmid
# proteome
# proteomecomponent
# replaces
# reviewed
# scope
# sequence
# sequence_modified
# source
# strain
# taxonomy
# tissue
# web
def search(query, source = "uniprot", result_format = "json"):
    if source == "uniprot":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        print(decoded)
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following protein IDs:" % str(len(basic_search_results)))
    for prot in basic_search_results:
        for iden in prot.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()