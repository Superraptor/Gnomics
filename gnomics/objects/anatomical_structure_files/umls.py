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
#   UMLS.
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
import gnomics.objects.auxiliary_files.wiki

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    umls_unit_tests("Q199507", "Ulna", "UBERON:0001424")
    
# Return UMLS CUI.
def get_umls_cui(anat, user=None):
    umls_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["umls", "umls concept uid", "umls concept unique id", "umls concept unique identifier", "umls cui", "umls id", "umls identifier"]):
        if iden["identifier"] not in umls_array:
            umls_array.append(iden["identifier"])
            
    if umls_array:
        return umls_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "umls cui", wikidata_property_language = "en")

                for x in found_array:
                    if x not in umls_array:
                        umls_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "UMLS CUI", language = None, source = "Wikidata")
                        
    if umls_array:
        return umls_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["language"] == "en" and iden["identifier"] not in ids_completed:
            
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "umls cui", wikidata_property_language = "en")

                for x in found_array:
                    if x not in umls_array:
                        umls_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "UMLS CUI", language = None, source = "Wikidata")
                            
    if umls_array:        
        return umls_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            
            ids_completed.append(iden["identifier"]) 
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "umls cui", wikidata_property_language = "en")

                for x in found_array:
                    if x not in umls_array:
                        umls_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "UMLS CUI", language = None, source = "Wikidata")
                            
    return umls_array
    
#   UNIT TESTS
def umls_unit_tests(wikidata_accession, wikipedia_accession, uberon_id):
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    
    print("\nGetting UMLS CUI from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    umls_array = get_umls_cui(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for umls in umls_array:
        print("\t- " + str(umls))
        
    wikipedia_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikipedia_accession, identifier_type = "Wikipedia Accession", language = "en", source = "Wikipedia")
    
    print("\nGetting UMLS CUI from Wikipedia Accession (%s):" % wikipedia_accession)
    start = timeit.timeit()
    umls_array = get_umls_cui(wikipedia_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for umls in umls_array:
        print("\t- " + str(umls))
        
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = str(uberon_id), identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    
    print("\nGetting UMLS CUI from UBERON ID (%s):" % uberon_id)
    start = timeit.timeit()
    umls_array = get_umls_cui(uberon_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for umls in umls_array:
        print("\t- " + str(umls))
    
#   MAIN
if __name__ == "__main__": main()