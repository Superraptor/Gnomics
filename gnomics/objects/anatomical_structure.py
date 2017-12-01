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
#   Create instance of an anatomical structure.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

#   Import modules.
from gnomics.objects.user import User
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.drug
import gnomics.objects.pathway
import gnomics.objects.phenotype

#   Other imports.
import io
import json
import pubchempy as pubchem
import re
import requests
import signal
import wikipedia

#   Import sub-methods.
from gnomics.objects.anatomical_structure_files.aeo import get_aeo_id
from gnomics.objects.anatomical_structure_files.aod import get_aod
from gnomics.objects.anatomical_structure_files.bncf import get_bncf_thesaurus
from gnomics.objects.anatomical_structure_files.britannica import get_encyclopedia_britannica_online_id
from gnomics.objects.anatomical_structure_files.caro import get_caro_id 
from gnomics.objects.anatomical_structure_files.ccpss import get_ccpss
from gnomics.objects.anatomical_structure_files.ceph import get_ceph_id
from gnomics.objects.anatomical_structure_files.ehdaa2 import get_ehdaa2_id
from gnomics.objects.anatomical_structure_files.emap import get_emap_id, get_emapa_id
from gnomics.objects.anatomical_structure_files.fbbt import get_fbbt_id
from gnomics.objects.anatomical_structure_files.fma import get_fma_id
from gnomics.objects.anatomical_structure_files.freebase import get_freebase_id
from gnomics.objects.anatomical_structure_files.hao import get_hao_id
from gnomics.objects.anatomical_structure_files.jstor import get_jstor_topic_id
from gnomics.objects.anatomical_structure_files.loc import get_loc_sh
from gnomics.objects.anatomical_structure_files.ma import get_ma_id
from gnomics.objects.anatomical_structure_files.mfmo import get_mfmo_id
from gnomics.objects.anatomical_structure_files.nci import get_nci_thesaurus_id
from gnomics.objects.anatomical_structure_files.neu import get_neu_id
from gnomics.objects.anatomical_structure_files.plana import get_plana_id
from gnomics.objects.anatomical_structure_files.psy import get_psy
from gnomics.objects.anatomical_structure_files.read_codes import get_read_codes
from gnomics.objects.anatomical_structure_files.search import search
from gnomics.objects.anatomical_structure_files.ta import get_ta98_id, get_ta98_latin_term
from gnomics.objects.anatomical_structure_files.tads import get_tads_id
from gnomics.objects.anatomical_structure_files.tgma import get_tgma_id
from gnomics.objects.anatomical_structure_files.uberon import get_uberon_obj, get_uberon_id
from gnomics.objects.anatomical_structure_files.uwda import get_uwda_id
from gnomics.objects.anatomical_structure_files.wbbt import get_wbbt_id
from gnomics.objects.anatomical_structure_files.wiki import get_english_wikipedia_accession, get_german_wikipedia_accession, get_wikidata_accession, get_wikidata_object, get_albanian_wikipedia_accession, get_arabic_wikipedia_accession, get_aramaic_wikipedia_accession, get_aymara_wikipedia_accession, get_azerbaijani_wikipedia_accession, get_bangla_wikipedia_accession, get_bashkir_wikipedia_accession, get_basque_wikipedia_accession, get_breton_wikipedia_accession, get_bosnian_wikipedia_accession, get_bulgarian_wikipedia_accession, get_cantonese_wikipedia_accession, get_catalan_wikipedia_accession, get_central_kurdish_wikipedia_accession, get_chinese_wikipedia_accession, get_classical_chinese_wikipedia_accession, get_croatian_wikipedia_accession, get_czech_wikipedia_accession, get_danish_wikipedia_accession, get_divehi_wikipedia_accession, get_dutch_wikipedia_accession, get_simple_english_wikipedia_accession, get_esperanto_wikipedia_accession, get_finnish_wikipedia_accession, get_french_wikipedia_accession, get_galician_wikipedia_accession, get_georgian_wikipedia_accession, get_german_wikipedia_accession, get_greek_wikipedia_accession, get_hebrew_wikipedia_accession, get_hungarian_wikipedia_accession, get_ido_wikipedia_accession, get_indonesian_wikipedia_accession, get_irish_wikipedia_accession, get_italian_wikipedia_accession, get_japanese_wikipedia_accession, get_kazakh_wikipedia_accession, get_korean_wikipedia_accession, get_latin_wikipedia_accession, get_latvian_wikipedia_accession, get_lithuanian_wikipedia_accession, get_macedonian_wikipedia_accession, get_newari_wikipedia_accession, get_norwegian_wikipedia_accession, get_persian_wikipedia_accession, get_polish_wikipedia_accession, get_portuguese_wikipedia_accession, get_romanian_wikipedia_accession, get_russian_wikipedia_accession, get_scots_wikipedia_accession, get_serbo_croatian_wikipedia_accession, get_slovenian_wikipedia_accession, get_spanish_wikipedia_accession, get_swedish_wikipedia_accession, get_tamil_wikipedia_accession, get_telugu_wikipedia_accession, get_thai_wikipedia_accession, get_turkish_wikipedia_accession, get_ukrainian_wikipedia_accession, get_walloon_wikipedia_accession, get_western_mari_wikipedia_accession, get_xhosa_wikipedia_accession
from gnomics.objects.anatomical_structure_files.xao import get_xao_id
from gnomics.objects.anatomical_structure_files.zfa import get_zfa_id

