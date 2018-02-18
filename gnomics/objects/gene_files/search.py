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
#   Search for genes.
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

#   Other imports.
import eutils
import eutils.client
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("SLC4A1")

#   Search.
def search(query, user=None, search_type=None, taxon="Homo sapiens", source="ensembl", efetch_limit=100):
    result_set = []
    
    if source.lower() in ["ensembl", "all"]:
        server = "https://rest.ensembl.org"
        ext = "/xrefs/symbol/" + taxon.replace(" ", "_").lower() + "/" + query + "?"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            temp_gen = gnomics.objects.gene.Gene()
            for result in decoded:
                result_id = result["id"]
                if "ENSG" in result_id:
                    gnomics.objects.gene.Gene.add_identifier(temp_gen, identifier = result_id, identifier_type = "Ensembl Gene ID", source = "Ensembl")
                elif "LRG_" in result_id:
                    gnomics.objects.gene.Gene.add_identifier(temp_gen, identifier = result_id, identifier_type = "Locus Reference Genomics", source = "Ensembl")
                else:
                    print("The identifier '%s' was not found among the covered gene types." % result_id)
            if len(temp_gen.identifiers) > 0:
                result_set.append(temp_gen)
    
    if source is None:
        print("No included source provided.")
        print("Repeating with Ensembl search...")
        search(query, source="ensembl")
        
    if source.lower() in ["ncbi", "entrez", "all"]:
        ec = eutils.client.Client()
        esr = ec.esearch(db="gene", term=query)
        id_array = []
        for x in esr.ids:
            
            # Set limit to number of results.
            if efetch_limit is not None:
                if len(id_array) < efetch_limit:
                    id_array.append(x)
            else:
                id_array.append(x)
                
        try:
            egs = ec.efetch(db="gene", id=id_array)
            result_set = []
            for gen in egs.entrezgenes:
                hgnc = gen.hgnc
                maploc = gen.maploc
                description = gen.description
                gene_type = gen.type
                genus_species = gen.genus_species
                common_tax = gen.common_tax
                gene_commentaries = gen.gene_commentaries
                references = gen.references
                summary = gen.summary
                synonyms = gen.synonyms
                gene_id = gen.gene_id

                if genus_species == taxon:
                    temp_gen = gnomics.objects.gene.Gene(identifier = gene_id, name = hgnc, language = None, source = "Entrez Programming Utilities", identifier_type = "Entrez Gene ID", taxon = genus_species)
                    gnomics.objects.gene.Gene(identifier = hgnc, name = hgnc, language = None, source = "Entrez Programming Utilities", identifier_type = "HGNC Symbol", taxon = genus_species)

                    result_set.append(temp_gen)
        except eutils.exceptions.EutilsNCBIError:
            print("Error parsing response object from NCBI.")
    
    return result_set

#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic searches for '%s'..." % basic_query)
    
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="ensembl")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    print("\nEnsembl search returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for ens in basic_search_results:
        for iden in ens.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
    basic_search_results = search(basic_query, source="entrez")
    print("\nEntrez search returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for ent in basic_search_results:
        for iden in ent.identifiers:
            print("- %s: %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"], iden["taxon"]))

#   MAIN
if __name__ == "__main__": main()