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
#   Get PubChem CIDs and PubChem SIDs.
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

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    cid_unit_tests("33510", "C01576", "Q418817", "")
    sids_unit_tests("6918092")
    
# Returns PubChem compound from CID.
def get_pubchem_compound(compound, user=None):
    pubchem_array = []
    
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['pubchem compound', 'pubchem', 'pubchem compound object']:
                pubchem_array.append(com_obj['object'])
                
    if pubchem_array:
        return pubchem_array
    
    for pubchem_cid in get_pubchem_cids(compound, user = user):
        pubchem_compound = pubchem.Compound.from_cid(pubchem_cid)
        gnomics.objects.compound.Compound.add_object(compound, obj=pubchem_compound, object_type="PubChem Compound")
        pubchem_array.append(pubchem_compound)
        
    return pubchem_array

#   Get CID.
def get_pubchem_cids(com, user=None):
    cid_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in cid_array:
            cid_array.append(iden["identifier"])
            
    if cid_array:
        return cid_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            results = pubchem.get_compounds(gnomics.objects.compound.Compound.inchi(com, user = user), 'inchi')
            
            for x in results:
                gnomics.objects.compound.Compound.add_identifier(com, identifier=x.cid, identifier_type="PubChem CID", language=None, source="PubChem")
                cid_array.append(x.cid)
                
        elif user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for kegg_com in gnomics.objects.compound.Compound.kegg_compound_db_entry(com):
            
                # Returns PubChem SID.
                pubchem_sid = str(kegg_com["DBLINKS"]["PubChem"])

                # Get CIDs from SIDs.
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/substance/sid/" + str(pubchem_sid) + "/JSONP"

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong when trying to access the PubChem PUG REST.")
                else:
                    str_r = r.text
                    try:
                        l_index = str_r.index("(") + 1
                        r_index = str_r.rindex(")")
                        res = str_r[l_index:r_index]
                        decoded = json.loads(res)
                        for temp_com in decoded["PC_Substances"][0]["compound"]:
                            if "id" in temp_com:
                                if temp_com["id"]["type"] == 1 and "id" in temp_com["id"]:
                                    if "cid" in temp_com["id"]["id"]:
                                        if temp_com["id"]["id"]["cid"] not in cid_array:
                                            cid_array.append(temp_com["id"]["id"]["cid"])
                                            gnomics.objects.compound.Compound.add_identifier(com, identifier=temp_com["id"]["id"]["cid"], identifier_type="PubChem CID", source="KEGG", language=None)

                    except ValueError:
                        print("Input is not in a JSONP format.")

    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in gnomics.objects.compound.Compound.wikidata(com):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "pubchem cid", wikidata_property_language = "en")

                for x in found_array:
                    if x not in cid_array:
                        cid_array.append(x)
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = x, identifier_type = "PubChem CID", language = None, source = "Wikidata")
            
    return cid_array
            
#   Get SIDs.
def get_pubchem_sids(com, user=None):
    
    sid_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["sid", "pubchem sid", "pubchem substance", "pubchem substance id", "pubchem substance identifier"]):
        if iden["identifier"] not in sid_array:
            sid_array.append(iden["identifier"])
            
    if sid_array:
        return sid_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
    
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com):
                sid_array_from_pubchem = sub_com.sids
                for sid in sid_array_from_pubchem:
                    if sid not in sid_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier=sid, language=None, identifier_type="PubChem SID", source="PubChem")
                        sid_array.append(sid)
            
    return sid_array

#   UNIT TESTS
def cid_unit_tests(chemspider_id, kegg_compound_id, wikidata_accession, chemspider_security_token=None):
    if chemspider_security_token is not None:
        print("\nCreating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting PubChem CID from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        cid_array = get_pubchem_cids(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cid_array:
            print("\t- %s" % str(com))

        kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting PubChem CID from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        cid_array = get_pubchem_cids(kegg_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cid_array:
            print("\t- %s" % str(com))
            
        wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
        print("\nGetting PubChem CID from Wikidata Accession (%s):" % wikidata_accession)
        start = timeit.timeit()
        cid_array = get_pubchem_cids(wikidata_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cid_array:
            print("\t- %s" % str(com))
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with KEGG Compound conversion...\n")
        
        kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("Getting PubChem CID from KEGG Compund ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        cid_array = get_pubchem_cids(kegg_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cid_array:
            print("\t- %s" % str(com))
            
def sids_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting PubChem SIDs from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    sid_array = get_pubchem_sids(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in sid_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()