#
#
#
#
#

#
#   IMPORT SOURCES:
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
import eutils.client
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("SLC4A1") # BRCA2

#   Search.
def search(query, user = None, search_type = None, taxon = "Homo sapiens", source = "ensembl"):
    result_set = []
    if source.lower() == "ensembl":
        server = "https://rest.ensembl.org"
        ext = "/xrefs/symbol/" + taxon.replace(" ", "_").lower() + "/" + query + "?"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        print(repr(decoded))
        
        temp_gen = gnomics.objects.gene.Gene()
        for result in decoded:
            result_id = result["id"]
            if "ENSG" in result_id:
                gnomics.objects.gene.Gene.add_identifier(temp_gen, identifier = result_id, identifier_type = "Ensembl Gene ID", source = "Ensembl")
            elif "LRG_" in result_id:
                gnomics.objects.gene.Gene.add_identifier(temp_gen, identifier = result_id, identifier_type = "Locus Reference Genomics", source = "Ensembl")
            else:
                print("The identifier '%s' was not found among the covered gene types." % result_id)
        result_set.append(temp_gen)
        return result_set
    elif source is None:
        print("No included source provided.")
        print("Repeating with Ensembl search...")
        search(query, source = "ensembl")
    elif source.lower() == "ncbi" or source.lower() == "entrez":
        ec = eutils.client.Client()
        esr = ec.esearch(db="gene", term=query)
        id_array = []
        for x in esr.ids:
            id_array.append(x)
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
            
        return result_set
    else:
        print("Something went wrong.")

#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("NOT FUNCTIONAL.")
    
    print("Beginning basic searches for '%s'..." % basic_query)
    
    basic_search_results = search(basic_query, source="ensembl")
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