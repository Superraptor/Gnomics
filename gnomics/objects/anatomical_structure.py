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
import timeit
import wikipedia

#   Import sub-methods.
from gnomics.objects.anatomical_structure_files.aeo import get_aeo_id
from gnomics.objects.anatomical_structure_files.aod import get_aod
from gnomics.objects.anatomical_structure_files.bncf import get_bncf_thesaurus
from gnomics.objects.anatomical_structure_files.britannica import get_encyclopedia_britannica_online_id
from gnomics.objects.anatomical_structure_files.caro import get_caro_id 
from gnomics.objects.anatomical_structure_files.ccpss import get_ccpss
from gnomics.objects.anatomical_structure_files.ceph import get_ceph_id
from gnomics.objects.anatomical_structure_files.ehdaa import get_ehdaa2_id, get_ehdaa_id
from gnomics.objects.anatomical_structure_files.emap import get_emap_id, get_emapa_id
from gnomics.objects.anatomical_structure_files.fbbt import get_fbbt_id
from gnomics.objects.anatomical_structure_files.fma import get_fma_id
from gnomics.objects.anatomical_structure_files.freebase import get_freebase_id
from gnomics.objects.anatomical_structure_files.hao import get_hao_id
from gnomics.objects.anatomical_structure_files.jstor import get_jstor_topic_id
from gnomics.objects.anatomical_structure_files.loc import get_loc_sh
from gnomics.objects.anatomical_structure_files.ma import get_ma_id
from gnomics.objects.anatomical_structure_files.mesh import get_mesh_uid, get_mesh_term_english, get_mesh_tree_number, get_mesh_term_czech, get_mesh_term_dutch, get_mesh_term_finnish, get_mesh_term_french, get_mesh_term_german, get_mesh_term_italian, get_mesh_term_japanese, get_mesh_term_latvian, get_mesh_term_norwegian, get_mesh_term_polish, get_mesh_term_portuguese, get_mesh_term_russian, get_mesh_term_croatian, get_mesh_term_spanish, get_mesh_term_swedish
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
from gnomics.objects.interaction_objects.anatomical_structure_gene import get_genes_affecting_phenotype_of, get_genes_expressed_within
from gnomics.objects.interaction_objects.anatomical_structure_taxon import get_taxa
from gnomics.objects.interaction_objects.anatomical_structure_tissue import get_tissues

