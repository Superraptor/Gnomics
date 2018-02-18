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
#   BNCF Thesaurus.
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
import json
import requests
import timeit

#   MAIN
def main():
    bncf_unit_tests("Q199507")
    
# Return BNCF Thesaurus ID.
def get_bncf_thesaurus(anat, user=None):
    bncf_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["bncf", "bncf thesaurus", "bncf thesaurus id", "bncf thesaurus identifier"]):
        if iden["identifier"] not in bncf_array:
            bncf_array.append(iden["identifier"])
            
    if bncf_array:
        return bncf_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "bncf thesaurus":
                        for x in prop_dict:
                            if x not in bncf_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "BNCF Thesaurus", language = None, source = "Wikidata")
                                bncf_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if bncf_array:
        return bncf_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia accession", "wikipedia", "wikipedia article"]):
        if iden["identifier"] not in ids_completed and iden["language"].lower() == "en":
            ids_completed.append(iden["identifier"])
            
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "bncf thesaurus":
                        for x in prop_dict:
                            if x not in bncf_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "BNCF Thesaurus", language = None, source = "Wikidata")
                                bncf_array.append(x["mainsnak"]["datavalue"]["value"])
    if bncf_array:        
        return bncf_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "bncf thesaurus":
                        for x in prop_dict:
                            if x not in bncf_array:
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "BNCF Thesaurus", language = None, source = "Wikidata")
                                bncf_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return bncf_array
    
#   UNIT TESTS
def bncf_unit_tests(wikidata_accession):
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    
    print("Getting BNCF Thesaurus from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    bncf_array = get_bncf_thesaurus(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for bncf in bncf_array:
        print("\t- %s" % str(bncf))
    
#   MAIN
if __name__ == "__main__": main()