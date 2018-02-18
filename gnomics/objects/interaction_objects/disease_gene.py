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
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
#

#
#   Get genes associated with a disease.
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
import gnomics.objects.disease_files.disgenet
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
from bioservices import *
from decimal import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import requests
import timeit

#   MAIN
def main():
    gene_unit_tests("219700", "C0010674", "2394", "H00286")

#   Get genes.
def get_genes(dis, user=None, score=False, score_threshold=None, sentence=False, reference=False):
    gene_array = []
    gene_obj_array = []
    gene_dict = {}
    
    for ident in dis.identifiers:
        if user is not None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            omim_diseases = gnomics.objects.disease.Disease.omim_disease(dis, user)
            for omim_dis in omim_diseases:
                for entry in omim_dis["object"]["omim"]["entryList"]:
                    ext_links = entry["entry"]["externalLinks"]
                    if "approvedGeneSymbols" in ext_links:
                        split_up = ext_links["approvedGeneSymbols"].split(",")
                        for s in split_up:
                            if s not in gene_array:
                                new_gene = gnomics.objects.gene.Gene(identifier = s, identifier_type = "Approved Gene Symbol", language = None, source = "OMIM")
                                gene_array.append(new_gene)
                                gene_obj_array.append(new_gene)
                    if "geneIDs" in ext_links:
                        split_up = ext_links["approvedGeneSymbols"].split(",")
                        for s in split_up:
                            if s not in gene_array:
                                new_gene = gnomics.objects.gene.Gene(identifier = s, identifier_type = "Entrez Gene ID", language = None, source = "OMIM")
                                gene_array.append(new_gene)
                                gene_obj_array.append(new_gene)
                    if "uniGenes" in ext_links:
                        split_up = ext_links["approvedGeneSymbols"].split(",")
                        for s in split_up:
                            if s not in gene_array:
                                new_gene = gnomics.objects.gene.Gene(identifier = s, identifier_type = "UniGene", language = None, source = "OMIM")
                                gene_array.append(new_gene)
                                gene_obj_array.append(new_gene)
                                
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier"]:
            pregene = gnomics.objects.disease_files.disgenet.umls_genes(dis)
            for sease, value in pregene.items():
                for v in value:
                    processed_gen = v["gene"]["value"].split("/")[-1]
                    if processed_gen not in gene_array and processed_gen != ident["identifier"]:
                        gene_dict[processed_gen] = {}
                        if score == False and score_threshold == None and sentence == False and reference == False:
                            gene_array.append(processed_gen)
                        elif score == True and score_threshold == None and sentence == False and reference == False:
                            gene_dict[processed_gen]["score"] = v["score"]["value"]
                        elif score == True and score_threshold is not None and sentence == False and reference == False:
                            if Decimal(score_threshold) < Decimal(v["score"]["value"]):
                                gene_dict[processed_gen]["score"] = v["score"]["value"]
                        elif score == True and score_threshold is not None and sentence == True and reference == False:
                            if Decimal(score_threshold) < Decimal(v["score"]["value"]):
                                gene_dict[processed_gen]["score"] = v["score"]["value"]
                                gene_dict[processed_gen]["sentence"] = v["sentence"]["value"][s.find("[")+1:s.rfind("]")]
                        elif score == True and score_threshold is not None and sentence == True and reference == True:
                            if Decimal(score_threshold) < Decimal(v["score"]["value"]):
                                gene_dict[processed_gen]["score"] = v["score"]["value"]
                                gene_dict[processed_gen]["sentence"] = v["sentence"]["value"][s.find("[")+1:s.rfind("]")]
                                gene_dict[processed_gen]["reference"] = v["pmid"]["value"].split("/")[-1]
                            
        elif user is None and (
            ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]
        ):
            
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/disease/OMIM:" + str(ident["identifier"]) + "/genes/"
            
            r = requests.get(server+ext)
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.json()
            
            for subj in decoded["associations"]:
                ncbi_gen = subj["subject"]["id"].split(":")[1]
                
                if ncbi_gen not in gene_array:
                    new_gene = gnomics.objects.gene.Gene(identifier = ncbi_gen, identifier_type = "NCBI Gene ID", language = None, source = "OMIM")
                    gnomics.objects.gene.Gene.add_identifier(new_gene, identifier = subj["subject"]["label"], identifier_type = "HGNC Approved Symbol", taxon = subj["subject"]["taxon"]["label"], language = None, source = "Monarch Initiative")
                    
                    gene_array.append(ncbi_gen)
                    gene_dict[ncbi_gen] = new_gene
                    gene_obj_array.append(new_gene)
                
                for edge in subj["evidence_graph"]["edges"]:
                    break
                    
        elif ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/disease/DOID:" + ident["identifier"] + "/genes/"
            
            r = requests.get(server+ext)
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.json()
            
            for subj in decoded["associations"]:
                ncbi_gen = subj["subject"]["id"].split(":")[1]
                
                if ncbi_gen not in gene_array:
                    new_gene = gnomics.objects.gene.Gene(identifier = ncbi_gen, identifier_type = "NCBI Gene ID", language = None, source = "OMIM")
                    gnomics.objects.gene.Gene.add_identifier(new_gene, identifier = subj["subject"]["label"], identifier_type = "HGNC Approved Symbol", taxon = subj["subject"]["taxon"]["label"],  language = None, source = "Monarch Initiative")
                    
                    gene_array.append(ncbi_gen)
                    gene_dict[ncbi_gen] = new_gene
                    gene_obj_array.append(new_gene)
                
                for edge in subj["evidence_graph"]["edges"]:
                    break
                    
        elif ident["identifier_type"].lower() in ["kegg", "kegg id", "kegg identifier", "kegg disease id"]:
            for key, val in gnomics.objects.disease.Disease.kegg_disease(dis)["GENE"].items():
                if key not in gene_array:
                    gene_array.append(key)
                    new_gene = gnomics.objects.gene.Gene(identifier = key, identifier_type = "HGNC Approved Symbol", language = None, source = "KEGG")
                    gene_dict[key] = new_gene
                    gene_obj_array.append(new_gene)
            
    if score == False and score_threshold == None and sentence == False and reference == False:
        return gene_obj_array
    else:
        return gene_dict
    
