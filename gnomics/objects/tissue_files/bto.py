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
from ftplib import FTP
import json
import re
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    hpa_accs = ["adipose tissue", "adrenal gland", "appendix", "bone marrow", "breast", "bronchus", "caudate", "cerebellum", "cerebral cortex", "cervix, uterine", "colon", "duodenum", "endometrium 1", "endometrium 2", "epididymis", "esophagus", "fallopian tube", "gallbladder", "heart muscle", "hippocampus", "kidney", "liver", "lung", "lymph node", "nasopharynx", "oral mucosa", "ovary", "pancreas", "parathyroid gland", "placenta", "prostate", "rectum", "salivary gland", "seminal vesicle", "skeletal muscle", "skin 1", "small intestine", "smooth muscle", "soft tissue 1", "soft tissue 2", "spleen", "stomach 1", "testis", "thyroid gland", "tonsil", "urinary bladder"]
    bto_unit_tests("TS-0171", "UBERON:0002185", hpa_accs, "d4169a1a", "c133be1db72a55682afaf86b94c9e850", "d6f408cd-ffac-4f0f-a645-75c1d966375e")
    
#   Get BTO identifier.
def get_bto_id(tissue, user = None):
    bto_array = []
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "bto" or ident["identifier_type"].lower() == "bto id" or ident["identifier_type"].lower() == "bto identifier":
            bto_array.append(ident["identifier"])
    if bto_array:
        return bto_array
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() == "caloha" or ident["identifier_type"].lower() == "caloha id" or ident["identifier_type"].lower() == "caloha identifier":
            for xref in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user)["primaryTopic"]["hasDbXref"]:
                if "BTO" in xref:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref, identifier_type = "BTO ID", source = "OpenPHACTS")
                    bto_array.append(xref)
        elif ident["identifier_type"].lower() == "hpa id" or ident["identifier_type"].lower() == "hpa identifier" or ident["identifier_type"].lower() == "hpa identifier" or ident["identifier_type"].lower() == "the human protein atlas accession" or ident["identifier_type"].lower() == "human protein atlas accession" or ident["identifier_type"].lower() == "human protein atlas id" or ident["identifier_type"].lower() == "hpa accession":
            ident_proc = ''.join([i for i in ident["identifier"] if not i.isdigit()]).strip()
            ident_proc = ident_proc.replace(" ", "+")
            ftp = FTP("ftp.nextprot.org")
            ftp.login()
            ftp.cwd('pub/current_release/controlled_vocabularies')
            files = ftp.nlst()
            file_name = 'caloha.obo'
            ftp.retrbinary("RETR " + file_name, open("../../data/caloha/" + file_name, 'wb').write)
            temp_dict = {}
            with open('../../data/caloha/caloha.obo', 'r') as temp_file:
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
        elif ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier" or ident["identifier_type"].lower() == "uberon":
            temp_ident = ident["identifier"]
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
    return bto_array

#   UNIT TESTS
def bto_unit_tests(caloha_id, uberon_id, hpa_accs, openphacts_app_id, openphacts_app_key, ncbo_api_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key, ncbo_api_key = ncbo_api_key)
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    print("Getting BTO IDs from CALOHA ID (%s):" % caloha_id)
    for bto in get_bto_id(caloha_tiss, user = user):
        print("- %s" % bto)
    uberon_tiss = gnomics.objects.tissue.Tissue(identifier = uberon_id, identifier_type = "UBERON ID", source = "OpenPHACTS")
    print("\nGetting BTO IDs from UBERON ID (%s):" % uberon_id)
    for bto in get_bto_id(uberon_tiss, user = user):
        print("- %s" % bto)
    for acc in hpa_accs:
        hpa_tiss = gnomics.objects.tissue.Tissue(identifier = acc, identifier_type = "HPA Accession", language = "en", source = "The Human Protein Atlas")
        print("\nGetting UBERON IDs from HPA Accession (%s):" % acc)
        for bto in get_bto_id(hpa_tiss, user = user):
            print("- %s" % bto)
        
#   MAIN
if __name__ == "__main__": main()