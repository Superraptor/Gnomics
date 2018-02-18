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
#   Get EOL (Encyclopedia of Life).
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
import gnomics.objects.gene
import gnomics.objects.taxon

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    eol_unit_tests("328067", "180542", "180542", "180542", "180542", "Q15978631", eol_api_key = "")
    
#   Get EOL object.
#
#   All parameters are discussed in-depth here:
#   http://eol.org/api/docs/pages/1.0
#
#   batch: True, False
#   id: [any string]
#   images_per_page: 0-75
#   images_page: [any integer]
#   videos_per_page: 0-75
#   videos_page: [any integer]
#   sounds_per_page: 0-75
#   sounds_page: [any integer]
#   maps_per_page: 0-75
#   maps_page: [any integer]
#   texts_per_page: 0-75
#   texts_page: [any integer]
#   subjects: [in-depth discussion is available here:
#       http://eol.org/info/toc_subjects] 
#       [pipe-delimited, |, for multiple]
#   - all
#   - overview
#   - TaxonBiology
#   - Description
#   - GeneralDescription
#   - Biology
#   - Distribution
#   - Morphology
#   - Size
#   - DiagnosticDescription
#   - LookAlikes
#   - Development
#   - Habitat
#   - Migration
#   - Dispersal
#   - TrophicStrategy
#   - Associations
#   - Diseases
#   - PopulationBiology
#   - Ecology
#   - Behaviour
#   - Cyclicity
#   - LifeCycle
#   - LifeExpectancy
#   - Reproduction
#   - Growth
#   - Evolution
#   - FossilHistory
#   - SystematicsOrPhylogenetics
#   - FunctionalAdaptations
#   - Physiology
#   - Cytology
#   - Genetics
#   - Genome
#   - MolecularBiology
#   - Barcode
#   - ConservationStatus
#   - Conservation
#   - Trends
#   - Procedures
#   - Threats
#   - Legislation
#   - Management
#   - Use
#   - RiskStatement
#   - Notes
#   - Taxonomy
#   - TypeInformation
#   - EducationResources
#   - Education
#   - CitizenScience
#   - Key
#   - IdentificationResources
#   - NucleotideSequences
#   licenses: [pipe-delimited, |, for multiple]
#   - cc-by
#   - cc-by-nc
#   - cc-by-sa
#   - cc-by-nc-sa
#   - pd [public domain]
#   - na [not applicable]
#   - all
#   details: True, False
#   common_names: True, False
#   synonyms: True, False
#   references: True, False
#   taxonomy: True, False
#   vetted: 0, 1, 2, 3, 4
#   cache_ttl: [any integer]
#   language:
#   - ms [Malay]
#   - de [German]
#   - en [English]
#   - es [Spanish]
#   - fr [French]
#   - gl [Galician]
#   - it [Italian]
#   - nl [Dutch/Flemish]
#   - nb [Bokmål, Norwegian; Norwegian Bokmål]
#   - oc [Occitan]
#   - pt-BR [Brazilian Portuguese]
#   - sv [Swedish]
#   - tl [Tagalog]
#   - mk [Macedonian]
#   - sr [Serbian]
#   - uk [Ukrainian]
#   - ar [Arabic]
#   - zh-Hans [Simplified Chinese]
#   - zh-Hant [Traditional Chinese]
#   - ko [Korean]
def get_eol_object(taxon, batch=False, images_per_page=1, images_page=1, videos_per_page=1, videos_page=1, sounds_per_page=1, sounds_page=1, maps_per_page=1, maps_page=1, texts_per_page=2, texts_page=1, subjects="overview", licenses="all", details=True, common_names=True, synonyms=True, references=True, taxonomy=True, vetted=0, cache_ttl=None, language="en", result_format="JSON", user=None):
    
    eol_obj_array = []
    
    for tax_obj in taxon.taxon_objects:
        if 'object_type' in tax_obj:
            if tax_obj['object_type'].lower() in ['eol', 'eol page']:
                eol_obj_array.append(tax_obj['object'])
            
    if eol_obj_array:
        return eol_obj_array
            
    ids_completed = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["eol", "eol id", "eol identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
        
                    base_url = "http://eol.org/api/pages/1.0.json?"
                    ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(ident["identifier"]) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language) + "&key=" + str(user.eol_api_key)

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                        eol_obj_array.append(decoded)
                        
                else:
                    
                    base_url = "http://eol.org/api/pages/1.0.json?"
                    ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(ident["identifier"]) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language)

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                        eol_obj_array.append(decoded)
                
            else:
                
                base_url = "http://eol.org/api/pages/1.0.json?"
                ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(ident["identifier"]) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language)

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                    eol_obj_array.append(decoded)
            
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["ncbi", "ncbi taxid", "ncbi taxon", "ncbi taxon id", "ncbi taxon identifier", "ncbi taxonomy", "ncbi taxonomy id", "ncbi taxonomy identifier", "ncbitaxon", "ncbitaxon id", "ncbitaxon identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
        
                    base_url = "http://eol.org/api/pages/1.0.json?"
                    ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(get_eol_id(taxon)) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language) + "&key=" + str(user.eol_api_key)

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                        eol_obj_array.append(decoded)
                        
                else:
                    
                    base_url = "http://eol.org/api/pages/1.0.json?"
                    ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(get_eol_id(taxon)) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language)

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                        eol_obj_array.append(decoded)
                        
            else:
                
                base_url = "http://eol.org/api/pages/1.0.json?"
                ext_url = "batch=" + str(batch).lower() + "&" + "id=" + str(get_eol_id(taxon)) + "&" + "images_per_page=" + str(images_per_page) + "&" + "images_page=" + str(images_page) + "&" + "videos_per_page=" + str(videos_per_page) + "&" + "videos_page=" + str(videos_page) + "&" + "sounds_per_page=" + str(sounds_per_page) + "&" + "sounds_page=" + str(sounds_page) + "&" + "maps_per_page=" + str(maps_per_page) + "&" + "maps_page=" + str(maps_page) + "&" + "texts_per_page=" + str(texts_per_page) + "&" + "texts_page=" + str(texts_page) + "&" + "subjects=" + str(subjects) + "&" + "licences=" + str(licenses) + "&" + "details=" + str(details).lower() + "&" + "common_names=" + str(common_names).lower() + "&" + "synonyms=" + str(synonyms).lower() + "&" + "references=" + str(references).lower() + "&" + "taxonomy=" + str(taxonomy).lower() + "&" + "vetted=" + str(vetted) + "&" + "cache_ttl=" + "&" + "language=" + str(language)

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Page")
                    eol_obj_array.append(decoded)
    
    return eol_obj_array

