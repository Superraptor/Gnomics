#
#
#
#
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.anatomical_structure

#   Other imports.
from wikidata.client import Client
import json
import requests

#   MAIN
def main():
    wiki_unit_tests("UBERON:0001424", "Q199507")

#   Get Wikipedia accession (Albanian).
def get_albanian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "sq":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "sq":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="sq", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Arabic).
def get_arabic_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ar":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ar":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ar", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Aramaic).
def get_aramaic_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "arc":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "arc":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="arc", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Aymara).
def get_aymara_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ay":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ay":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ay", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Azerbaijani).
def get_azerbaijani_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "az":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "az":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="az", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Bangla).
def get_bangla_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "bn":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "bn":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="bn", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Bengali).
def get_bengali_wikipedia_accession(anat, user = None):
    return get_bangla_wikipedia_accession(anat, user = None)
                    
#   Get Wikipedia accession (Bashkir).
def get_bashkir_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ba":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ba":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ba", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Basque).
def get_basque_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "eu":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "eu":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="eu", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Breton).
def get_breton_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "br":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "br":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="br", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Bosnian).
def get_bosnian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "bs":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "bs":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="bs", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Bulgarian).
def get_bulgarian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "bg":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "bg":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="bg", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

                    
#   Get Wikipedia accession (Cantonese).
def get_cantonese_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "zh_yue":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "zh_yue":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="zh_yue", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Catalan).
def get_catalan_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ca":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ca":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ca", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Central Kurdish).
def get_central_kurdish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ckb":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ckb":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ckb", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Chinese).
def get_chinese_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "zh":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "zh":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="zh", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Classical Chinese).
def get_classical_chinese_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "zh_classical":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "zh_classical":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="zh_classical", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Croatian).
def get_croatian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "hr":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "hr":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="hr", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Czech).
def get_czech_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "cs":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "cs":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="cs", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Danish).
def get_danish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "da":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "da":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="da", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Divehi).
def get_divehi_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "dv":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "dv":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="dv", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Dutch).
def get_dutch_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "nl":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "nl":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="nl", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (English).
def get_english_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "en":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            for ext_id in gnomics.objects.anatomical_structure.AnatomicalStructure.uberon(anat)["annotation"]["database_cross_reference"]:
                if "http://en.wikipedia.org" in ext_id:
                    new_ext_id = ext_id.split("/wiki/")[1]
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="en", source="Ontology Lookup Service", name=new_ext_id)
                    return new_ext_id

#   Get Wikipedia accession (Simple English).
def get_simple_english_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "simple":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "simple":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="simple", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Esperanto).
def get_esperanto_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ep":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ep":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ep", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Finnish).
def get_finnish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "fi":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "fi":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="fi", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (French).
def get_french_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "fr":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "fr":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="fr", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Galician).
def get_galician_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "gl":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "gl":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="gl", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Georgian).
def get_georgian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ka":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ka":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ka", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                
#   Get Wikipedia accession (German).
def get_german_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "de":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "de":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="de", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Greek).
def get_greek_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "el":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "el":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="el", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Hebrew).
def get_hebrew_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "he":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "he":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="he", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Hungarian).
def get_hungarian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "hu":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "hu":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="hu", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Ido).
def get_ido_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "io":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "io":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="io", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Indonesian).
def get_indonesian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "id":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "id":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="id", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Irish).
def get_irish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ga":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ga":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ga", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Italian).
def get_italian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "it":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "it":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="it", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Japanese).
def get_japanese_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ja":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ja":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ja", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Kazakh).
def get_kazakh_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "kk":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "kk":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="kk", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Korean).
def get_korean_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ko":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ko":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ko", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Latin).
def get_latin_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "la":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "la":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="la", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Latvian).
def get_latvian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "lv":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "lv":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="lv", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Lithuanian).
def get_lithuanian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "lt":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "lt":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="lt", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Macedonian).
def get_macedonian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "mk":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "mk":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="mk", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Newari).
def get_newari_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "new":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "new":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="new", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Norwegian).
def get_norwegian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "no":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "no":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="no", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Persian).
def get_persian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "fa":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "fa":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="fa", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Polish).
def get_polish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "pl":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "pl":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="pl", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Portuguese).
def get_portuguese_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "pt":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "pt":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="pt", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Romanian).
def get_romanian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ro":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ro":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ro", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Russian).
def get_russian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ru":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ru":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ru", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Scots).
def get_scots_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "sco":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "sco":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="sco", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Serbo-Croatian).
def get_serbo_croatian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "sh":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "sh":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="sh", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Slovenian).
def get_slovenian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "sl":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "sl":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="sl", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Spanish).
def get_spanish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "es":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "es":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="es", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Swedish).
def get_swedish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "sv":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "sv":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="sv", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Tamil).
def get_tamil_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "ta":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "ta":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="ta", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Telugu).
def get_telugu_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "te":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "te":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="te", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Thai).
def get_thai_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "th":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "th":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="th", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Turkish).
def get_turkish_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "tr":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "tr":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="tr", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Ukrainian).
def get_ukrainian_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "uk":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "uk":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="uk", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id

