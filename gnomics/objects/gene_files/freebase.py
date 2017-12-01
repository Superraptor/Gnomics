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
#   Get Freebase ID.
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
import json
import requests

#   MAIN
def main():
    freebase_unit_tests("ENSG00000012048")
    
#   Get Freebase ID.
def get_freebase_id(gene):
    gene_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "freebase" or ident["identifier_type"].lower() == "freebase id" or ident["identifier_type"].lower() == "freebase identifier":
            if ident["identifier"] not in gene_array:
                gene_array.append(ident["identifier"])
    if gene_array:
        return gene_array
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.gene.Gene.wikidata(gene):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "freebase id":
                        for x in prop_dict:
                            gnomics.objects.gene.Gene.add_identifier(gene, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Freebase ID", language = None, source = "Wikidata")
                            gene_array.append(x["mainsnak"]["datavalue"]["value"])
            return gene_array
    if gene_array:
        return gene_array
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier":
            gnomics.objects.gene.Gene.wikidata_accession(gene)
            return get_freebase_id(gene)

#   UNIT TESTS
def freebase_unit_tests(ensembl_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("Getting Freebase IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for gen in get_freebase_id(ensembl_gene):
            print("- %s" % gen)

#   MAIN
if __name__ == "__main__": main()