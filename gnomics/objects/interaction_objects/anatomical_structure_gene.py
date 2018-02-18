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
#   Get genes from anatomical structure.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.gene

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    anatomical_structure_gene_unit_tests("UBERON_0003097", "UBERON_0002389")
     
#   Get genes affecting entity phenotype.
def get_genes_affecting_phenotype_of(anatomical_structure, user=None):
    
    gene_array = []
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anatomical_structure.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.replace(":", "_")
                
            base = "http://kb.phenoscape.org/api/gene/"
            ext = "affecting_entity_phenotype?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + str(proc_id) + "&limit=100"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("It appears something went wrong.")
            else:

                decoded = json.loads(r.text)

                for result in decoded["results"]:
                    gene_name = result["label"]
                    gene_taxon = result["taxon"]["label"]

                    if "zfin" in result["@id"]:
                        zfin_id = result["@id"].split("http://zfin.org/")[1]
                        temp_gene = gnomics.objects.gene.Gene(identifier = zfin_id, identifier_type = "ZFIN ID", source = "Phenoscape Knowledgebase", taxon = gene_taxon)
                        gene_array.append(temp_gene)
            
    return gene_array

#   Get genes expressed within entity.
def get_genes_expressed_within(anatomical_structure, user=None):
    gene_array = []
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anatomical_structure.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.replace(":", "_")
            
            base = "http://kb.phenoscape.org/api/gene/"
            ext = "expressed_within_entity?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + str(proc_id) + "&limit=0"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("It appears something went wrong.")
            else:

                decoded = json.loads(r.text)

                for result in decoded["results"]:

                    if "/marker/" in result["@id"]:
                        mousemine_primary_gene_id = result["@id"].split("/marker/")[1]

                        temp_gene = gnomics.objects.gene.Gene(identifier=mousemine_primary_gene_id, identifier_type="MouseMine Primary Gene ID", language=None, name=result["label"], taxon=result["taxon"]["label"])

                        gene_array.append(temp_gene)
            
    return gene_array
    
#   UNIT TESTS
def anatomical_structure_gene_unit_tests(uberon_id_1, uberon_id_2):
    uberon_anat = gnomics.objects.tissue.Tissue(identifier = uberon_id_1, identifier_type = "UBERON ID", source = "Phenoscape Knowledgebase")
    print("\nGetting gene identifiers which affect UBERON identifier (%s) entity phenotypes:" % uberon_id_1)
    start = timeit.timeit()
    phenotypes_affecting = get_genes_affecting_phenotype_of(uberon_anat)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for gene in phenotypes_affecting:
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
    uberon_anat = gnomics.objects.tissue.Tissue(identifier = uberon_id_2, identifier_type = "UBERON ID", source = "Phenoscape Knowledgebase")
    print("\nGetting gene identifiers expressed within UBERON identifier (%s) entity:" % uberon_id_2)
    start = timeit.timeit()
    phenotypes_expressed = get_genes_expressed_within(uberon_anat)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for gene in phenotypes_expressed:
        for iden in gene.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()