#   Import further methods.
from gnomics.objects.interaction_objects.anatomical_structure_tissue import get_tissues

#   MAIN
def main():
    anatomical_structure_unit_tests("UBERON:0002386")

#   ANATOMICAL STRUCTURE CLASS
class AnatomicalStructure:
    """
        Anatomical structure class:
        
        According to Anatomy Ontologies for Bioinformatics:
        Principles and Practice, an anatomical structure
        is a "material anatomical entity that has inherent 3D
        shape and is generated by coordinated expression of the
        organism's own genome."
    """
    
    """
        Anatomical structure attributes:
        
        Identifier      = A particular way to identify the
                          anatomical structure in question. Usually a database unique identifier, but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The taxon in which the anatomical
                          structure is typically found.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the anatomical structure.
    def __init__(self, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'taxon': taxon,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of anatomical structure objects.
        self.anatomical_structure_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an anatomical structure.
    def add_identifier(anatomical_structure, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        anatomical_structure.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'taxon': taxon,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to an anatomical structure.
    def add_object(anatomical_structure, obj = None, object_type = None):
        anatomical_structure.anatomical_structure_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Anatomical structure objects:
        
        UBERON Object
        Wikidata Object
        
    """
    
    def uberon(anatomical_structure):
        return get_uberon_obj(anatomical_structure)
    
    def wikidata(anatomical_structure):
        return get_wikidata_object(anatomical_structure)
        
    """
        Anatomical structure identifiers:
        
        AEO (Anatomical Entity Ontology) ID
        AOD
        BNCF Thesaurus ID
        CARO ID
        CCPSS
        CEPH ID
        EHDAA2 ID
        EMAP ID
        EMAPA ID
        Encyclopedia Britannica Online ID
        FBbt ID
        FMA ID
        Freebase ID
        HAO ID
        JSTOR Topic ID
        Library of Congress Subject Heading (LCSH)
        MA ID
        MFMO ID
        NCI Thesaurus ID
        NEU ID
        PLANA ID
        Read Codes
        TADS ID
        TGMA ID
        Thesaurus of Psychological Index Terms
        Terminologia Anatomica '98 (TA98) ID
        Terminologia Anatomica '98 (TA98) Latin Term
        UBERON ID
        UWDA ID
        WBBT ID
        Wikidata Accession
        Wikipedia Accession (Albanian)
        Wikipedia Accession (Arabic)
        Wikipedia Accession (Aramaic)
        Wikipedia Accession (Aymara)
        Wikipedia Accession (Azerbaijani)
        Wikipedia Accession (Bangla/Bengali)
        Wikipedia Accession (Bashkir)
        Wikipedia Accession (Basque)
        Wikipedia Accession (Breton)
        Wikipedia Accession (Bosnian)
        Wikipedia Accession (Bulgarian)
        Wikipedia Accession (Cantonese)
        Wikipedia Accession (Catalan)
        Wikipedia Accession (Chinese)
        Wikipedia Accession (Classical Chinese)
        Wikipedia Accession (Croatian)
        Wikipedia Accession (Czech)
        Wikipedia Accession (Danish)
        Wikipedia Accession (Divehi)
        Wikipedia Accession (Dutch)
        Wikipedia Accession (English)
        Wikipedia Accession (Simple English)
        Wikipedia Accession (Esperanto)
        Wikipedia Accession (Finnish)
        Wikipedia Accession (French)
        Wikipedia Accession (Galician)
        Wikipedia Accession (Georgian)
        Wikipedia Accession (German)
        Wikipedia Accession (Greek)
        Wikipedia Accession (Hebrew)
        Wikipedia Accession (Hungarian)
        Wikipedia Accession (Ido)
        Wikipedia Accession (Indonesian)
        Wikipedia Accession (Irish)
        Wikipedia Accession (Italian)
        Wikipedia Accession (Japanese)
        Wikipedia Accession (Kazakh)
        Wikipedia Accession (Korean)
        Wikipedia Accession (Latin)
        Wikipedia Accession (Latvian)
        Wikipedia Accession (Lithuanian)
        Wikipedia Accession (Macedonian)
        Wikipedia Accession (Newari)
        Wikipedia Accession (Norwegian)
        Wikipedia Accession (Persian)
        Wikipedia Accession (Polish)
        Wikipedia Accession (Portuguese)
        Wikipedia Accession (Romanian)
        Wikipedia Accession (Russian)
        Wikipedia Accession (Scots)
        Wikipedia Accession (Serbo-Croatian)
        Wikipedia Accession (Slovenian)
        Wikipedia Accession (Spanish)
        Wikipedia Accession (Swedish)
        Wikipedia Accession (Tamil)
        Wikipedia Accession (Telugu)
        Wikipedia Accession (Thai)
        Wikipedia Accession (Turkish)
        Wikipedia Accession (Ukrainian)
        Wikipedia Accession (Walloon)
        Wikipedia Accession (Xhosa)
        XAO ID
        ZFA ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(anatomical_structure, user = None):
        AnatomicalStructure.aeo_id(anatomical_structure, user = user)
        AnatomicalStructure.aod(anatomical_structure, user = user)
        AnatomicalStructure.bncf_thesaurus_id(anatomical_structure, user = user)
        AnatomicalStructure.caro_id(anatomical_structure)
        AnatomicalStructure.ceph_id(anatomical_structure)
        AnatomicalStructure.ccpss(anatomical_structure, user = user)
        AnatomicalStructure.ehdaa2_id(anatomical_structure)
        AnatomicalStructure.emap_id(anatomical_structure)
        AnatomicalStructure.emapa_id(anatomical_structure)
        AnatomicalStructure.encyclopedia_britannica_online_id(anatomical_structure)
        AnatomicalStructure.fbbt_id(anatomical_structure)
        AnatomicalStructure.fma_id(anatomical_structure)
        AnatomicalStructure.freebase_id(anatomical_structure)
        AnatomicalStructure.hao_id(anatomical_structure)
        AnatomicalStructure.jstor_topic_id(anatomical_structure)
        AnatomicalStructure.loc_sh(anatomical_structure, user = user)
        AnatomicalStructure.ma_id(anatomical_structure)
        AnatomicalStructure.mfmo_id(anatomical_structure)
        AnatomicalStructure.nci_thesaurus_id(anatomical_structure, user = user)
        AnatomicalStructure.neu_id(anatomical_structure)
        AnatomicalStructure.plana_id(anatomical_structure)
        AnatomicalStructure.psy(anatomical_structure, user = user)
        AnatomicalStructure.read_codes(anatomical_structure, user = user)
        AnatomicalStructure.ta98_id(anatomical_structure, user = user)
        AnatomicalStructure.ta98_latin_term(anatomical_structure, user = user)
        AnatomicalStructure.tads_id(anatomical_structure)
        AnatomicalStructure.tgma_id(anatomical_structure)
        AnatomicalStructure.uberon_id(anatomical_structure)
        AnatomicalStructure.uwda_id(anatomical_structure, user = user)
        AnatomicalStructure.wbbt_id(anatomical_structure)
        AnatomicalStructure.wikidata_accession(anatomical_structure)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="albanian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="arabic")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="aramaic")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="aymara")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="azerbaijani")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bangla")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bashkir")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="basque")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="breton")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bosnian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bulgarian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="cantonese")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="catalan")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="central kurdish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="chinese")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="classical chinese")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="croatian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="czech")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="danish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="divehi")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="dutch")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="english")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="simple english")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="esperanto")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="finnish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="french")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="galician")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="georgian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="german")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="greek")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="hebrew")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="hungarian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="ido")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="indonesian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="irish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="italian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="japanese")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="kazakh")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="korean")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="latin")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="latvian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="lithuanian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="macedonian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="newari")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="norwegian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="persian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="polish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="portuguese")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="romanian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="russian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="scots")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="serbo-croatian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="slovenian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="spanish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="swedish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="tamil")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="telugu")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="thai")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="turkish")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="ukrainian")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="walloon")
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="xhosa")
        AnatomicalStructure.xao_id(anatomical_structure)
        AnatomicalStructure.zfa_id(anatomical_structure)
        return anatomical_structure.identifiers
    
    def aeo_id(anatomical_structure, user = None):
        return get_aeo_id(anatomical_structure, user = user)
        
    def aod(anatomical_structure, user = None):
        return get_aod(anatomical_structure, user = user)
        
    def bncf_thesaurus_id(anatomical_structure, user = None):
        return get_bncf_thesaurus(anatomical_structure)
        
    def caro_id(anatomical_structure):
        return get_caro_id(anatomical_structure)
        
    def ceph_id(anatomical_structure):
        return get_ceph_id(anatomical_structure)
    
    def ccpss(anatomical_structure, user = None):
        return get_ccpss(anatomical_structure, user = user)
        
    def ehdaa2_id(anatomical_structure):
        return get_ehdaa2_id(anatomical_structure)
        
    def emap_id(anatomical_structure):
        return get_emap_id(anatomical_structure)
        
    def emapa_id(anatomical_structure):
        return get_emapa_id(anatomical_structure)
        
    def encyclopedia_britannica_online_id(anatomical_structure):
        return get_encyclopedia_britannica_online_id(anatomical_structure)
        
    def fbbt_id(anatomical_structure):
        return get_fbbt_id(anatomical_structure)
        
    def fma_id(anatomical_structure):
        return get_fma_id(anatomical_structure)
        
    def freebase_id(anatomical_structure):
        return get_freebase_id(anatomical_structure)
        
    def hao_id(anatomical_structure):
        return get_hao_id(anatomical_structure)
        
    def jstor_topic_id(anatomical_structure):
        return get_jstor_topic_id(anatomical_structure)
    
    def loc_sh(anatomical_structure, user = None):
        return get_loc_sh(anatomical_structure, user = user)
        
    def ma_id(anatomical_structure):
        return get_ma_id(anatomical_structure)
        
    def mfmo_id(anatomical_structure):
        return get_mfmo_id(anatomical_structure)
        
    def nci_thesaurus_id(anatomical_structure, user = None):
        return get_nci_thesaurus_id(anatomical_structure, user = user)
        
    def neu_id(anatomical_structure):
        return get_neu_id(anatomical_structure)
        
    def plana_id(anatomical_structure):
        return get_plana_id(anatomical_structure)
    
    # Get Thesaurus of Psychological Index Terms (PSY).
    def psy(anatomical_structure, user = None):
        return get_psy(anatomical_structure, user = user)
    
    # Get Read Codes.
    def read_codes(anatomical_structure, user = None):
        return get_read_codes(anatomical_structure, user = user)
    
    # Get Terminologia Anatomica 98 (TA98) ID.
    def ta98_id(anatomical_structure, user = None):
        return get_ta98_id(anatomical_structure, user = user)
    
    # Get Terminologia Anatomica 98 (TA98) Latin Term.
    def ta98_latin_term(anatomical_structure, user = None):
        return get_ta98_latin_term(anatomical_structure, user = user)
        
    def tads_id(anatomical_structure):
        return get_tads_id(anatomical_structure)
        
    def tgma_id(anatomical_structure):
        return get_tgma_id(anatomical_structure)
    
    def uberon_id(anatomical_structure):
        return get_uberon_id(anatomical_structure)
        
    def uwda_id(anatomical_structure, user = None):
        return get_uwda_id(anatomical_structure, user = user)
        
    def wbbt_id(anatomical_structure):
        return get_wbbt_id(anatomical_structure)
    
    def wikidata_accession(anatomical_structure):
        return get_wikidata_accession(anatomical_structure)
        
    def wikipedia_accession(anatomical_structure, language = "en"):
        if language == "sqi" or language == "sq" or language.lower() == "albanian":
            return get_albanian_wikipedia_accession(anatomical_structure)
        elif language == "ara" or language == "ar" or language.lower() == "arabic":
            return get_arabic_wikipedia_accession(anatomical_structure)
        elif language == "arc" or language.lower() == "aramaic":
            return get_aramaic_wikipedia_accession(anatomical_structure)
        elif language == "aym" or language == "ay" or language.lower() == "aymara":
            return get_aymara_wikipedia_accession(anatomical_structure)
        elif language == "aze" or language == "az" or language.lower() == "azerbaijani":
            return get_azerbaijani_wikipedia_accession(anatomical_structure)
        elif language == "ben" or language == "bn" or language.lower() == "bangla" or language.lower() == "bengali":
            return get_bangla_wikipedia_accession(anatomical_structure)
        elif language == "bak" or language == "ba" or language.lower() == "bashkir":
            return get_bashkir_wikipedia_accession(anatomical_structure)
        elif language == "baq" or language == "eu" or language.lower() == "basque":
            return get_basque_wikipedia_accession(anatomical_structure)
        elif language == "bre" or language == "br" or language.lower() == "breton":
            return get_breton_wikipedia_accession(anatomical_structure)
        elif language == "bos" or language == "bs" or language.lower() == "bosnian":
            return get_bosnian_wikipedia_accession(anatomical_structure)
        elif language == "bul" or language == "bg" or language.lower() == "bulgarian":
            return get_bulgarian_wikipedia_accession(anatomical_structure)
        elif language == "zh_yue" or language.lower() == "cantonese":
            return get_cantonese_wikipedia_accession(anatomical_structure)
        elif language == "cat" or language == "ca" or language.lower() == "catalan":
            return get_catalan_wikipedia_accession(anatomical_structure)
        elif language == "ckb" or language.lower() == "central kurdish":
            return get_central_kurdish_wikipedia_accession(anatomical_structure)
        elif language == "chi" or language == "zh" or language.lower() == "chinese":
            return get_chinese_wikipedia_accession(anatomical_structure)
        elif language == "zh_classical" or language.lower() == "classical chinese":
            return get_classical_chinese_wikipedia_accession(anatomical_structure)
        elif language == "hry" or language == "hr" or language.lower() == "croatian":
            return get_croatian_wikipedia_accession(anatomical_structure)
        elif language == "cze" or language == "cs" or language.lower() == "czech":
            return get_czech_wikipedia_accession(anatomical_structure)
        elif language == "dan" or language == "da" or language.lower() == "danish":
            return get_danish_wikipedia_accession(anatomical_structure)
        elif language == "div" or language == "dv" or language.lower() == "divehi":
            return get_divehi_wikipedia_accession(anatomical_structure)
        elif language == "dut" or language == "nl" or language.lower() == "dutch":
            return get_dutch_wikipedia_accession(anatomical_structure)
        elif language == "eng" or language == "en" or language.lower() == "english":
            return get_english_wikipedia_accession(anatomical_structure)
        elif language == "simple" or language.lower() == "simple english":
            return get_simple_english_wikipedia_accession(anatomical_structure)
        elif language == "epo" or language == "eo" or language == "ep" or language.lower() == "esperanto":
            return get_esperanto_wikipedia_accession(anatomical_structure)
        elif language == "fin" or language == "fi" or language.lower() == "finnish":
            return get_finnish_wikipedia_accession(anatomical_structure)
        elif language == "fre" or language == "fr" or language.lower() == "french":
            return get_french_wikipedia_accession(anatomical_structure)
        elif language == "glg" or language == "gl" or language.lower() == "galician":
            return get_galician_wikipedia_accession(anatomical_structure)
        elif language == "geo" or language == "ka" or language.lower() == "georgian":
            return get_georgian_wikipedia_accession(anatomical_structure)
        elif language == "ger" or language == "de" or language.lower() == "german":
            return get_german_wikipedia_accession(anatomical_structure)
        elif language == "gre" or language == "el" or language.lower() == "greek":
            return get_greek_wikipedia_accession(anatomical_structure)
        elif language == "heb" or language == "he" or language.lower() == "hebrew":
            return get_hebrew_wikipedia_accession(anatomical_structure)
        elif language == "hun" or language == "hu" or language.lower() == "hungarian":
            return get_hungarian_wikipedia_accession(anatomical_structure)
        elif language == "ido" or language == "io" or language.lower() == "ido":
            return get_ido_wikipedia_accession(anatomical_structure)
        elif language == "ind" or language == "id" or language.lower() == "indonesian":
            return get_indonesian_wikipedia_accession(anatomical_structure)
        elif language == "gle" or language == "ga" or language.lower() == "irish":
            return get_irish_wikipedia_accession(anatomical_structure)
        elif language == "ita" or language == "it" or language.lower() == "italian":
            return get_italian_wikipedia_accession(anatomical_structure)
        elif language == "jpn" or language == "ja" or language.lower() == "japanese":
            return get_japanese_wikipedia_accession(anatomical_structure)
        elif language == "kaz" or language == "kk" or language.lower() == "kazakh":
            return get_kazakh_wikipedia_accession(anatomical_structure)
        elif language == "kor" or language == "ko" or language.lower() == "korean":
            return get_korean_wikipedia_accession(anatomical_structure)
        elif language == "lat" or language == "la" or language.lower() == "latin":
            return get_latin_wikipedia_accession(anatomical_structure)
        elif language == "lav" or language == "lv" or language.lower() == "latvian":
            return get_latvian_wikipedia_accession(anatomical_structure)
        elif language == "lit" or language == "lt" or language.lower() == "lithuanian":
            return get_lithuanian_wikipedia_accession(anatomical_structure)
        elif language == "mac" or language == "mk" or language.lower() == "macedonian":
            return get_macedonian_wikipedia_accession(anatomical_structure)
        elif language == "new" or language.lower() == "newari":
            return get_newari_wikipedia_accession(anatomical_structure)
        elif language == "nor" or language == "no" or language.lower() == "norwegian":
            return get_norwegian_wikipedia_accession(anatomical_structure)
        elif language == "per" or language == "fa" or language.lower() == "persian":
            return get_persian_wikipedia_accession(anatomical_structure)
        elif language == "pol" or language == "pl" or language.lower() == "polish":
            return get_polish_wikipedia_accession(anatomical_structure)
        elif language == "por" or language == "pt" or language.lower() == "portuguese":
            return get_portuguese_wikipedia_accession(anatomical_structure)
        elif language == "rum" or language == "ro" or language.lower() == "romanian":
            return get_romanian_wikipedia_accession(anatomical_structure)
        elif language == "rus" or language == "ru" or language.lower() == "russian":
            return get_russian_wikipedia_accession(anatomical_structure)
        elif language == "sco" or language.lower() == "scots":
            return get_scots_wikipedia_accession(anatomical_structure)
        elif language == "sh" or language.lower() == "serbo-croatian":
            return get_serbo_croatian_wikipedia_accession(anatomical_structure)
        elif language == "slv" or language == "sl" or language.lower() == "slovenian":
            return get_slovenian_wikipedia_accession(anatomical_structure)
        elif language == "spa" or language == "es" or language.lower() == "spanish":
            return get_spanish_wikipedia_accession(anatomical_structure)
        elif language == "swe" or language == "sv" or language.lower() == "swedish":
            return get_swedish_wikipedia_accession(anatomical_structure)
        elif language == "tam" or language == "ta" or language.lower() == "tamil":
            return get_tamil_wikipedia_accession(anatomical_structure)
        elif language == "tel" or language == "te" or language.lower() == "telugu":
            return get_telugu_wikipedia_accession(anatomical_structure)
        elif language == "tha" or language == "th" or language.lower() == "thai":
            return get_thai_wikipedia_accession(anatomical_structure)
        elif language == "tur" or language == "tr" or language.lower() == "turkish":
            return get_turkish_wikipedia_accession(anatomical_structure)
        elif language == "ukr" or language == "uk" or language.lower() == "ukrainian":
            return get_ukrainian_wikipedia_accession(anatomical_structure)
        elif language == "wln" or language == "wa" or language.lower() == "walloon":
            return get_walloon_wikipedia_accession(anatomical_structure)
        elif language == "xho" or language == "xh" or language.lower() == "xhosa":
            return get_xhosa_wikipedia_accession(anatomical_structure)
        else:
            print("The given language is not currently supported.")
        
    def xao_id(anatomical_structure):
        return get_xao_id(anatomical_structure)
        
    def zfa_id(anatomical_structure):
        return get_zfa_id(anatomical_structure)
    
    """
        Interaction objects:
        
        Tissues
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(anatomical_structure, user = None):
        interaction_obj = {}
        interaction_obj["Tissues"] = AnatomicalStructure.tissues(anatomical_structure)
        return interaction_obj
    
    # Get tissues.
    def tissues(anatomical_structure, children = False, descendants = False, hierarchical_descendants = False):
        return get_tissues(anatomical_structure, children = children, descendants = descendants, hierarchical_descendants = hierarchical_descendants)
    
    """
        Other properties:
        
        Anatomical connections
        Anatomical location
        Arterial supply
        Comment
        Connections (anatomical)
        Description
        External definition
        Venous drainage
        
    """
    
    def all_properties(anatomical_structure, user = None):
        property_dict = {}
        return property_dict
    
    def anatomical_connections(anatomical_structure, language = "en"):
        anatomical_connections = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "connects with":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                anatomical_connections.append(en_prop_name)
        return anatomical_connections
    
    def anatomical_location(anatomical_structure, language = "en"):
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "anatomical location":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                return en_prop_name
    
    def arterial_supply(anatomical_structure, language = "en"):
        anatomical_supply = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "arterial supply":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                anatomical_supply.append(en_prop_name)
        return anatomical_supply
    
    def classes(anatomical_structure, language = "en"):
        anatomical_classes = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "instance of":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                anatomical_classes.append(en_prop_name)
        return anatomical_classes
    
    def hypernym(anatomical_structure, language = "en"):
        anatomical_hypernyms = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "subclass of":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                anatomical_hypernyms.append(en_prop_name)
        return anatomical_hypernyms
    
    def venous_drainage(anatomical_structure, language = "en"):
        anatomical_drainage = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "venous drainage":
                    for x in prop_dict:
                        if "Q" in x["mainsnak"]["datavalue"]["value"]["id"]:
                            prop_id2 = x["mainsnak"]["datavalue"]["value"]["id"]
                            base2 = "https://www.wikidata.org/w/api.php"
                            ext2 = "?action=wbgetentities&ids=" + prop_id2 + "&format=json"
                            r = requests.get(base2+ext2, headers={"Content-Type": "application/json"})
                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()
                            decoded = json.loads(r.text)
                            if language == "en":
                                en_prop_name = decoded["entities"][prop_id2]["labels"]["en"]["value"]
                                anatomical_drainage.append(en_prop_name)
        return anatomical_drainage
    
    """
        URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None, source = "ebi", search_type = "exact", return_id_type = "sourceUi"):
        return search(query, user = user, source = source, search_type = search_type, return_id_type = return_id_type)

    """
        External files:
        
        Images
    """
    
    # Return images.
    def images(anatomical_structure):
        image_array = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                if en_prop_name.lower() == "image":
                    for x in prop_dict:
                        imag_url = "https://commons.wikimedia.org/wiki/File:" + x["mainsnak"]["datavalue"]["value"]
                        image_url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + x["mainsnak"]["datavalue"]["value"]
                        image_array.append(image_url)
        return image_array
    
#   UNIT TESTS
def anatomical_structure_unit_tests(uberon_id):
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = str(uberon_id), identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    print("All identifiers for %s..." % uberon_id)
    with open("temp_anat_iden_text.txt", "w", encoding="utf8") as f:
        str_iden = str(AnatomicalStructure.all_identifiers(uberon_anat))
        f.write(str_iden)
    
    print("Anatomical Location: %s" % (AnatomicalStructure.anatomical_location(uberon_anat)))
    print("\nAnatomical Connections:")
    for conn in AnatomicalStructure.anatomical_connections(uberon_anat):
        print("- %s" % conn)
    print("\nArterial Supply:")
    for sup in AnatomicalStructure.arterial_supply(uberon_anat):
        print("- %s" % sup)
    print("\nClasses:")
    for cla in AnatomicalStructure.classes(uberon_anat):
        print("- %s" % cla)
    print("\nHypernyms:")
    for hyp in AnatomicalStructure.hypernym(uberon_anat):
        print("- %s" % hyp)
    print("\nVenous Drainage:")
    for drain in AnatomicalStructure.venous_drainage(uberon_anat):
        print("- %s" % drain)
    print("\nImages:")
    for imag in AnatomicalStructure.images(uberon_anat):
        print("- %s" % imag)

#   MAIN
if __name__ == "__main__": main()