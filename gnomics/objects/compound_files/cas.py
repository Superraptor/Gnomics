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
#   Get CAS registry numbers.
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
import json
import pubchempy as pubchem
import re
import requests
import timeit

#   MAIN
def main():
    cas_unit_tests("CHEBI:4911", "33510", "C01576", "6918092", "Q418817", "fd4ce40f-23e5-44be-91f5-a40b92ab1580")

#   Get CAS.
def get_cas(com, user=None):
    cas_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in cas_array:
            cas_array.append(iden["identifier"])
            
    if cas_array:
        return cas_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "cas registry number" and accession._DatabaseAccession__accession_number not in cas_array:

                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, language = None, identifier_type = "CAS Registry Number", source = "ChEBI")
                        cas_array.append(accession._DatabaseAccession__accession_number)
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            cas_num_regex = re.compile("^([0-9]{2,7}-[0-9]{2}-[0-9])$")
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com, user = user)) + "/synonyms/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                print("Something went wrong while trying to attain a PubChem PUG REST connection...")
            else:
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.rindex(")")
                    
                    res = str_r[l_index:r_index]
                    decoded = json.loads(res)
                    synonym_list = decoded["InformationList"]["Information"][0]["Synonym"]
                    final_num = []
                    for synonym in synonym_list:
                        if re.match(cas_num_regex, synonym) and synonym not in cas_array:
                            
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = synonym, language = None, identifier_type = "CAS Registry Number", source = "PubChem")
                            cas_array.append(synonym)
                    
                except ValueError:
                    print("Input is not in a JSONP format.")
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):

        server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        ext = "/compound/cid/" + str(iden["identifier"]) + "/xrefs/RN/JSONP"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            print("Something went wrong while trying to attain a PubChem PUG REST connection...")
        else:
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rindex(")")

                res = str_r[l_index:r_index]
                decoded = json.loads(res)
                for result in decoded["InformationList"]["Information"]:
                    regi = result["RN"]
                    for reg in regi:
                        if reg not in cas_array:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = reg, identifier_type = "CAS Registry Number", source = "PubChem", language = None)

                            cas_array.append(reg)

            except ValueError:
                print("Input is not in a JSONP format.")

    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])

            for wikidata_object in gnomics.objects.compound.Compound.wikidata(com):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "cas registry number", wikidata_property_language = "en")

                for x in found_array:
                    if x not in cas_array:
                        cas_array.append(x)
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = x, identifier_type = "CAS Registry Number", language = None, source = "Wikidata")
                            
    if cas_array:
        return cas_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_cas(com, user = user)
        
    return cas_array

#   UNIT TESTS
def cas_unit_tests(chebi_id, chemspider_id, kegg_compound_id, pubchem_cid, wikidata_accession, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("\nGetting CAS Registry Number from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        cas_array = get_cas(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
            
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting CAS Registry Number from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        cas_array = get_cas(chebi_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
            
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting CAS Registry Number from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        cas_array = get_cas(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting CAS Registry Number from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        cas_array = get_cas(kegg_compound_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
            
        wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
        print("\nGetting CAS Registry Number from Wikidata Accession (%s):" % wikidata_accession)
        start = timeit.timeit()
        cas_array = get_cas(wikidata_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI ID conversion...\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting CAS Registry Number from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        cas_array = get_cas(chebi_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
            
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting external registry IDs from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        cas_array = get_cas(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting CAS Registry Number from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        cas_array = get_cas(kegg_compound_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in cas_array:
            print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()