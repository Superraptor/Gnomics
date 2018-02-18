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
#   Get UBERON identifiers.
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
import requests
import timeit
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    uberon_unit_tests("TS-0171", "BTO:0001418", "", "", "")

#   Get UBERON term.
def get_uberon_term(tissue, user = None):
    uberon_array = []
    uberon_id_array = []
    
    for ident in tissue.identifiers:
        if ident["identifier_type"].lower() in ["uberon label", "uberon term"]:
            uberon_array.append(ident["identifier"])

    if uberon_array:
        return uberon_array
    
    ids_completed = []
    for ident in tissue.identifiers:
        if (ident["identifier_type"].lower() in ["uberon", "uberon id", "uberon identifier"]) and ident["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key:
                ids_completed.append(ident["identifier"])

                temp_ident = ident["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                full_url = "http://data.bioontology.org/ontologies/UBERON/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + str(temp_ident) + "/?apikey=" + user.ncbo_api_key
                
                r = requests.get(full_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    continue
                else:
                    decoded = json.loads(r.text)
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = decoded["prefLabel"], identifier_type = "UBERON Term", source = "NCBO BioPortal", language = "en")
                    uberon_array.append(decoded["prefLabel"])
                    
            else:
                print("Operation cannot be performed without a valid NCBO API key attached to a valid user object.")
                    
    return uberon_array

#   Get UBERON identifier.
def get_uberon_id(tissue, user = None):
    uberon_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in uberon_array:
            uberon_array.append(iden["identifier"])
            
    if uberon_array:
        return uberon_array
    
    ids_completed = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["caloha", "caloha id", "caloha identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            if user is not None:
                if "hasDbXref" in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user)["primaryTopic"]:
                    for xref in gnomics.objects.tissue.Tissue.caloha_obj(tissue, user = user)["primaryTopic"]["hasDbXref"]:
                        if "UBERON" in xref:
                            gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = xref, identifier_type = "UBERON ID", source = "OpenPHACTS")
                            uberon_array.append(xref)
                
            else:
                print("Operation cannot be performed without valid OpenPHACTS API keys attached to a valid user object.")
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["brenda tissue ontology id", "brenda tissue ontology identifier", "bto", "bto id", "bto identifier"] and ident["identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            if user is not None:
                temp_ident = ident["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "BTO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Link not functional.")
                else:
                    decoded = json.loads(r.text)
                    for result in decoded:
                        for subresult in result["classes"]:
                            if "UBERON" in subresult["@id"]:
                                uberon_id = subresult["@id"].split("/obo/")[1]
                                if uberon_id not in uberon_array:
                                    uberon_array.append(uberon_id)
                                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier = uberon_id, identifier_type = "UBERON ID", source = "NCBO BioPortal")
                
            else:
                print("Operation cannot be performed without a valid NCBO API key attached to a valid user object.")
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl tissue", "chembl tissue id", "chembl tissue identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            tissue_temp = new_client.tissue
            res = tissue_temp.filter(chembl_id=iden["identifier"])
            
            for sub_res in res:
                if sub_res["uberon_id"] not in uberon_array:
                    gnomics.objects.tissue.Tissue.add_identifier(tissue, identifier=sub_res["uberon_id"], identifier_type="UBERON ID", source="ChEMBL", name=sub_res["pref_name"])
                    uberon_array.append(sub_res["uberon_id"])
                    
    return uberon_array

#   UNIT TESTS
def uberon_unit_tests(caloha_id, bto_id, openphacts_app_id, openphacts_app_key, ncbo_api_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key, ncbo_api_key = ncbo_api_key)
    
    caloha_tiss = gnomics.objects.tissue.Tissue(identifier = caloha_id, identifier_type = "CALOHA ID", source = "OpenPHACTS")
    print("Getting UBERON IDs from CALOHA ID (%s):" % caloha_id)
    for uberon in get_uberon_id(caloha_tiss, user = user):
        print("- %s" % uberon)
        
    bto_tiss = gnomics.objects.tissue.Tissue(identifier = bto_id, identifier_type = "BTO ID", source = "OpenPHACTS")
    print("\nGetting UBERON IDs from BTO ID (%s):" % bto_id)
    for uberon in get_uberon_id(bto_tiss, user = user):
        print("- %s" % uberon)
        
#   MAIN
if __name__ == "__main__": main()