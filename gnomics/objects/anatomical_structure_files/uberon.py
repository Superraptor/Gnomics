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
#   Get UWDA identifiers.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
from urllib.parse import urlencode, quote_plus
import json
import requests
import timeit

#   MAIN
def main():
    uberon_unit_tests("UBERON:0001424", "Q199507")

# Return UBERON object.
def get_uberon_obj(anat, user=None):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() in ["uberon id", "uberon identifier", "uberon"]:
            if ":" in iden["identifier"]:
                temp_iden = iden["identifier"].replace(':', '_')
                norm_url = "http://purl.obolibrary.org/obo/" + temp_iden
                
                payload = {'term': norm_url}
                result_url = urlencode(payload)
                encode_payload = {'term': result_url}
                encode_result_url = urlencode(encode_payload)
                
                url = "http://www.ebi.ac.uk/ols/api/"
                ext = "ontologies/uberon/terms/" + encode_result_url.split("%3D")[1]

                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj=decoded, object_type="UBERON")
                
                return decoded
                
            elif "_" in iden["identifier"]:
                norm_url = "http://purl.obolibrary.org/obo/" + iden["identifier"]
                
                payload = {'term': norm_url}
                result_url = urlencode(payload)
                encode_payload = {'term': result_url}
                encode_result_url = urlencode(encode_payload)
                
                url = "http://www.ebi.ac.uk/ols/api/"
                ext = "ontologies/uberon/terms/" + encode_result_url.split("%3D")[1]

                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj=decoded, object_type="UBERON")
                
                return decoded
                
            else:
                print("UBERON identifier is not in the correct format to allow for double URL encoding in the OLS.")
            
#   Get UBERON ID.
def get_uberon_id(anat, user=None):
    uberon_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in uberon_array:
            uberon_array.append(iden["identifier"])
            
    if uberon_array:
        return uberon_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "umls cui", wikidata_property_language = "en")

                for x in found_array:
                    if x not in uberon_array:
                        uberon_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "UBERON ID", language = None, source = "Wikidata")
    
    return uberon_array
    
    
#   UNIT TESTS
def uberon_unit_tests(uberon_id, wikidata_accession):
            
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uberon_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", source = "Wikidata")
    
    print("\nGetting UBERON ID from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    uberon_array = get_uberon_id(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for uberon in uberon_array:
        print("\t- " + str(uberon))
    
#   MAIN
if __name__ == "__main__": main()