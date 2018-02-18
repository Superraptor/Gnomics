#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       GEOPARSE
#           https://geoparse.readthedocs.io/en/latest/
#

#
#   Perform gene expression functionalities.
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
import csv
import eutils.client
import GEOparse
import numpy as np
import pandas as pd
import re
import requests
import string

#   Import sub-methods.

#   Import further methods.

#   MAIN
def main():
    search_geo("idiopathic pulmonary fibrosis")
    geo_unit_tests("GSE24206", "ENSG00000042832")
    
#   Search GEO datasets.
def search_geo(query, taxon = "Homo sapiens"):
    ec = eutils.client.Client()
    full_query = "GSE[ETYP]+AND+%s[porgn]+AND+%s" % (taxon, query)
    
    server = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ext = "/esearch.fcgi?db=gds&term=" + full_query + "&retmode=json&retmax=5000"
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    id_array = decoded["esearchresult"]["idlist"]
    id_string = ",".join(id_array)
    
    server = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    ext = "/esummary.fcgi?db=gds&id=" + id_string + "&retmode=json"
    
    print(server+ext)

    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()
    
    accession_list = []
    for iden, iden_dict in decoded["result"].items():
        if iden != "uids":
            accession_list.append(iden_dict["accession"])

    return accesssion_list

#   Download GEO Dataset.
#   GSE = GEO data SEries
def download(geo_accession):
    if not os.path.exists("../../data/geo/"):
        os.makedirs("../../data/geo/")
    gse = GEOparse.get_GEO(geo=geo_accession, destdir="../../data/geo/")
    return gse

#   Get GSMs from GEO Dataset.
#   GSM = GEO SaMple
def get_gsms(gse):
    gsm_dict = {}
    for gsm_name, gsm in gse.gsms.items():
        gsm_dict[gsm_name] = gsm
    return gsm_dict

#   Get GPLs from GEO Dataset.
#   GPL = GEO PLatform
def get_gpls(gse):
    gpl_dict = {}
    for gpl_name, gpl in gse.gpls.items():
        gpl_dict[gpl_name] = gpl
    return gpl_dict

#   Get gene from GPL and GSM.
#
#   Note that this is RMA.
def get_gene_from_gpl(gpl, gsm, gene):
    hgnc_symbol = gnomics.objects.gene.Gene.hgnc_gene_symbol(gene)
    gene_rows = gpl.table.loc[gpl.table["Gene Symbol"] == hgnc_symbol]

    if gene_rows.empty:
        gene_rows = gpl.table[gpl.table["Gene Symbol"].str.contains(hgnc_symbol, na=False)]
        
    affymetrix_probe_set_ids = gene_rows[["ID"]].as_matrix().flatten()
    probe_dict = {}
    for iden in affymetrix_probe_set_ids:
        probe_found = gsm.table[gsm.table["ID_REF"].str.contains(iden, na=False)]
        probe_val = probe_found[["VALUE"]].as_matrix().flatten()[0]
        probe_dict[iden] = probe_val
        
    return probe_dict

#   Get phenotype data from GSE.
def get_phenotype_data_from_gse(gse):
    experiments = {}
    for i, (idx, row) in enumerate(gse.phenotype_data.iterrows()):
        tissue_results = gnomics.objects.tissue.Tissue.search(row["characteristics_ch1.0.tissue"])
        
        tmp = {}
        found = False
        for result in tissue_results:
            for x in result.identifiers:
                if x["identifier_type"] == "UBERON ID":
                    tmp["UBERON ID"] = x["identifier"]
                    tmp["UBERON Term"] = x["name"]
                    found = True
                if found:
                    break
            if found:
                break
        
        found = False
        phenotype_results = gnomics.objects.phenotype.Phenotype.search(row["characteristics_ch1.2.phenotype"])
        for result in phenotype_results:
            for x in result.identifiers:
                if x["identifier_type"] == "HPO ID" or x["identifier_type"] == "HP ID" or x["identifier_type"] == "Human Phenotype Ontology ID":
                    tmp["HPO ID"] = x["identifier"]
                    tmp["HPO Term"] = x["name"]
                    found = True
                if found:
                    break
            if found:
                break
            
        tmp["Experiment"] = idx
        tmp["Type"] = row["characteristics_ch1.2.phenotype"]
        tmp["Tissue"] = row["characteristics_ch1.0.tissue"]
        tmp["Gender"] = row["characteristics_ch1.3.gender"]
        tmp["Age"] = row["characteristics_ch1.4.age"]
        
        experiments[i] = tmp
        
    experiments = pd.DataFrame(experiments).T
    return experiments
    
    
