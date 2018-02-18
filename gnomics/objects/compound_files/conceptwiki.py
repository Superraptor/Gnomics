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
#   Get ConceptWiki.
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
from ssl import SSLError
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    conceptwiki_unit_tests("38932552-111f-4a4e-a46a-4ed1d7bdf9d5", "187440", "CHEMBL1336", "SCHEMBL8218", "", "")
    
#   Get ConceptWiki object.
#
#   _format
#   _callback
#   _metadata
def get_conceptwiki_obj(com, user=None, verbose=False):
    conceptwiki_array = []
    
    for com_obj in com.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['conceptwiki object', 'conceptwiki']:
                conceptwiki_array.append(com_obj['object'])
                
    if conceptwiki_array:
        return conceptwiki_array
    
    ids_completed = []
    
    for iden in gnomics.objects.compound.Compound.chemspider_id(com, user = user):
        if iden not in ids_completed and user is not None:
            ids_completed.append(iden)
            
            if user.openphacts_app_id is not None and user.openphacts_app_key is not None:
            
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.chemspider.com%2F" + str(iden) + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

                try:
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        print("There was a problem connecting to OpenPHACTS.")
                    else:
                        decoded = json.loads(r.text)
                        gnomics.objects.compound.Compound.add_object(com, obj=decoded["result"], object_type="ConceptWiki Object")
                        conceptwiki_array.append(decoded["result"])
                except SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                except requests.exceptions.SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                else:
                    break
    
    for iden in gnomics.objects.compound.Compound.chembl_id(com, user=user):
        if iden not in ids_completed and user is not None:
            ids_completed.append(iden)
            
            if user.openphacts_app_id is not None and user.openphacts_app_key is not None:
            
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fchembl%2Fmolecule%2F" + str(iden) + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

                try:
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        print("There was a problem connecting to OpenPHACTS.")
                    else:
                        decoded = json.loads(r.text)
                        gnomics.objects.compound.Compound.add_object(com, obj=decoded["result"], object_type="ConceptWiki Object")
                        conceptwiki_array.append(decoded["result"])
                except SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                except requests.exceptions.SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                else:
                    break
        
    for iden in gnomics.objects.compound.Compound.schembl_id(com, user=user):
        if iden not in ids_completed and user is not None:
            ids_completed.append(iden)
            
            if user.openphacts_app_id is not None and user.openphacts_app_key is not None:
            
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fsurechembl%2Fmolecule%2F" + str(iden) + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

                try:
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        print("There was a problem connecting to OpenPHACTS.")
                    else:
                        decoded = json.loads(r.text)
                        gnomics.objects.compound.Compound.add_object(com, obj=decoded["result"], object_type="ConceptWiki Object")
                        conceptwiki_array.append(decoded["result"])
                except SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                except requests.exceptions.SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                else:
                    break
            
    for iden in get_conceptwiki_id(com, user=user):
        if iden not in ids_completed and user is not None:
            ids_completed.append(iden)
            
            if user.openphacts_app_id is not None and user.openphacts_app_key is not None:
            
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Fwww.conceptwiki.org%2Fconcept%2F" + str(iden) + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

                try:
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        print("There was a problem connecting to OpenPHACTS.")
                    else:
                        decoded = json.loads(r.text)
                        gnomics.objects.compound.Compound.add_object(com, obj=decoded["result"], object_type="ConceptWiki Object")
                        conceptwiki_array.append(decoded["result"])
                except SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                except requests.exceptions.SSLError as e:
                    if verbose:
                        print("A SSL error occurred while attempting request.")
                        print("ERROR: %s" % str(e))
                    break
                else:
                    break
            
    return conceptwiki_array
    
#   Get ConceptWiki ID.
def get_conceptwiki_id(com, user=None):
    
    conceptwiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["concept wiki", "concept wiki id", "concept wiki identifier", "conceptwiki", "conceptwiki id", "conceptwiki identifier"]):
        if iden["identifier"] not in conceptwiki_array:
            conceptwiki_array.append(iden["identifier"])
            
    if conceptwiki_array:
        return conceptwiki_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            cs_uri = "http://rdf.chemspider.com/" + iden["identifier"]
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"] and subitem["_about"].split("/concept/")[1] not in conceptwiki_array:
                            
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1], identifier_type = "ConceptWiki ID", language = None, source = "OpenPHACTS") 
                            conceptwiki_array.append(subitem["_about"].split("/concept/")[1])
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl compound", "chembl compound id", "chembl compound identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            chembl_uri = "http://rdf.ebi.ac.uk/resource/chembl/molecule/" + iden["identifier"]
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"] and subitem["_about"].split("/concept/")[1] not in conceptwiki_array:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1], identifier_type = "ConceptWiki ID", language = None, source = "OpenPHACTS")
                            conceptwiki_array.append(subitem["_about"].split("/concept/")[1])
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["schembl", "schembl id", "schembl identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            schembl_uri = "http://rdf.ebi.ac.uk/resource/surechembl/molecule/" + iden["identifier"]
            
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"] and subitem["_about"].split("/concept/")[1] not in conceptwiki_array:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1], identifier_type = "ConceptWiki ID", source = "OpenPHACTS", language = None)
                            conceptwiki_array.append(subitem["_about"].split("/concept/")[1])
    
    return conceptwiki_array

#   UNIT TESTS
def conceptwiki_unit_tests(conceptwiki_id, chemspider_id, chembl_id, schembl_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    conceptwiki_com = gnomics.objects.compound.Compound(identifier = conceptwiki_id, identifier_type = "ConceptWiki ID", source = "OpenPHACTS")
    
    chemspider_com = gnomics.objects.compound.Compound(identifier = chemspider_id, identifier_type = "ChemSpider ID", source = "OpenPHACTS")
    print("Getting ConceptWiki IDs from ChemSpider ID (%s):" % chemspider_id)
    start = timeit.timeit()
    conceptwiki_array = get_conceptwiki_id(chemspider_com, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in conceptwiki_array:
        print("\t- %s" % str(com))
    
    chembl_com = gnomics.objects.compound.Compound(identifier = chembl_id, identifier_type = "ChEMBL ID", source = "OpenPHACTS")
    print("\nGetting ConceptWiki IDs from ChEMBL ID (%s):" % chembl_id)
    start = timeit.timeit()
    conceptwiki_array = get_conceptwiki_id(chembl_com, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in conceptwiki_array:
        print("\t- %s" % str(com))
    
    schembl_com = gnomics.objects.compound.Compound(identifier = schembl_id, identifier_type = "SCHEMBL ID", source = "OpenPHACTS")
    print("\nGetting ConceptWiki IDs from SCHEMBL ID (%s):" % schembl_id)
    
    start = timeit.timeit()
    conceptwiki_array = get_conceptwiki_id(schembl_com, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in conceptwiki_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()