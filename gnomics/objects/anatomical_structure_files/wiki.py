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
#   Get Wikipedia information.
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
import gnomics.objects.pathway
import gnomics.objects.anatomical_structure
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
import json
import requests
import timeit

#   MAIN
def main():
    wiki_unit_tests("UBERON:0001424", "Q199507")

#   Get Wikipedia accession (Albanian).
def get_albanian_wikipedia_accession(anat, user=None):      
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "sq":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for wikidata_object in get_wikidata_object(anat):
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "sq" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="sq", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Arabic).
def get_arabic_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ar":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ar" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ar", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Aramaic).
def get_aramaic_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "arc":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "arc" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="arc", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Aymara).
def get_aymara_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ay":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ay" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ay", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Azerbaijani).
def get_azerbaijani_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "az":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "az" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="az", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Bangla).
def get_bangla_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "bn":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "bn" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="bn", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Bengali).
def get_bengali_wikipedia_accession(anat, user=None):
    return get_bangla_wikipedia_accession(anat, user=user)
                    
#   Get Wikipedia accession (Bashkir).
def get_bashkir_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ba":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ba" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ba", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Basque).
def get_basque_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "eu":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "eu" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="eu", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Breton).
def get_breton_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "br":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "br" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="br", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Bosnian).
def get_bosnian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "bs":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "bs" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="bs", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Bulgarian).
def get_bulgarian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "bg":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "bg" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="bg", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Cantonese).
def get_cantonese_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "zh_yue":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "zh_yue" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="zh_yue", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Catalan).
def get_catalan_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ca":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ca" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ca", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Central Kurdish).
def get_central_kurdish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ckb":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ckb" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ckb", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Chinese).
def get_chinese_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "zh":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "zh" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="zh", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Classical Chinese).
def get_classical_chinese_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "zh_classical":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "zh_classical" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="zh_classical", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Croatian).
def get_croatian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "hr":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "hr" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="hr", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Czech).
def get_czech_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "cs":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "cs" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="cs", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Danish).
def get_danish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "da":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "da" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="da", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Divehi).
def get_divehi_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "dv":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "dv" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="dv", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Dutch).
def get_dutch_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "nl":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "nl" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="nl", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (English).
def get_english_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "en":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.split(":")[1]
            elif "_" in proc_id:
                proc_id = proc_id.split("_")[1]
            
            sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
            sparql_query = """
            SELECT ?item ?itemLabel 
            WHERE 
            {
              ?item wdt:P1554 "%s".
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }""" % (proc_id)
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)

            results = sparql.query().convert()

            for result in results["results"]["bindings"]:
                if result["itemLabel"]["value"] not in wiki_array:
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                    wiki_array.append(result["itemLabel"]["value"])

    return wiki_array

#   Get Wikipedia accession (Simple English).
def get_simple_english_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "simple":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "simple" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="simple", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Esperanto).
def get_esperanto_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ep":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ep" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ep", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Finnish).
def get_finnish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "fi":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "fi" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="fi", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (French).
def get_french_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "fr":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "fr" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="fr", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Galician).
def get_galician_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "gl":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "gl" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="gl", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Georgian).
def get_georgian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ka":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ka" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ka", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                
#   Get Wikipedia accession (German).
def get_german_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "de":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "de" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="de", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Greek).
def get_greek_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "el":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "el" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="el", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Hebrew).
def get_hebrew_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "he":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "he" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="he", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Hungarian).
def get_hungarian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "hu":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "hu" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="hu", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Ido).
def get_ido_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "io":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "io" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="io", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Indonesian).
def get_indonesian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "id":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "id" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="id", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Irish).
def get_irish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ga":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ga" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ga", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Italian).
def get_italian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "it":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "it" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="it", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Japanese).
def get_japanese_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ja":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ja" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ja", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Kazakh).
def get_kazakh_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "kk":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "kk" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="kk", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Korean).
def get_korean_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ko":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ko" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ko", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Latin).
def get_latin_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "la":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "la" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="la", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Latvian).
def get_latvian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "lv":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "lv" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="lv", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Lithuanian).
def get_lithuanian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "lt":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "lt" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="lt", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Macedonian).
def get_macedonian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "mk":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "mk" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="mk", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Newari).
def get_newari_wikipedia_accession(anat, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "new":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "new" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="new", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Norwegian).
def get_norwegian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "no":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "no" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="no", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Persian).
def get_persian_wikipedia_accession(anat, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "fa":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "fa" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="fa", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Polish).
def get_polish_wikipedia_accession(anat, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "pl":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "pl" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="pl", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Portuguese).
def get_portuguese_wikipedia_accession(anat, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "pt":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "pt" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="pt", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Romanian).
def get_romanian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ro":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ro" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ro", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Russian).
def get_russian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ru":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ru" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ru", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Scots).
def get_scots_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "sco":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "sco" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="sco", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Serbo-Croatian).
def get_serbo_croatian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "sh":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "sh" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="sh", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Slovenian).
def get_slovenian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "sl":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "sl" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="sl", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Spanish).
def get_spanish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "es":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "es" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="es", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Swedish).
def get_swedish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "sv":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "sv" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="sv", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Tamil).
def get_tamil_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "ta":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "ta" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="ta", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Telugu).
def get_telugu_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "te":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "te" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="te", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Thai).
def get_thai_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "th":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "th" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="th", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Turkish).
def get_turkish_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "tr":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "tr" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="tr", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Ukrainian).
def get_ukrainian_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "uk":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "uk" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="uk", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array

