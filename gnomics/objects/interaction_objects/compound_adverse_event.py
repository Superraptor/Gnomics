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
#   Get adverse events from compound.
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
import gnomics.objects.drug

#   Other imports.
import json
import requests
import time
import timeit

#   MAIN
def main():
    compound_adverse_event_unit_tests("CHEBI:5855", "3672", "")

#   Get adverse events.
def get_adverse_events(com, user=None):
    ae_array = []
    
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["cas registry number", "cas", "cas rn"]:
            mesh_uid = gnomics.objects.compound.Compound.mesh_uid(com)
            drug_mesh_array = []
            for iden in mesh_uid:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden, identifier_type = "MeSH UID")
                drug_mesh_array.append(temp_drug)
            for drug in drug_mesh_array:
                ae_array.extend(gnomics.objects.drug.Drug.adverse_events(drug))
                
    if ae_array:
        return ae_array
            
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["chebi", "chebi id", "chebi identifier"]:
            drugs = gnomics.objects.compound.Compound.drugs(com)
            drugbank_ids = []
            drugbank_drugs = []
            print(drugs)
            for drug in drugs:
                drugbank_id = gnomics.objects.drug.Drug.drugbank_id(drug)
                if drugbank_id:
                    drugbank_drugs.append(drug)
                    drugbank_ids.extend(drugbank_id)
            if drugbank_ids:
                for drug in drugbank_drugs:
                    ae_array.extend(gnomics.objects.drug.Drug.adverse_events(drug))
                    
                    return ae_array
            else:
                # Map to CAS RN.
                print("CAS")
                gnomics.objects.compound.Compound.cas(com)
                return get_adverse_events(com)
                
    if ae_array:
        return ae_array
        
    for ident in com.identifiers:    
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            chebi_id = gnomics.objects.compound.Compound.chebi_id(com)
            if chebi_id:
                return get_adverse_events(com)
            else:
                # Map to CAS RN.
                gnomics.objects.compound.Compound.cas(com)
                return get_adverse_events(com)

#   UNIT TESTS
def compound_adverse_event_unit_tests(chebi_id, pubchem_cid, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    
    pubchem_cid_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting adverse events from PubChem CID (%s):" % pubchem_cid)
    for ae in get_adverse_events(pubchem_cid_com):
        for iden in ae.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("\nGetting adverse events from ChEBI ID (%s):" % chebi_id)
    
    start = timeit.timeit()
    all_ae = get_adverse_events(chebi_com)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for ae in all_ae:
        for iden in ae.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()