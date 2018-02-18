#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

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
#   Convert to and from MedDRA.
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
import gnomics.objects.adverse_event

#   Other imports.
import json
import requests
import time
import timeit

#   MAIN
def main():
    meddra_unit_tests("Diabetes", "10051097", "", "")
    
#   Get MedDRA object.
def get_meddra_obj(adverse_event, user=None, source="umls"):
    obj_array = []
    
    for ae_obj in adverse_event.adverse_event_objects:
        if 'object_type' in com_obj:
            if ae_obj['object_type'].lower() in ['mdr', 'mdr code', 'mdr id', 'mdr identifier', 'meddra', 'meddra code', 'meddra id', 'meddra identifier', 'meddra label', 'meddra object', 'meddra term']:
                return ae_obj['object']
            
    if obj_array:
        return obj_array
    
    ids_completed = []
    if user is not None:
        for meddra_term in get_meddra_term(adverse_event):
            if source.lower() in ["umls", "all"] and meddra_term not in ids_completed and user.umls_api_key is not None:
            
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/search/current?sabs=MDR&searchType=exact&returnIdType=code"
                
                id_array = []
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"string": str(meddra_term), "ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    if not r.ok:
                        break
                    else:
                        items = json.loads(r.text)
                        json_data = items["result"]
                        if json_data["results"][0]["ui"] == "NONE":
                            break
                        else:
                            id_array.append(json_data)
                            
                if id_array:       
                    gnomics.objects.adverse_event.AdverseEvent.add_object(adverse_event, obj = id_array, object_type = "MedDRA Object")
                    obj_array.append(id_array)
                
                if source.lower() != "all":
                    ids_completed.append(meddra_term)
                    
            if source.lower() in ["ncbo", "all"] and meddra_term not in ids_completed and user.ncbo_api_key is not None:
            
                base = "http://data.bioontology.org/search"
                ext = "?q=" + str(meddra_term) + "&ontologies=MEDDRA&require_exact_match=true&roots_only=true/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

                if not r.ok:
                    continue
                else:
                    decoded = json.loads(r.text)

                    id_array = []
                    for result in decoded["collection"]:
                        id_array.append(result)
                        
                    if id_array:
                        gnomics.objects.adverse_event.AdverseEvent.add_object(adverse_event, obj = id_array, object_type = "MedDRA Object")
                        obj_array.append(id_array)
                        
                    if source.lower() != "all":
                        ids_completed.append(meddra_term)

        return obj_array
    
    else:
        print("MedDRA object cannot be obtained without valid user object (with valid UMLS API key or NCBO API key).")

#   Get MedDRA ID.
def get_meddra_id(adverse_event, user):
    id_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["mdr", "mdr code", "mdr id", "mdr identifier", "meddra", "meddra code", "meddra id", "meddra identifier"]):
        if iden["identifier"] not in id_array:
            id_array.append(iden["identifier"])
            
    if id_array:
        return id_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["mdr label", "mdr term", "meddra label", "meddra term"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for obj in get_meddra_obj(adverse_event, user, source="all"):
                for iden_obj in obj:
                    if "results" in iden_obj:
                        for res in iden_obj["results"]:
                            if res["ui"] not in id_array:
                                meddra_id = res["ui"]
                                meddra_name = res["name"]
                                id_array.append(meddra_id)
                                gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = meddra_id, identifier_type = "MedDRA ID", language = "en", source = "UMLS", name = meddra_name)
                                
                    elif "@id" in iden_obj:
                        if "/MEDDRA/" in iden_obj["@id"]:
                            if iden_obj["@id"].split("/MEDDRA/")[1] not in id_array:
                                meddra_id = iden_obj["@id"].split("/MEDDRA/")[1]
                                meddra_name = iden_obj["prefLabel"]
                                id_array.append(meddra_id)
                                gnomics.objects.adverse_event.AdverseEvent.add_identifier(adverse_event, identifier = meddra_id, identifier_type = "MedDRA ID", language = "en", source = "NCBO BioPortal", name = meddra_name)
                    else:
                        print("Malformed MedDRA object.")
        
    return id_array

#   Get MedDRA Term.
def get_meddra_term(adverse_event, user=None):
    id_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(adverse_event.identifiers, ["mdr label", "mdr term", "meddra label", "meddra term"]):
        if iden["identifier"] not in id_array:
            id_array.append(iden["identifier"])
            
    return id_array

#   UNIT TESTS
def meddra_unit_tests(meddra_term, meddra_id, umls_api_key, ncbo_api_key):
    
    user = User(umls_api_key = umls_api_key, ncbo_api_key = ncbo_api_key)
    
    meddra_term_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "UMLS")
    print("Getting MedDRA IDs from MedDRA term (%s):" % meddra_term)
    start = timeit.timeit()
    meddra_array = get_meddra_id(meddra_term_ae, user=user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for med in meddra_array:
        print("\t- %s" % str(med))
        

#   MAIN
if __name__ == "__main__": main()