#   UNIT TESTS
def gene_unit_tests(omim_disease_id, umls_id, doid, kegg_disease_id, omim_api_key = None):
    if omim_api_key is not None:
        
        print("Creating user...")
        user = User(omim_api_key = omim_api_key)
        print("User created successfully.\n")
        
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("Getting genes (NCBI Gene IDs) from MIM Number (%s):" % omim_disease_id)
        for gene in get_genes(omim_disease, user = user):
            print("- " + str(gene))
        
        umls_disease = gnomics.objects.disease.Disease(identifier = str(umls_id), identifier_type = "UMLS ID", source = "UMLS")
        print("\nGetting genes (NCBI Gene IDs) from UMLS ID (%s):" % umls_id)
        for gene in get_genes(umls_disease):
            print("- " + str(gene))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting genes (NCBI Gene IDs) from DOID (%s):" % doid)
        for gene in get_genes(doid_dis):
            print("- " + str(gene))
        
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG DISEASE ID", source = "KEGG")
        print("\nGetting genes (HGNC Approved Gene Symbols) from KEGG DISEASE ID (%s):" % doid)
        for gene in get_genes(kegg_dis):
            print("- " + str(gene))
        
    else:
        print("No user provided. Cannot test OMIM's native conversion without OMIM API key.\n")
        print("Continuing with UMLS ID conversion...\n")
        
        umls_disease = gnomics.objects.disease.Disease(identifier = str(umls_id), identifier_type = "UMLS ID", source = "UMLS")
        print("Getting genes (NCBI Gene IDs) from UMLS ID (%s):" % umls_id)
        for gene in get_genes(umls_disease):
            print("- " + str(gene))
            
        omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
        print("\nGetting genes (NCBI Gene IDs) from MIM Number (%s):" % omim_disease_id)
        for gene in get_genes(omim_disease):
            print("- " + str(gene))
            
        doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        print("\nGetting genes (NCBI Gene IDs) from DOID (%s):" % doid)
        for gene in get_genes(doid_dis):
            print("- " + str(gene))
            
        kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG DISEASE ID", source = "KEGG")
        start = timeit.timeit()
        all_genes = get_genes(kegg_disease)
        end = timeit.timeit()
        print("TIME ELAPSED: %s seconds." % str(end - start))
        print("\nGetting genes (HGNC Approved Gene Symbols) from KEGG DISEASE ID (%s):" % doid)
        for gene in all_genes:
            print("- " + str(gene))

#   MAIN
if __name__ == "__main__": main()