#   MAIN
def main():
    anatomical_structure_unit_tests("UBERON:0002386") # "UBERON:0000947") # "UBERON:0001424")

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
    
    # AEO BioPortal PURL.
    aeo_bioportal_purl = "http://purl.bioontology.org/ontology/AEO"
    
    # CARO BioPortal PURL.
    caro_bioportal_purl = "http://purl.bioontology.org/ontology/CARO"
    
    # CEPH BioPortal PURL.
    ceph_bioportal_purl = "http://purl.bioontology.org/ontology/CEPH"
    
    # EHDAA BioPortal PURL.
    ehdaa_bioportal_purl = "http://purl.bioontology.org/ontology/EHDAA"
    
    # EHDAA2 BioPortal PURL.
    ehdaa2_bioportal_purl = "http://purl.bioontology.org/ontology/EHDAA2"
    
    # EMAP BioPortal PURL.
    emap_bioportal_purl = "http://purl.bioontology.org/ontology/EMAP"
    
    # EMAPA BioPortal PURL.
    emapa_bioportal_purl = "http://purl.bioontology.org/ontology/EMAPA"
    
    # FB-BT BioPortal PURL.
    fbbt_bioportal_purl = "http://purl.bioontology.org/ontology/FB-BT"
    
    # FMA BioPortal PURL.
    fma_bioportal_purl = "http://purl.bioontology.org/ontology/FMA"
    
    # HAO BioPortal PURL.
    hao_bioportal_purl = "http://purl.bioontology.org/ontology/HAO"
    
    # MA BioPortal PURL.
    ma_bioportal_purl = "http://purl.bioontology.org/ontology/MA"
    
    # MFMO BioPortal PURL.
    mfmo_bioportal_purl = "http://purl.bioontology.org/ontology/MFMO"
    
    # NCIT BioPortal PURL.
    ncit_bioportal_purl = "http://purl.bioontology.org/ontology/NCIT"
    
    # PLANA BioPortal PURL.
    plana_bioportal_purl = "http://purl.bioontology.org/ontology/PLANA"
    
    # Read Codes, CTV3 (RCD) BioPortal PURL.
    rcd_bioportal_purl = "http://purl.bioontology.org/ontology/RCD"
    
    # TADS BioPortal PURL.
    tads_bioportal_purl = "http://purl.bioontology.org/ontology/TADS"
    
    # TGMA BioPortal PURL.
    tgma_bioportal_purl = "http://purl.bioontology.org/ontology/TGMA"
    
    # UBERON BioPortal PURL.
    uberon_bioportal_purl = "http://purl.bioontology.org/ontology/UBERON"
    
    # WB-BT BioPortal PURL.
    wbbt_bioportal_purl = "http://purl.bioontology.org/ontology/WB-BT"
    
    # XAO BioPortal PURL.
    xao_bioportal_purl = "http://purl.bioontology.org/ontology/XAO"
    
    # ZFA BioPortal PURL.
    zfa_bioportal_purl = "http://purl.bioontology.org/ontology/ZFA"
    
    """
        Anatomical structure attributes:
        
        Identifier      = A particular way to identify the
                          anatomical structure in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
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
    def __init__(self, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'taxon': taxon,
                'source': source,
                'name': name
            }]

        # Initialize dictionary of anatomical structure objects.
        self.anatomical_structure_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an anatomical structure.
    def add_identifier(anatomical_structure, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        anatomical_structure.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'taxon': taxon,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to an anatomical structure.
    def add_object(anatomical_structure, obj=None, object_type=None):
        anatomical_structure.anatomical_structure_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Anatomical structure objects:
        
        UBERON Object
        Wikidata Object
    """
    
    def uberon(anatomical_structure, user=None):
        return get_uberon_obj(anatomical_structure)
    
    def wikidata(anatomical_structure, user=None):
        return get_wikidata_object(anatomical_structure)
        
    """
        Anatomical structure identifiers:
        
        AEO (Anatomical Entity Ontology) ID
        AOD
        BNCF Thesaurus ID
        CARO ID
        CCPSS
        CEPH ID
        EHDAA ID
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
        NCI Thesaurus (NCIT) ID
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
    def all_identifiers(anatomical_structure, user=None):
        AnatomicalStructure.aeo_id(anatomical_structure, user=user)
        AnatomicalStructure.aod(anatomical_structure, user=user)
        AnatomicalStructure.bncf_thesaurus_id(anatomical_structure, user=user)
        AnatomicalStructure.caro_id(anatomical_structure, user=user)
        AnatomicalStructure.ceph_id(anatomical_structure, user=user)
        AnatomicalStructure.ccpss(anatomical_structure, user=user)
        AnatomicalStructure.ehdaa_id(anatomical_structure, user=user)
        AnatomicalStructure.ehdaa2_id(anatomical_structure, user=user)
        AnatomicalStructure.emap_id(anatomical_structure, user=user)
        AnatomicalStructure.emapa_id(anatomical_structure, user=user)
        AnatomicalStructure.encyclopedia_britannica_online_id(anatomical_structure, user=user)
        AnatomicalStructure.fbbt_id(anatomical_structure, user=user)
        AnatomicalStructure.fma_id(anatomical_structure, user=user)
        AnatomicalStructure.freebase_id(anatomical_structure, user=user)
        AnatomicalStructure.hao_id(anatomical_structure, user=user)
        AnatomicalStructure.jstor_topic_id(anatomical_structure, user=user)
        AnatomicalStructure.loc_sh(anatomical_structure, user=user)
        AnatomicalStructure.ma_id(anatomical_structure, user=user)
        AnatomicalStructure.mfmo_id(anatomical_structure, user=user)
        AnatomicalStructure.nci_thesaurus_id(anatomical_structure, user=user)
        AnatomicalStructure.neu_id(anatomical_structure, user=user)
        AnatomicalStructure.plana_id(anatomical_structure, user=user)
        AnatomicalStructure.psy(anatomical_structure, user=user)
        AnatomicalStructure.read_codes(anatomical_structure, user=user)
        AnatomicalStructure.ta98_id(anatomical_structure, user=user)
        AnatomicalStructure.ta98_latin_term(anatomical_structure, user=user)
        AnatomicalStructure.tads_id(anatomical_structure, user=user)
        AnatomicalStructure.tgma_id(anatomical_structure, user=user)
        AnatomicalStructure.uberon_id(anatomical_structure, user=user)
        AnatomicalStructure.uwda_id(anatomical_structure, user=user)
        AnatomicalStructure.wbbt_id(anatomical_structure, user=user)
        AnatomicalStructure.wikidata_accession(anatomical_structure, user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="albanian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="arabic", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="aramaic", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="aymara", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="azerbaijani", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bangla", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bashkir", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="basque", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="breton", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bosnian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="bulgarian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="cantonese", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="catalan", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="central kurdish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="chinese", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="classical chinese", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="croatian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="czech", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="danish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="divehi", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="dutch", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="english", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="simple english", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="esperanto", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="finnish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="french", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="galician", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="georgian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="german", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="greek", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="hebrew", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="hungarian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="ido", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="indonesian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="irish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="italian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="japanese", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="kazakh", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="korean", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="latin", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="latvian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="lithuanian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="macedonian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="newari", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="norwegian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="persian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="polish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="portuguese", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="romanian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="russian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="scots", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="serbo-croatian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="slovenian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="spanish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="swedish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="tamil", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="telugu", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="thai", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="turkish", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="ukrainian", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="walloon", user=user)
        AnatomicalStructure.wikipedia_accession(anatomical_structure, language="xhosa", user=user)
        AnatomicalStructure.xao_id(anatomical_structure, user=user)
        AnatomicalStructure.zfa_id(anatomical_structure, user=user)
        return anatomical_structure.identifiers
    
    def aeo_id(anatomical_structure, user=None):
        return get_aeo_id(anatomical_structure, user=user)
        
    def aod(anatomical_structure, user=None):
        return get_aod(anatomical_structure, user=user)
        
    def bncf_thesaurus_id(anatomical_structure, user=None):
        return get_bncf_thesaurus(anatomical_structure)
        
    def caro_id(anatomical_structure, user=None):
        return get_caro_id(anatomical_structure, user=user)
        
    def ceph_id(anatomical_structure, user=None):
        return get_ceph_id(anatomical_structure, user=user)
    
    def ccpss(anatomical_structure, user=None):
        return get_ccpss(anatomical_structure, user=user)
        
    def ehdaa_id(anatomical_structure, user=None):
        return get_ehdaa_id(anatomical_structure, user=user)
    
    def ehdaa2_id(anatomical_structure, user=None):
        return get_ehdaa2_id(anatomical_structure, user=user)
        
    def emap_id(anatomical_structure, user=None):
        return get_emap_id(anatomical_structure, user=user)
        
    def emapa_id(anatomical_structure, user=None):
        return get_emapa_id(anatomical_structure, user=user)
        
    def encyclopedia_britannica_online_id(anatomical_structure, user=None):
        return get_encyclopedia_britannica_online_id(anatomical_structure, user=user)
        
    def fbbt_id(anatomical_structure, user=None):
        return get_fbbt_id(anatomical_structure, user=user)
        
    def fma_id(anatomical_structure, user=None):
        return get_fma_id(anatomical_structure, user=user)
        
    def freebase_id(anatomical_structure, user=None):
        return get_freebase_id(anatomical_structure, user=user)
        
    def hao_id(anatomical_structure, user=None):
        return get_hao_id(anatomical_structure, user=user)
        
    def jstor_topic_id(anatomical_structure, user=None):
        return get_jstor_topic_id(anatomical_structure, user=user)
    
    def loc_sh(anatomical_structure, user=None):
        return get_loc_sh(anatomical_structure, user=user)
        
    def ma_id(anatomical_structure, user=None):
        return get_ma_id(anatomical_structure, user=user)
    
    def mesh_term(anatomical_structure, language="en", user=None):
        mesh_term_array = []
        if language.lower() in ["all", "hry", "hr", "croatian"]:
            mesh_term_array.extend(get_mesh_term_croatian(anatomical_structure, user=user))
        if language.lower() in ["all", "cze", "cs", "czech"]:
            mesh_term_array.extend(get_mesh_term_czech(anatomical_structure, user=user))
        if language.lower() in ["all", "dut", "nl", "dutch"]:
            mesh_term_array.extend(get_mesh_term_dutch(anatomical_structure, user=user))
        if language.lower() in ["all", "eng", "en", "english"]:
            mesh_term_array.extend(get_mesh_term_english(anatomical_structure, user=user))
        if language.lower() in ["all", "fin", "fi", "finnish"]:
            mesh_term_array.extend(get_mesh_term_finnish(anatomical_structure, user=user))
        if language.lower() in ["all", "fre", "fr", "french"]:
            mesh_term_array.extend(get_mesh_term_french(anatomical_structure, user=user))
        if language.lower() in ["all", "ger", "de", "german"]:
            mesh_term_array.extend(get_mesh_term_german(anatomical_structure, user=user))
        if language.lower() in ["all", "ita", "it", "italian"]:
            mesh_term_array.extend(get_mesh_term_italian(anatomical_structure, user=user))
        if language.lower() in ["all", "jpn", "ja", "japanese"]:
            mesh_term_array.extend(get_mesh_term_japanese(anatomical_structure, user=user))
        if language.lower() in ["all", "lav", "lv", "latvian"]:
            mesh_term_array.extend(get_mesh_term_latvian(anatomical_structure, user=user))
        if language.lower() in ["all", "nor", "no", "norwegian"]:
            mesh_term_array.extend(get_mesh_term_norwegian(anatomical_structure, user=user))
        if language.lower() in ["all", "pol", "pl", "polish"]:
            mesh_term_array.extend(get_mesh_term_polish(anatomical_structure, user=user))
        if language.lower() in ["all", "por", "pt", "portuguese"]:
            mesh_term_array.extend(get_mesh_term_portuguese(anatomical_structure, user=user))
        if language.lower() in ["all", "rus", "ru", "russian"]:
            mesh_term_array.extend(get_mesh_term_russian(anatomical_structure, user=user))
        if language.lower() in ["all", "spa", "es", "spanish"]:
            mesh_term_array.extend(get_mesh_term_spanish(anatomical_structure, user=user))
        if language.lower() in ["all", "swe", "sv", "swedish"]:
            mesh_term_array.extend(get_mesh_term_swedish(anatomical_structure, user=user))
        if not mesh_term_array:
            print("The given language (%s) is not currently supported." % str(language))
        return mesh_term_array
    
    def mesh_tree_number(anatomical_structure, user=None):
        return get_mesh_tree_number(anatomical_structure, user=user)
    
    def mesh_uid(anatomical_structure, user=None):
        return get_mesh_uid(anatomical_structure, user=user)
        
    def mfmo_id(anatomical_structure, user=None):
        return get_mfmo_id(anatomical_structure, user=user)
        
    def nci_thesaurus_id(anatomical_structure, user=None):
        return get_nci_thesaurus_id(anatomical_structure, user=user)
    
    def ncit_id(anatomical_structure, user=None):
        return AnatomicalStructure.nci_thesaurus_id(anatomical_structure, user=user)
        
    def neu_id(anatomical_structure, user=None):
        return get_neu_id(anatomical_structure, user=user)
        
    def plana_id(anatomical_structure, user=None):
        return get_plana_id(anatomical_structure, user=user)
    
    # Get Thesaurus of Psychological Index Terms (PSY).
    def psy(anatomical_structure, user=None):
        return get_psy(anatomical_structure, user=user)
    
    # Get Read Codes.
    def rcd_id(anatomical_structure, user=None):
        return AnatomicalStructure.read_codes(anatomical_structure, user=user)
    
    # Get Read Codes.
    def read_codes(anatomical_structure, user=None):
        return get_read_codes(anatomical_structure, user=user)
    
    # Get Terminologia Anatomica 98 (TA98) ID.
    def ta98_id(anatomical_structure, user=None):
        return get_ta98_id(anatomical_structure, user=user)
    
    # Get Terminologia Anatomica 98 (TA98) Latin Term.
    def ta98_latin_term(anatomical_structure, user=None):
        return get_ta98_latin_term(anatomical_structure, user=user)
        
    def tads_id(anatomical_structure, user=None):
        return get_tads_id(anatomical_structure)
        
    def tgma_id(anatomical_structure, user=None):
        return get_tgma_id(anatomical_structure)
    
    def uberon_id(anatomical_structure, user=None):
        return get_uberon_id(anatomical_structure)
        
    def uwda_id(anatomical_structure, user=None):
        return get_uwda_id(anatomical_structure, user=user)
        
    def wbbt_id(anatomical_structure, user=None):
        return get_wbbt_id(anatomical_structure)
    
    def wikidata_accession(anatomical_structure, user=None):
        return get_wikidata_accession(anatomical_structure)
        
    def wikipedia_accession(anatomical_structure, language="en", user=None):
        wiki_array = []
        if language.lower() in ["all", "sqi", "sq", "albanian"]:
            wiki_array.extend(get_albanian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ara", "ar", "arabic"]:
            wiki_array.extend(get_arabic_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "arc", "aramaic"]:
            wiki_array.extend(get_aramaic_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "aym", "ay", "aymara"]:
            wiki_array.extend(get_aymara_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "aze", "az", "azerbaijani"]:
            wiki_array.extend(get_azerbaijani_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ben", "bn", "bangla", "bengali"]:
            wiki_array.extend(get_bangla_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "bak", "ba", "bashkir"]:
            wiki_array.extend(get_bashkir_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "baq", "eu", "basque"]:
            wiki_array.extend(get_basque_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "bre", "br", "breton"]:
            wiki_array.extend(get_breton_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "bos", "bs", "bosnian"]:
            wiki_array.extend(get_bosnian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "bul", "bg", "bulgarian"]:
            wiki_array.extend(get_bulgarian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "zh_yue", "cantonese"]:
            wiki_array.extend(get_cantonese_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "cat", "ca", "catalan"]:
            wiki_array.extend(get_catalan_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ckb", "central kurdish"]:
            wiki_array.extend(get_central_kurdish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "chi", "zh", "chinese"]:
            wiki_array.extend(get_chinese_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "zh_classical", "classical chinese"]:
            wiki_array.extend(get_classical_chinese_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "hry", "hr", "croatian"]:
            wiki_array.extend(get_croatian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "cze", "cs", "czech"]:
            wiki_array.extend(get_czech_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "dan", "da", "danish"]:
            wiki_array.extend(get_danish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "div", "dv", "divehi"]:
            wiki_array.extend(get_divehi_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "dut", "nl", "dutch"]:
            wiki_array.extend(get_dutch_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "eng", "en", "english"]:
            wiki_array.extend(get_english_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "simple", "simple english"]:
            wiki_array.extend(get_simple_english_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "epo", "eo", "ep", "esperanto"]:
            wiki_array.extend(get_esperanto_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "fin", "fi", "finnish"]:
            wiki_array.extend(get_finnish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "fre", "fr", "french"]:
            wiki_array.extend(get_french_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "glg", "gl", "galician"]:
            wiki_array.extend(get_galician_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "geo", "ka", "georgian"]:
            wiki_array.extend(get_georgian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ger", "de", "german"]:
            wiki_array.extend(get_german_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "gre", "el", "greek"]:
            wiki_array.extend(get_greek_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "heb", "he", "hebrew"]:
            wiki_array.extend(get_hebrew_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "hun", "hu", "hungarian"]:
            wiki_array.extend(get_hungarian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ido", "io", "ido"]:
            wiki_array.extend(get_ido_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ind", "id", "indonesian"]:
            wiki_array.extend(get_indonesian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "gle", "ga", "irish"]:
            wiki_array.extend(get_irish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ita", "it", "italian"]:
            wiki_array.extend(get_italian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "jpn", "ja", "japanese"]:
            wiki_array.extend(get_japanese_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "kaz", "kk", "kazakh"]:
            wiki_array.extend(get_kazakh_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "kor", "ko", "korean"]:
            wiki_array.extend(get_korean_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "lat", "la", "latin"]:
            wiki_array.extend(get_latin_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "lav", "lv", "latvian"]:
            wiki_array.extend(get_latvian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "lit", "lt", "lithuanian"]:
            wiki_array.extend(get_lithuanian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "mac", "mk", "macedonian"]:
            wiki_array.extend(get_macedonian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "new", "newari"]:
            wiki_array.extend(get_newari_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "nor", "no", "norwegian"]:
            wiki_array.extend(get_norwegian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "per", "fa", "persian"]:
            wiki_array.extend(get_persian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "pol", "pl", "polish"]:
            wiki_array.extend(get_polish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "por", "pt", "portuguese"]:
            wiki_array.extend(get_portuguese_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "rum", "ro", "romanian"]:
            wiki_array.extend(get_romanian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "rus", "ru", "russian"]:
            wiki_array.extend(get_russian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "sco", "scots"]:
            wiki_array.extend(get_scots_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "sh", "serbo-croatian"]:
            wiki_array.extend(get_serbo_croatian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "slv", "sl", "slovenian"]:
            wiki_array.extend(get_slovenian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "spa", "es", "spanish"]:
            wiki_array.extend(get_spanish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "swe", "sv", "swedish"]:
            wiki_array.extend(get_swedish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "tam", "ta", "tamil"]:
            wiki_array.extend(get_tamil_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "tel", "te", "telugu"]:
            wiki_array.extend(get_telugu_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "tha", "th", "thai"]:
            wiki_array.extend(get_thai_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "tur", "tr", "turkish"]:
            wiki_array.extend(get_turkish_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "ukr", "uk", "ukrainian"]:
            wiki_array.extend(get_ukrainian_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "wln", "wa", "walloon"]:
            wiki_array.extend(get_walloon_wikipedia_accession(anatomical_structure))
        if language.lower() in ["all", "xho", "xh", "xhosa"]:
            wiki_array.extend(get_xhosa_wikipedia_accession(anatomical_structure))
        if not wiki_array:
            print("The given language (%s) is not currently supported." % str(language))
        return wiki_array
        
    def xao_id(anatomical_structure, user=None):
        return get_xao_id(anatomical_structure, user=user)
        
    def zfa_id(anatomical_structure, user=None):
        return get_zfa_id(anatomical_structure, user=user)
    
    """
        Interaction objects:
        
        Genes Affecting Phenotype Of
        Genes Expressed Within
        Taxa
        Tissues
    """
    
    # Return interaction objects.
    def all_interaction_objects(anatomical_structure, user=None):
        interaction_obj = {}
        interaction_obj["Taxa"] = AnatomicalStructure.taxa(anatomical_structure, user=user)
        interaction_obj["Tissues"] = AnatomicalStructure.tissues(anatomical_structure, user=user)
        return interaction_obj
    
    # Get genes affecting the phenotype of the
    # given anatomical structure.
    def genes_affecting_phenotype_of(anatomical_structure, user=None):
        return get_genes_affecting_phenotype_of(anatomical_structure)
    
    # Get genes expressed in the given anatomical structure.
    def genes_expressed_within(anatomical_structure, user=None):
        return get_genes_expressed_within(anatomical_structure)
    
    # Get taxa.
    def taxa(anatomical_structure, user=None):
        return get_taxa(anatomical_structure)
    
    # Get tissues.
    def tissues(anatomical_structure, children=False, descendants=False, hierarchical_descendants=False, user=None):
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
    
    def all_properties(anatomical_structure, user=None):
        property_dict = {}
        return property_dict
    
    def anatomical_connections(anatomical_structure, language="en", user=None):
        anatomical_connections = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                    
                if language in ["en", "eng", "english"]:

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
    
    def anatomical_location(anatomical_structure, language="en", user=None):
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
    
    def arterial_supply(anatomical_structure, language="en", user=None):
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
    
    def classes(anatomical_structure, language="en", user=None):
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
    
    def hypernym(anatomical_structure, language="en", user=None):
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
    
    def venous_drainage(anatomical_structure, language="en", user=None):
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
        
        AEO BioPortal URL
        CARO BioPortal URL
        CEPH BioPortal URL
        EHDAA BioPortal URL
        EHDAA2 BioPortal URL
        EMAP BioPortal URL
        EMAPA BioPortal URL
        FBBT BioPortal URL
        FMA BioPortal URL
        HAO BioPortal URL
        MA BioPortal URL
        MFMO BioPortal URL
        NCIT BioPortal URL
        PLANA BioPortal URL
        RCD BioPortal URL
        TADS BioPortal URL
        TGMA BioPortal URL
        UBERON BioPortal URL
        WBBT BioPortal URL
        XAO BioPortal URL
        ZFA BioPortal URL
    """
    
    # Return links.
    def all_urls(anatomical_structure, user=None):
        url_dict = {}
        url_dict["AEO BioPortal"] = AnatomicalStructre.aeo_bioportal_url(anatomical_structure, user=user)
        url_dict["CARO BioPortal"] = AnatomicalStructre.caro_bioportal_url(anatomical_structure, user=user)
        url_dict["CEPH BioPortal"] = AnatomicalStructre.ceph_bioportal_url(anatomical_structure, user=user)
        url_dict["EHDAA BioPortal"] = AnatomicalStructre.ehdaa_bioportal_url(anatomical_structure, user=user)
        url_dict["EHDAA2 BioPortal"] = AnatomicalStructre.ehdaa2_bioportal_url(anatomical_structure, user=user)
        url_dict["EMAP BioPortal"] = AnatomicalStructre.emap_bioportal_url(anatomical_structure, user=user)
        url_dict["EMAPA BioPortal"] = AnatomicalStructre.emapa_bioportal_url(anatomical_structure, user=user)
        url_dict["FBBT BioPortal"] = AnatomicalStructre.fbbt_bioportal_url(anatomical_structure, user=user)
        url_dict["FMA BioPortal"] = AnatomicalStructre.fma_bioportal_url(anatomical_structure, user=user)
        url_dict["HAO BioPortal"] = AnatomicalStructre.hao_bioportal_url(anatomical_structure, user=user)
        url_dict["MA BioPortal"] = AnatomicalStructre.ma_bioportal_url(anatomical_structure, user=user)
        url_dict["MFMO BioPortal"] = AnatomicalStructre.mfmo_bioportal_url(anatomical_structure, user=user)
        url_dict["NCIT BioPortal"] = AnatomicalStructre.ncit_bioportal_url(anatomical_structure, user=user)
        url_dict["PLANA BioPortal"] = AnatomicalStructre.plana_bioportal_url(anatomical_structure, user=user)
        url_dict["RCD BioPortal"] = AnatomicalStructre.rcd_bioportal_url(anatomical_structure, user=user)
        url_dict["TADS BioPortal"] = AnatomicalStructre.tads_bioportal_url(anatomical_structure, user=user)
        url_dict["TGMA BioPortal"] = AnatomicalStructre.tgma_bioportal_url(anatomical_structure, user=user)
        url_dict["UBERON BioPortal"] = AnatomicalStructre.uberon_bioportal_url(anatomical_structure, user=user)
        url_dict["WBBT BioPortal"] = AnatomicalStructre.wbbt_bioportal_url(anatomical_structure, user=user)
        url_dict["XAO BioPortal"] = AnatomicalStructre.xao_bioportal_url(anatomical_structure, user=user)
        url_dict["ZFA BioPortal"] = AnatomicalStructre.zfa_bioportal_url(anatomical_structure, user=user)
        return url_dict
    
    # Return AEO BioPortal URL.
    def aeo_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.aeo_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.aeo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return CARO BioPortal URL.
    def caro_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.caro_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.caro_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return CEPH BioPortal URL.
    def ceph_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.ceph_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.ceph_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return EHDAA BioPortal URL.
    def ehdaa_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.ehdaa_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.ehdaa_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return EHDAA2 BioPortal URL.
    def ehdaa2_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.ehdaa2_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.ehdaa2_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return EMAP BioPortal URL.
    def emap_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.emap_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.emap_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return EMAPA BioPortal URL.
    def emapa_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.emapa_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.emapa_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return FB-BT BioPortal URL.
    def fbbt_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.fbbt_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.fbbt_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return FMA BioPortal URL.
    def fma_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.fma_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.fma_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return HAO BioPortal URL.
    def hao_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.hao_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.hao_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MA BioPortal URL.
    def ma_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.ma_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.ma_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MFMO BioPortal URL.
    def mfmo_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.mfmo_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.mfmo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return NCIT BioPortal URL.
    def ncit_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.nci_thesaurus_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.ncit_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return PLANA BioPortal URL.
    def plana_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.plana_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.plana_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return RCD BioPortal URL.
    def rcd_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.read_codes(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.rcd_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return TADS BioPortal URL.
    def tads_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.tads_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.tads_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return TGMA BioPortal URL.
    def tgma_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.tgma_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.tgma_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return UBERON BioPortal URL.
    def uberon_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.uberon_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.uberon_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return WBBT BioPortal URL.
    def wbbt_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.wbbt_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.wbbt_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return XAO BioPortal URL.
    def xao_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.xao_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.xao_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return ZFA BioPortal URL.
    def zfa_bioportal_url(anatomical_structure, user=None):
        url_array = []
        for iden in AnatomicalStructure.zfa_id(anatomical_structure, user=user):
            url_array.append(AnatomicalStructure.zfa_bioportal_purl + "/" + str(iden))
        return url_array
    
    """
        Auxiliary functions:
        
        Search
    """
    
    def search(query, user=None, source="ebi", search_type="exact", return_id_type="sourceUi"):
        return search(query, user=user, source=source, search_type=search_type, return_id_type=return_id_type)

    """
        External files:
        
        Images
    """
    
    # Return images.
    def images(anatomical_structure, user=None):
        image_array = []
        for stuff in AnatomicalStructure.wikidata(anatomical_structure):
            for prop_id, prop_dict in stuff["claims"].items():
                base = "https://www.wikidata.org/w/api.php"
                ext = "?action=wbgetentities&ids=" + str(prop_id) + "&format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:

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