#   Get Wikipedia accession (Walloon).
def get_walloon_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "wa":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "wa" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="wa", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikipedia accession (Western Mari).
def get_western_mari_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "mrj":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "mrj" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="mrj", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array 
                    
#   Get Wikipedia accession (Xhosa).
def get_xhosa_wikipedia_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "xh":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                                     
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            
            for wikidata_object in get_wikidata_object(anat):
                
                for lang_id, lang_dict in wikidata_object["labels"].items():
                    if lang_id == "xh" and lang_dict["value"] not in wiki_array:
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=lang_dict["value"], identifier_type="Wikipedia Accession", language="xh", source="Wikidata", name=lang_dict["value"])
                
                        wiki_array.append(lang_dict["value"])

    return wiki_array
                    
#   Get Wikidata accession.
def get_wikidata_accession(anat, user=None):
    
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in wiki_array:
            wiki_array.append(iden["identifier"])
        
    if wiki_array:
        return wiki_array
    
    ids_completed = []
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "en" and iden["identifier"] not in ids_completed:
            
            ids_completed.append(iden["identifier"])
            
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + iden["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("A connection error occurred.")
            else:
                decoded = json.loads(r.text)
                for key, value in decoded["query"]["pages"].items():
                    if "pageprops" in value:
                        if value["pageprops"]["wikibase_item"] not in wiki_array:

                            wiki_array.append(value["pageprops"]["wikibase_item"])
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = value["pageprops"]["wikibase_item"], identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                
                if not wiki_array:
                    return wiki_array
                
    if wiki_array:
        return wiki_array
                        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            if get_english_wikipedia_accession(anat):
                return get_wikidata_accession(anat)
        
    return wiki_array
        
#   Get WikiSkripta ID.
def get_wikiskripta_id(anat, user=None):
    
    wikiskripta_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikiskripta", "wikiskripta id", "wikiskripta identifier"]):
        if iden["identifier"] not in wikiskripta_array:
            wikiskripta_array.append(iden["identifier"])
        
    if wikiskripta_array:
        return wikiskripta_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            
            ids_completed.append(iden["identifier"])
            
            for wikidata_object in get_wikidata_object(anat):
                for prop_id, prop_dict in wikidata_object["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"

                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        print("A connection error occurred.")
                    else:

                        decoded = json.loads(r.text)
                        en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                        if en_prop_name.lower() == "wikiskripta id":
                            for x in prop_dict:
                                if x["mainsnak"]["datavalue"]["value"] not in wikiskripta_array:
                                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "WikiSkripta ID", language = None, source = "Wikidata")
                                    wikiskripta_array.append(x["mainsnak"]["datavalue"]["value"])
    
    return wikiskripta_array
            
#   Get Wikidata object.
def get_wikidata_object(anat, user=None):
    wikidata_obj_array = []
    for anat_obj in anat.anatomical_structure_objects:
        if 'object_type' in anat_obj:
            if anat_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(anat_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in get_wikidata_accession(anat):
        
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj = entity.attributes, object_type = "Wikidata Object")
        
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array
    
#   UNIT TESTS
def wiki_unit_tests(uberon_id, wikidata_accession):
    
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = str(uberon_id), identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    
    print("\nGetting English Wikipedia accession from UBERON ID (%s):" % uberon_id)
    start = timeit.timeit()
    wiki_array = get_english_wikipedia_accession(uberon_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for wiki in wiki_array:
        print("\t- " + str(wiki))
    
    print("\nGetting German Wikipedia accession from UBERON ID (%s):" % uberon_id)
    start = timeit.timeit()
    wiki_array = get_german_wikipedia_accession(uberon_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for wiki in wiki_array:
        print("\t- " + str(wiki))
    
    print("\nGetting Wikidata accession from UBERON ID (%s):" % uberon_id)
    start = timeit.timeit()
    wiki_array = get_wikidata_accession(uberon_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for wiki in wiki_array:
        print("\t- " + str(wiki))
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    print("\nGetting WikiSkripta ID from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    wiki_array = get_wikiskripta_id(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for wiki in wiki_array:
        print("\t- " + str(wiki))

#   MAIN
if __name__ == "__main__": main()