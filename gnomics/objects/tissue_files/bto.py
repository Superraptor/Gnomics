#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#

#
#   Get BTO (BRENDA Tissue Ontology) identifiers.
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
import gnomics.objects.tissue

#   Other imports.
from chembl_webresource_client.new_client import new_client
from ftplib import FTP
import json
import re
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    # The following do not map to UBERON: caudate, soft tissue 1, soft tissue 2
    hpa_accs = ["adipose tissue", "adrenal gland", "appendix", "bone marrow", "breast", "bronchus", "caudate", "cerebellum", "cerebral cortex", "cervix, uterine", "colon", "duodenum", "endometrium 1", "endometrium 2", "epididymis", "esophagus", "fallopian tube", "gallbladder", "heart muscle", "hippocampus", "kidney", "liver", "lung", "lymph node", "nasopharynx", "oral mucosa", "ovary", "pancreas", "parathyroid gland", "placenta", "prostate", "rectum", "salivary gland", "seminal vesicle", "skeletal muscle", "skin 1", "small intestine", "smooth muscle", "soft tissue 1", "soft tissue 2", "spleen", "stomach 1", "testis", "thyroid gland", "tonsil", "urinary bladder"]
    
    bto_unit_tests("TS-0171", "UBERON:0002185", hpa_accs, "CHEMBL3638205", "", "", "")
    
#   Get BTO identifier.
def get_bto_id(tissue, user=None):
    bto_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["brenda tissue ontology id", "brenda tissue ontology identifier", "bto", "bto id", "bto identifier"]):
        if iden["identifier"] not in bto_array:
            bto_array.append(iden["identifier"])
            
    if bto_array:
        return bto_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["caloha", "caloha id", "caloha identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
    
            for sub_tiss in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user):
                for xref in sub_tiss["primaryTopic"]["hasDbXref"]:
                    if "BTO" in xref:
                        gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref, identifier_type = "BTO ID", source = "OpenPHACTS")
                        bto_array.append(xref)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["hpa", "hpa accession", "hpa id", "hpa identifier", "human protein atlas", "human protein atlas accession", "human protein atlas id", "human protein atlas identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            ident_proc = ''.join([i for i in iden["identifier"] if not i.isdigit()]).strip()
            ident_proc = ident_proc.replace(" ", "+")
            
            ftp = FTP("ftp.nextprot.org")
            ftp.login()
            ftp.cwd('pub/current_release/controlled_vocabularies')
            files = ftp.nlst()
            file_name = 'caloha.obo'
            ftp.retrbinary("RETR " + file_name, open("../../data/caloha/" + file_name, 'wb').write)
            
            temp_dict = {}
            with open('../../data/caloha/caloha.obo', 'r') as temp_file:
            #    print(ident_proc)
                new_term = False
                key = None
                found_term = False
                found_term_keys = []
                for line in temp_file:
                    if key is not None:
                        temp_dict[key].append(line)
                        sp_ident_proc = "/" + ident_proc
                        sp_2_ident_proc = '"' + ident_proc + '"'
                        if sp_ident_proc in line and "proteinatlas" in line:
                            found_term = True
                            if key not in found_term_keys:
                                found_term_keys.append(key)
                        elif "name" in line:
                            proc_name = line.replace("name: ", "").strip().lower().replace(" ", "+")
                            if proc_name == ident_proc:
                                found_term = True
                                if key not in found_term_keys:
                                    found_term_keys.append(key)
                        elif sp_2_ident_proc in line.lower() and "synonym" in line:
                            proc_name = line.replace("synonym: ", "").strip().replace(" RELATED []", "").strip().replace('"', '').strip().lower()
                            if proc_name == ident_proc:
                                found_term = True
                                if key not in found_term_keys:
                                    found_term_keys.append(key)
                    if new_term == True:
                        if line not in temp_dict:
                            temp_dict[line] = []
                            key = line
                        new_term = False
                    if "[Term]" in line:
                        new_term = True
                if found_term_keys:
                    for found_term_key in found_term_keys:
                        for entry in temp_dict[found_term_key]:
                            if "BTO" in entry:
                                xref = entry.strip().replace("xref: ", "")
                                gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref, identifier_type = "BTO ID", source = "neXtProt")
                                bto_array.append(xref)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "UBERON/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for result in decoded:
                    for subresult in result["classes"]:
                        if "BTO" in subresult["@id"]:
                            bto_id = subresult["@id"].split("/obo/")[1]
                            if bto_id not in bto_array:
                                bto_array.append(bto_id)
                                gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = bto_id, identifier_type = "BTO ID", source = "NCBO BioPortal")
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl tissue", "chembl tissue id", "chembl tissue identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            tissue_temp = new_client.tissue
            res = tissue_temp.filter(chembl_id=iden["identifier"])
            
            for sub_res in res:
                if sub_res["bto_id"] not in bto_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["bto_id"], identifier_type="BTO ID", source="ChEMBL", name=sub_res["pref_name"])
                    bto_array.append(sub_res["bto_id"])
 
    return bto_array

#   UNIT TESTS
def bto_unit_tests(caloha_id, uberon_id, hpa_accs, chembl_id, openphacts_app_id, openphacts_app_key, ncbo_api_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key, ncbo_api_key = ncbo_api_key)
    
    chembl_tiss = gnomics.objects.tissue.Tissue(identifier = chembl_id, identifier_type = "ChEMBL ID", source = "ChEMBL")
    
    print("\nGetting BTO IDs from ChEMBL ID (%s):" % chembl_id)
    start = timeit.timeit()
    bto_array = get_bto_id(chembl_tiss, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for tiss in bto_array:
        print("\t- %s" % str(tiss))
    
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    
    print("\nGetting BTO IDs from CALOHA ID (%s):" % caloha_id)
    start = timeit.timeit()
    bto_array = get_bto_id(caloha_tiss, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for tiss in bto_array:
        print("\t- %s" % str(tiss))

    uberon_tiss = gnomics.objects.tissue.Tissue(identifier = uberon_id, identifier_type = "UBERON ID", source = "OpenPHACTS")
    
    print("\nGetting BTO IDs from UBERON ID (%s):" % uberon_id)
    start = timeit.timeit()
    bto_array = get_bto_id(uberon_tiss, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for tiss in bto_array:
        print("\t- %s" % str(tiss))
        
    for acc in hpa_accs:
        hpa_tiss = gnomics.objects.tissue.Tissue(identifier = acc, identifier_type = "HPA Accession", language = "en", source = "The Human Protein Atlas")
        print("\nGetting UBERON IDs from HPA Accession (%s):" % acc)
        start = timeit.timeit()
        hpa_array = get_bto_id(hpa_tiss, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for tiss in hpa_array:
            print("\t- %s" % str(tiss))
        
#   MAIN
if __name__ == "__main__": main()