#   Get Wikipedia accession (Walloon).
def get_walloon_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "wa":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "wa":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="wa", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikipedia accession (Western Mari).
def get_western_mari_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "mrj":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "mrj":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="mrj", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id 
                    
#   Get Wikipedia accession (Xhosa).
def get_xhosa_wikipedia_accession(anat, user = None):
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"] == "xh":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            get_english_wikipedia_accession(anat)
            get_wikidata_accession(anat)
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for lang_id, lang_dict in stuff["labels"].items():
                    if lang_id == "xh":
                        new_ext_id = lang_dict["value"]
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=new_ext_id, identifier_type="Wikipedia Accession", language="xh", source="Ontology Lookup Service", name=new_ext_id)
                        return new_ext_id
                    
#   Get Wikidata accession.
def get_wikidata_accession(anat):
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikidata accession" or ident["identifier_type"].lower() == "wikidata":
            return ident["identifier"]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia":
            if ident["language"].lower() == "en":
                base = "https://en.wikipedia.org/w/api.php"
                ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                for key, value in decoded["query"]["pages"].items():
                    wikidata_id = value["pageprops"]["wikibase_item"]
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                    return wikidata_id
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier" or ident["identifier_type"].lower() == "uberon":
            get_english_wikipedia_accession(anat)
            return get_wikidata_accession(anat)
        
#   Get WikiSkripta ID.
def get_wikiskripta_id(anat):
    wikiskripta_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikiskripta id" or ident["identifier_type"].lower() == "wikiskripta identifier":
            wikiskripta_array.append(ident["identifier"])
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
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
                    if en_prop_name.lower() == "wikiskripta id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "WikiSkripta ID", language = None, source = "Wikidata")
                            wikiskripta_array.append(x["mainsnak"]["datavalue"]["value"])
    return wikiskripta_array
            
#   Get Wikidata object.
def get_wikidata_object(anat):
    wikidata_obj_array = []
    for anat_obj in anat.anatomical_structure_objects:
        if 'object_type' in anat_obj:
            if anat_obj['object_type'].lower() == 'wikidata object' or anat_obj['object_type'].lower() == 'wikidata':
                wikidata_obj_array.append(anat_obj['object'])
    if wikidata_obj_array:
        return wikidata_obj_array
    for wikidata_id in [get_wikidata_accession(anat)]:
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
    return wikidata_obj_array
    
#   UNIT TESTS
def wiki_unit_tests(uberon_id, wikidata_accession):
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = str(uberon_id), identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    print("Getting English Wikipedia accession from UBERON ID (%s):" % uberon_id)
    print("- " + get_english_wikipedia_accession(uberon_anat))
    print("\nGetting German Wikipedia accession from UBERON ID (%s):" % uberon_id)
    print("- " + get_german_wikipedia_accession(uberon_anat))
    print("\nGetting Wikidata accession from UBERON ID (%s):" % uberon_id)
    print("- " + get_wikidata_accession(uberon_anat))
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, source = "Wikidata")
    print("\nGetting WikiSkripta ID from Wikidata Accession (%s):" % wikidata_accession)
    for wiki in get_wikiskripta_id(wikidata_anat):
        print("- %s" % wiki)

#   MAIN
if __name__ == "__main__": main()