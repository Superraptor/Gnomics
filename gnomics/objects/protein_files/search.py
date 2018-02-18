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
#   Search for proteins.
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
import gnomics.objects.disease
import gnomics.objects.protein

#   Other imports.
import eutils
import json
import requests
import timeit
import xml.etree.ElementTree as ET

#   MAIN
def main():
    basic_search_unit_tests("AKT1") #"insulin")
    
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
def search(query, source="uniprot", result_format="tab", user=None):
    prot_list = []
    prot_id_array = []
    
    if source in ["ncbi", "entrez", "all"]:
        ec = eutils.client.Client()
        esr = ec.esearch(db="protein", term=query)
        id_list = ",".join(str (x) for x in esr.ids)
        
        base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        ext = "esummary.fcgi?db=protein&id=" + str(id_list)
        
        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            tree = ET.ElementTree(ET.fromstring(r.text))
            root = tree.getroot()
            temp_dict = {}

            for child in root:
                for subchild in child:
                    if "Name" in subchild.attrib:
                        if subchild.attrib["Name"] == "Gi":
                            species_name = None
                            prot_name = None
                            refseq_protein_accession = None
                            refseq_protein_accession_ver = None

                            for subchild_2 in child:
                                if "Name" in subchild_2.attrib:
                                    if subchild_2.attrib["Name"] == "Title":
                                        proc_title = (subchild_2.text).strip().split(" [")
                                        
                                        if len(proc_title) > 1:
                                            species_name = proc_title[1].replace("]", "").strip()
                                            
                                        prot_name = proc_title[0].strip()
                                    elif subchild_2.attrib["Name"] == "Caption":
                                        refseq_protein_accession = str(subchild_2.text)
                                    elif subchild_2.attrib["Name"] == "AccessionVersion":
                                        refseq_protein_accession_ver = str(subchild_2.text)

                            temp_prot = gnomics.objects.protein.Protein(identifier=subchild.text, identifier_type="GI Number", language=None, taxon=species_name, name=prot_name)
                            
                            if refseq_protein_accession is not None:
                                gnomics.objects.protein.Protein.add_identifier(temp_prot, identifier=refseq_protein_accession, identifier_type="RefSeq Protein Accession", language=None, taxon=species_name, name=prot_name)

                            if refseq_protein_accession_ver is not None:
                                gnomics.objects.protein.Protein.add_identifier(temp_prot, identifier=refseq_protein_accession_ver, identifier_type="RefSeq Protein Accession Version", language=None, taxon=species_name, name=prot_name)

                            prot_id_array.append(subchild.text)
                            prot_list.append(temp_prot)
    
    if source in ["uniprot", "all"]:
        
        # Results are currently limited to 100 due to the difficulty
        # in parsing larger files. Please see here for details:
        # https://www.uniprot.org/help/api_queries
        
        # Future UniProt queries may be carried out in tandem with
        # the Protein API, located here:
        # https://www.ebi.ac.uk/proteins/api/doc/#!/proteins/search
        
        url = "http://www.uniprot.org/uniprot"
        ext = "/?query=" + str(query) + "&sort=score&columns=id,entry%20name,protein%20names,organism&format=tab&limit=100"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            
            for counter, line in enumerate((r.text).split("\n")):
                if counter != 1:
                    line_split = (line.strip()).split("\t")
                    
                    if len(line_split) > 1:
                        uniprot_accession = line_split[0]
                        uniprot_id = line_split[1]
                        protein_name = line_split[2].split(" (")[0].strip()
                        organism = line_split[3].split(" (")[0].strip()

                        if uniprot_id not in prot_id_array and uniprot_accession not in prot_id_array and protein_name not in prot_id_array and protein_name is not None and uniprot_id != "Entry name":

                            temp_prot = gnomics.objects.protein.Protein(identifier=uniprot_id, identifier_type="UniProt ID", source="UniProt", language=None, name=protein_name, taxon=organism)

                            gnomics.objects.protein.Protein.add_identifier(temp_prot, identifier=uniprot_accession, identifier_type="UniProt ID", source="UniProt", language=None, name=protein_name, taxon=organism)

                            prot_list.append(temp_prot)
                            prot_id_array.append(uniprot_id)
                            prot_id_array.append(uniprot_accession)
                            prot_id_array.append(protein_name)
    
    return prot_list
        
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="all")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nSearch returned %s result(s) with the following protein IDs:" % str(len(basic_search_results)))
    for prot in basic_search_results:
        for iden in prot.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()