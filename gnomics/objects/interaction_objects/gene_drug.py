#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get diseases from a gene.
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
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    gene_drug_unit_tests("675", "ENSG00000113916")

# Get drug interactions.
# http://dgidb.genome.wustl.edu/api
#
# Interaction sources can be TTD, DrugBank, etc.
# But should be an array if possible.
def get_drugs(gene, source="dgidb", interaction_sources=None, interaction_types=None, drug_types=None, source_trust_levels=None, user=None):
    drug_id_array = []
    drug_obj_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["entrez gene id", "entrez gene identifier", "entrez gene", "ncbi entrez gene identifier", "ncbi entrez gene", "ncbi gene id"]:    
            if source == "dgidb":
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v2/interactions.json?genes=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if drug_types is not None:
                    ext = ext + (",".join(drug_types)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for iden in decoded["ambiguousTerms"]:
                    for iden_sec in iden["interactions"]:
                        if "drugChemblId" in iden_sec:
                            temp_com = gnomics.objects.compound.Compound(identifier = iden_sec["drugChemblId"], identifier_type = "ChEMBL ID", source = "DGIdb")
                            for drug in gnomics.objects.compound.Compound.drugs(temp_com):
                                if not bool(set([x["identifier"] for x in drug.identifiers]) & set(drug_id_array)):
                                    drug_id_array.extend(iden_sec["drugChemblId"])
                                    drug_obj_array.append(drug)
            
        elif ident["identifier_type"].lower() in ["ensembl gene id", "ensembl gene identifier", "ensembl gene", "ensembl"]:
    
            if source == "dgidb":
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v2/interactions.json?genes=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if drug_types is not None:
                    ext = ext + (",".join(drug_types)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for iden in decoded["matchedTerms"]:
                    for iden_sec in iden["interactions"]:
                        if "drugChemblId" in iden_sec:
                            temp_com = gnomics.objects.compound.Compound(identifier = iden_sec["drugChemblId"], identifier_type = "ChEMBL ID", source = "DGIdb")
                            for drug in gnomics.objects.compound.Compound.drugs(temp_com):
                                if not bool(set([x["identifier"] for x in drug.identifiers]) & set(drug_id_array)):
                                    drug_id_array.extend(iden_sec["drugChemblId"])
                                    drug_obj_array.append(drug)
    
    if drug_obj_array:
        return drug_obj_array
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["hgnc approved symbol", "hgnc gene symbol", "hgnc symbol"]: 
            for ensembl_ident in gnomics.objects.gene.Gene.ensembl_gene_id(gene, user=user):
            
                if source == "dgidb":
                    server = "http://dgidb.genome.wustl.edu"
                    ext = "/api/v2/interactions.json?genes=" + ident["identifier"]

                    if interaction_sources is not None:
                        ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                    if interaction_types is not None:
                        ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                    if drug_types is not None:
                        ext = ext + (",".join(drug_types)).replace(" ", "%20")
                    if source_trust_levels is not None:
                        ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                    r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = r.json()
                    for iden in decoded["matchedTerms"]:
                        for iden_sec in iden["interactions"]:
                            if "drugChemblId" in iden_sec:
                                temp_com = gnomics.objects.compound.Compound(identifier = iden_sec["drugChemblId"], identifier_type = "ChEMBL ID", source = "DGIdb")
                                for drug in gnomics.objects.compound.Compound.drugs(temp_com):
                                    if not bool(set([x["identifier"] for x in drug.identifiers]) & set(drug_id_array)):
                                        drug_id_array.extend(iden_sec["drugChemblId"])
                                        drug_obj_array.append(drug)
    
    return drug_obj_array
    
#   UNIT TESTS
def gene_drug_unit_tests(entrez_gene_id, ensembl_gene_id):
    entrez_gene = gnomics.objects.gene.Gene(identifier = entrez_gene_id, identifier_type = "Entrez Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("Getting drugs from NCBI Entrez gene ID (%s):" % entrez_gene_id)
    for drug in get_drugs(entrez_gene):
        for iden in drug.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting drugs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    start = timeit.timeit()
    all_drugs = get_drugs(ensembl_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for drug in all_drugs:
        for iden in drug.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()