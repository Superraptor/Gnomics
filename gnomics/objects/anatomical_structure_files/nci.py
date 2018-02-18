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
#   NCI Thesaurus.
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
    nci_unit_tests("Q199507")
    
# Return NCI Thesaurus ID.
def get_nci_thesaurus_id(anat, user=None):
    nci_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["nci thesaurus id", "nci thesaurus identifier", "nci id", "nci identifier", "ncit id", "ncit identifier"]:
            nci_array.append(ident["identifier"])
            
    if nci_array:
        return nci_array
            
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
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
                    
                    if en_prop_name.lower() == "nci thesaurus id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NCI Thesaurus ID", language = None, source = "Wikidata")
                            nci_array.append(x["mainsnak"]["datavalue"]["value"])
    
    if nci_array:
        return nci_array
    
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"].lower() == "en":
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
                    
                    if en_prop_name.lower() == "nci thesaurus id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NCI Thesaurus ID", language = None, source = "Wikidata")
                            nci_array.append(x["mainsnak"]["datavalue"]["value"])
    if nci_array:        
        return nci_array
    
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() in ["uberon", "uberon id", "uberon identifier"]:
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language="en")
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
                    
                    if en_prop_name.lower() == "nci thesaurus id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NCI Thesaurus ID", language = None, source = "Wikidata")
                            nci_array.append(x["mainsnak"]["datavalue"]["value"])
                            
    return nci_array
    
#   UNIT TESTS
def nci_unit_tests(wikidata_accession):
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    print("Getting NCI Thesaurus ID from Wikidata Accession (%s):" % wikidata_accession)
    for nci in get_nci_thesaurus_id(wikidata_anat):
        print("- %s" % nci)
    
#   MAIN
if __name__ == "__main__": main()