#   Get EOL Traitbank object.
def get_eol_traitbank_object(taxon):
    eol_obj_array = []
    
    for tax_obj in taxon.taxon_objects:
        if 'object_type' in tax_obj:
            if tax_obj['object_type'].lower() in ['eol traitbank', 'traitbank']:
                eol_obj_array.append(tax_obj['object'])
                
    if eol_obj_array:
        return eol_obj_array
            
    ids_completed = []
    
    base_url = "http://eol.org/api/"
    for eol_id in get_eol_id(taxon):
        if eol_id not in ids_completed:
            ids_completed.append(eol_id)
            ext_url = "traits/" + str(eol_id)
            r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            else:
                decoded = r.json()
                gnomics.objects.taxon.Taxon.add_object(taxon, obj = decoded, object_type = "EOL Traitbank")
                eol_obj_array.append(decoded)

    return eol_obj_array
    
#   Get EOL identifier.
def get_eol_id(taxon, user=None):
    eol_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["eol", "eol id", "eol identifier"] and ident["identifier"] not in eol_array:
            eol_array.append(ident["identifier"])
            
    if eol_array:
        return eol_array
        
    ids_completed = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["itis", "itis taxonomic serial number", "itis tsn", "taxonomic serial number", "tsn"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
            
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=903" + "&key=" + str(user.eol_api_key) + "&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
                else:
                    
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=903&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
            else:
                
                base_url = "http://eol.org/api/"
                ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=903&cache_ttl="

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    if decoded[0]["eol_page_id"] not in eol_array:
                        eol_array.append(decoded[0]["eol_page_id"])
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
        
        elif ident["identifier_type"].lower() in ["index fungorum", "index fungorum id", "index fungorum identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
            
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=596" + "&key=" + str(user.eol_api_key) + "&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
                else:
                    
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=596&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
            else:
                
                base_url = "http://eol.org/api/"
                ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=596&cache_ttl="

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    if decoded[0]["eol_page_id"] not in eol_array:
                        eol_array.append(decoded[0]["eol_page_id"])
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
        
        elif ident["identifier_type"].lower() in ["paleobiology database", "paleobiology database id", "paleobiology database identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
            
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=967" + "&key=" + str(user.eol_api_key) + "&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
                else:
                    
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=967&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
            else:
                
                base_url = "http://eol.org/api/"
                ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=967&cache_ttl="

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    if decoded[0]["eol_page_id"] not in eol_array:
                        eol_array.append(decoded[0]["eol_page_id"])
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
        
        elif ident["identifier_type"].lower() in ["ncbi", "ncbi taxid", "ncbi taxon", "ncbi taxon id", "ncbi taxon identifier", "ncbi taxonomy", "ncbi taxonomy id", "ncbi taxonomy identifier", "ncbitaxon", "ncbitaxon id", "ncbitaxon identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            if user is not None:
                if user.eol_api_key is not None:
            
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=1172" + "&key=" + str(user.eol_api_key) + "&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                        
                else:
                    
                    base_url = "http://eol.org/api/"
                    ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=1172&cache_ttl="

                    r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    else:
                        decoded = r.json()
                        if decoded[0]["eol_page_id"] not in eol_array:
                            eol_array.append(decoded[0]["eol_page_id"])
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
                            
            else:
                
                base_url = "http://eol.org/api/"
                ext_url = "search_by_provider/1.0.json?batch=false&id=" + ident["identifier"] + "&hierarchy_id=1172&cache_ttl="

                r = requests.get(base_url+ext_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                else:
                    decoded = r.json()
                    if decoded[0]["eol_page_id"] not in eol_array:
                        eol_array.append(decoded[0]["eol_page_id"])
                        gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = decoded[0]["eol_page_id"], identifier_type = "EOL ID", language = None, source = "EOL")
        
        elif ident["identifier_type"].lower() in ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            for stuff in gnomics.objects.taxon.Taxon.wikidata(taxon):
                
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "encyclopedia of life id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in eol_array:
                                gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "EOL ID", language = None, source = "Wikidata")
                                eol_array.append(x["mainsnak"]["datavalue"]["value"])
                                
    return eol_array
        
#   Get EOL URL.
def get_eol_url(taxon):
    url_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["eol", "eol id", "eol identifier"]:
            url = "http://eol.org/pages/%s/overview" % ident["identifier"]
            url_array.append(url)
            
    return url

#   UNIT TESTS
def eol_unit_tests(eol_id, tsn, index_fungorum_id, paleobiology_db_id, ncbi_taxonomy_id, wikidata_accession, eol_api_key = None):
    print("Creating user...")
    user = User(eol_api_key = eol_api_key)
    print("User created successfully.\n")
    
    eol_tax = gnomics.objects.taxon.Taxon(identifier = str(eol_id), identifier_type = "EOL ID", source = "EOL")
    print("Getting EOL object from EOL ID (%s):" % eol_id)
    # print(str(get_eol_object(eol_tax)).encode('utf-8'))
    
    print("Getting EOL Traitbank object from EOL ID (%s):" % eol_id)
    with open("traitbank_sample.txt", "w+", encoding="utf-8") as fil:
        fil.write(str(get_eol_traitbank_object(eol_tax)))
    
    print("\nGetting EOL ID from ITIS TSN (%s):" % tsn)
    tsn_tax = gnomics.objects.taxon.Taxon(identifier = str(tsn), identifier_type = "TSN", source = "ITIS")
    print("- %s" % get_eol_id(tsn_tax))
    
    print("\nGetting EOL ID from Index Fungorum identifier (%s):" % index_fungorum_id)
    fungorum_tax = gnomics.objects.taxon.Taxon(identifier = str(index_fungorum_id), identifier_type = "Index Fungorum Identifier", source = "Index Fungorum")
    print("- %s" % get_eol_id(fungorum_tax))
    
    print("\nGetting EOL ID from Paleobiology Database identifier (%s):" % paleobiology_db_id)
    paleo_tax = gnomics.objects.taxon.Taxon(identifier = str(paleobiology_db_id), identifier_type = "Paleobiology Database Identifier", source = "Paleobiology Database")
    print("- %s" % get_eol_id(paleo_tax))
    
    print("\nGetting EOL ID from NCBI Taxonomy identifier (%s):" % ncbi_taxonomy_id)
    ncbi_tax = gnomics.objects.taxon.Taxon(identifier = str(ncbi_taxonomy_id), identifier_type = "NCBI Taxonomy Identifier", source = "NCBI")
    print("- %s" % get_eol_id(ncbi_tax))
    
    wikidata_taxon = gnomics.objects.taxon.Taxon(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
    print("\nGetting EOL ID from Wikidata Accession (%s):" % wikidata_accession)
    print("- %s" % get_eol_id(wikidata_taxon))
        
#   MAIN
if __name__ == "__main__": main()