#   Convert read fragments to FPKM.
#   https://github.com/WenchaoLin/Sam2Xpkm
#   http://assets.geneious.com/manual/8.0/GeneiousManualsu76.html
#
#   FPKM = Fragments Per Kilbase of transcipt per Million
#   FPKM = (# of fragments) / (transcript length / 1000) / 
#   (total reads / 10^6)
def fpkm(gene, number_of_fragments, total_reads, length_of_all_genes):
    length_of_gene = gnomics.objects.gene.Gene.gene_length(gene)
    fpkm = (number_of_fragments) / (float(length_of_gene[0]) / float(1000)) / (total_reads / float(10^6))
    return fpkm
    
#   Convert read counts to RPKM.
#   https://github.com/WenchaoLin/Sam2Xpkm
#   http://assets.geneious.com/manual/8.0/GeneiousManualsu76.html
#
#   RPKM = Reads Per Kilobase per Million
#   RPKM = (# of mapped reads) / (length of transcript / 1000) /
#   (total reads / 10^6)
def rpkm(gene, number_of_reads, total_reads):
    length_of_gene = gnomics.objects.gene.Gene.gene_length(gene)
    rpkm = (number_of_reads) / (float(length_of_gene[0]) / float(1000)) / (total_reads / float(10^6))
    return rpkm

#   Convert FPKM to TPM.
#
#   TPM = (FPKM / SUM(FPKM)) * 10^6
#   - TPM = Transcripts Per Million
def fpkm_to_tpm(gene, fpkm, total_fpkm):
    tpm = (fpkm / total_fpkm) * float(10^6)
    return tpm
    
#   UNIT TESTS
def geo_unit_tests(geo_accession, ensembl_gene_id):
    gse = download(geo_accession)
    gsms = get_gsms(gse)
    gpls = get_gpls(gse)
    
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", source = "GEO")
    
    print("Finding %s in %s:" % (ensembl_gene_id, geo_accession))
    for gpl_name, gpl in gpls.items():
        print("- %s" % gpl_name)
        for gsm_name, gsm in gsms.items():
            print(" - %s" % gsm_name)
            for probe, expr in get_gene_from_gpl(gpl, gsm, ensembl_gene).items():
                print("  - %s: %s" % (probe, str(expr)))
    
    print("Getting phenotype information...")
    phenotype_data = get_phenotype_data_from_gse(gse)
    
    probe_dict = {}
    counter = 0
    for gpl_name, gpl in gpls.items():
        for gsm_name, gsm in gsms.items():
            for probe, expr in get_gene_from_gpl(gpl, gsm, ensembl_gene).items():
                phen_array = phenotype_data[phenotype_data["Experiment"].str.contains(gsm_name, na=False)]        

                tmp = {}
                tmp["Age"] = phen_array[["Age"]].as_matrix().flatten()[0]
                tmp["Gender"] = phen_array[["Gender"]].as_matrix().flatten()[0]
                tmp["HPO ID"] = phen_array[["HPO ID"]].as_matrix().flatten()[0]
                tmp["HPO Term"] = phen_array[["HPO Term"]].as_matrix().flatten()[0]
                tmp["Tissue"] = phen_array[["Tissue"]].as_matrix().flatten()[0]
                tmp["Type"] = phen_array[["Type"]].as_matrix().flatten()[0]
                tmp["UBERON ID"] = phen_array[["UBERON ID"]].as_matrix().flatten()[0]
                tmp["UBERON Term"] = phen_array[["UBERON Term"]].as_matrix().flatten()[0]
                tmp["Sample"] = gsm_name
                tmp["Probe"] = probe
                tmp["Expression"] = expr

                probe_dict[counter] = tmp
                counter += 1
        
    probe_dict = pd.DataFrame(probe_dict).T
    
    f = open("sample_file.txt", "w")
    f.write(pd.DataFrame(probe_dict).to_csv(sep="\t", quoting=csv.QUOTE_NONE))
    f.close()

def gene_expression_unit_tests(ensembl_gene_id, number_of_reads, mean_read_length, total_number_of_reads, length_of_all_genes, fpkm, total_fpkm):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", source = "GEO")
    
    print("FPKM-to-TPM for %s is: " % ensembl_gene_id)
    print(fpkm_to_tpm(ensembl_gene, fpkm, total_fpkm))
    
    print("\nRPKM for %s is: " % ensembl_gene_id)
    print(rpkm(ensembl_gene, number_of_reads, total_number_of_reads))

#   MAIN
if __name__ == "__main__": main()