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
#   Create instance of a phenotype.
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
import gnomics.objects.disease

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.phenotype_files.apo import get_apo_id
from gnomics.objects.phenotype_files.atol import get_atol_id
from gnomics.objects.phenotype_files.ddpheno import get_ddpheno_id
from gnomics.objects.phenotype_files.fbcv import get_fbcv_id
from gnomics.objects.phenotype_files.flopo import get_flopo_id
from gnomics.objects.phenotype_files.fypo import get_fypo_id
from gnomics.objects.phenotype_files.hpo import get_hpo_id, get_hpo_term, get_hpo_synonyms
from gnomics.objects.phenotype_files.meddra import get_meddra_id, get_meddra_term
from gnomics.objects.phenotype_files.mesh import get_mesh_uid
from gnomics.objects.phenotype_files.mp import get_mp_id
from gnomics.objects.phenotype_files.mpo import get_mpo_id
from gnomics.objects.phenotype_files.omp import get_omp_id
from gnomics.objects.phenotype_files.repo import get_repo_id
from gnomics.objects.phenotype_files.search import search
from gnomics.objects.phenotype_files.snomed import get_snomed_ct_id
from gnomics.objects.phenotype_files.spto import get_spto_id
from gnomics.objects.phenotype_files.to import get_to_id
from gnomics.objects.phenotype_files.umls import get_umls_cui
from gnomics.objects.phenotype_files.upheno import get_upheno_id
from gnomics.objects.phenotype_files.vt import get_vt_id
from gnomics.objects.phenotype_files.wbphenotype import get_wbphenotype_id

#   Import further methods.
from gnomics.objects.interaction_objects.phenotype_anatomical_structure import get_anatomical_structures
from gnomics.objects.interaction_objects.phenotype_variation import get_variations

#   MAIN
def main():
    phenotype_unit_tests()

#   PHENOTYPE CLASS
class Phenotype:
    """
        Phenotype class
        
        A phenotype is the composite of an organism's 
        observable traits including morphology, development, 
        biochemical properties, physiological and anatomical 
        properties, behavior, and behavioral products.
    """
    
    # APO BioPortal PURL.
    apo_bioportal_purl = "http://purl.bioontology.org/ontology/APO"
    
    # ATOL BioPortal PURL.
    atol_bioportal_purl = "http://purl.bioontology.org/ontology/ATOL"
    
    # DDPHENO BioPortal PURL.
    ddpheno_bioportal_purl = "http://purl.bioontology.org/ontology/DDPHENO"
    
    # FLOPO BioPortal PURL.
    flopo_bioportal_purl = "http://purl.bioontology.org/ontology/FLOPO"
    
    # FYPO BioPortal PURL.
    fypo_bioportal_purl = "http://purl.bioontology.org/ontology/FYPO"
    
    # Human Phenotype Ontology (HP) BioPortal PURL.
    hp_bioportal_purl = "http://purl.bioontology.org/ontology/HP"
    
    # Mammalian Phenotype Ontology (MP) BioPortal PURL.
    mp_bioportal_purl = "http://purl.bioontology.org/ontology/MP"
    
    # Microbial Phenotype Ontology (MPO) BioPortal PURL.
    mpo_bioportal_purl = "http://purl.bioontology.org/ontology/MPO"
    
    # Ontology of Microbial Phenotypes (OMP) BioPortal PURL.
    omp_bioportal_purl = "http://purl.bioontology.org/ontology/OMP"
    
    # Reproductive Trait and Phenotype Ontology (REPO) BioPortal PURL.
    repo_bioportal_purl = "http://purl.bioontology.org/ontology/REPO"
    
    # SPTO BioPortal PURL.
    spto_bioportal_purl = "http://purl.bioontology.org/ontology/SPTO"
    
    # UPHENO BioPortal PURL.
    upheno_bioportal_purl = "http://purl.bioontology.org/ontology/UPHENO"
    
    # WB-PHENOTYPE BioPortal PURL.
    wb_phenotype_bioportal_purl = "http://purl.bioontology.org/ontology/WB-PHENOTYPE"
    
    """
        Phenotype attributes:
        
        Identifier      = A particular way to identify the
                          phenotype in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The taxon from which the protein
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the phenotype.
    def __init__(self, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        
        # If HPO-related, set taxon to "Homo sapiens."
        if identifier is not None:
            if identifier_type.lower() in ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology", "hp label", "hp term", "hpo label", "hpo term", "human phenotype ontology label", "human phenotype ontology term"]:
                taxon = "Homo sapiens"
        
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
        
        # Initialize dictionary of phenotype objects.
        self.phenotype_objects = []
        
    # Add an identifier to a phenotype.
    def add_identifier(phenotype, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        phenotype.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Phenotype objects
        
    """
    
    

    """
        Phenotype identifiers:
        
        HPO ID
        HPO Synonyms
        HPO Term
        MedDRA ID
        MedDRA Term
        MeSH UID
        SNOMED-CT ID
        UMLS CUI
    """
    
    # Return all identifiers.
    def all_identifiers(phenotype, user=None):
        Phenotype.apo_id(phenotype, user=user)
        Phenotype.atol_id(phenotype, user=user)
        Phenotype.ddpheno_id(phenotype, user=user)
        Phenotype.fbcv_id(phenotype, user=user)
        Phenotype.flopo_id(phenotype, user=user)
        Phenotype.fypo_id(phenotype, user=user)
        Phenotype.hpo_id(phenotype, user=user)
        Phenotype.hpo_synonyms(phenotype, user=user)
        Phenotype.hpo_term(phenotype, user=user)
        Phenotype.meddra_id(phenotype, user=user)
        Phenotype.meddra_term(phenotype, user=user)
        Phenotype.mesh_uid(phenotype, user=user)
        Phenotype.mp_id(phenotype, user=user)
        Phenotype.mpo_id(phenotype, user=user)
        Phenotype.oba_id(phenotype, user=user)
        Phenotype.omp_id(phenotype, user=user)
        Phenotype.repo_id(phenotype, user=user)
        Phenotype.snomed_ct_id(phenotype, user=user)
        Phenotype.spto_id(phenotype, user=user)
        Phenotype.to_id(phenotype, user=user)
        Phenotype.umls_cui(phenotype, user=user)
        Phenotype.upheno_id(phenotype, user=user)
        Phenotype.vt_id(phenotype, user=user)
        Phenotype.wbphenotype_id(phenotype, user=user)
        return phenotype.identifiers
    
    # Returns APO IDs (Ascomycete Phenotype Ontology).
    def apo_id(phenotype, user=None):
        return get_apo_id(phenotype, user=user)
    
    # Returns ATOL IDs (Animal Trait Ontology for Livestock).
    def atol_id(phenotype, user=None):
        return get_atol_id(phenotype, user=user)
    
    # Returns DDPHENO IDs (Dictyostelium Discoideum Phenotype Ontology).
    def ddpheno_id(phenotype, user=None):
        return get_ddpheno_id(phenotype, user=user)
    
    # Returns FB-CV IDs (FlyBase Controlled Vocabulary).
    def fbcv_id(phenotype, user=None):
        return get_fbcv_id(phenotype, user=user)
    
    # Returns FLOPO IDs (Flora Phenotype Ontology).
    def flopo_id(phenotype, user=None):
        return get_flopo_id(phenotype, user=user)
    
    # Returns FYPO IDs (Fission Yeast Phenotype Ontology).
    def fypo_id(phenotype, user=None):
        return get_fypo_id(phenotype, user=user)
    
    # Returns HP IDs (Human Phenotype Ontology).
    def hp_id(phenotype, user=None):
        return Phenotype.hpo_id(phenotype, user=user)
    
    # Returns HPO IDs (Human Phenotype Ontology).
    def hpo_id(phenotype, user=None):
        return get_hpo_id(phenotype, user=user)
    
    # Returns HPO Synonyms.
    def hpo_synonyms(phenotype, user=None):
        return get_hpo_synonyms(phenotype, user=user)
    
    # Returns HPO Terms.
    def hpo_term(phenotype, user=None):
        return get_hpo_term(phenotype, user=user)
    
    # Returns MedDRA IDs.
    def meddra_id(phenotype, user=None):
        return get_meddra_id(phenotype, user=user)
    
    # Returns MedDRA Terms.
    def meddra_term(phenotype, user=None):
        return get_meddra_term(phenotype, user=user)
    
    # Returns MeSH UIDs.
    def mesh_uid(phenotype, user=None):
        return get_mesh_uid(phenotype, user=user)
    
    # Returns MP IDs (Mammalian Phenotype Ontology).
    def mp_id(phenotype, user=None):
        return get_mp_id(phenotype, user=user)
    
    # Returns MPO IDs (Microbial Phenotype Ontology).
    def mpo_id(phenotype, user=None):
        return get_mpo_id(phenotype, user=user)
    
    # Returns OBA IDs (Ontology of Biological Attributes).
    def oba_id(phenotype, user=None):
        return get_oba_id(phenotype, user=user)
    
    # Returns OMP IDs (Ontology of Microbial Phenotypes).
    def omp_id(phenotype, user=None):
        return get_omp_id(phenotype, user=user)
    
    # Returns PTO IDs (Plant Trait Ontology).
    def pto_id(phenotype, user=None):
        return Phenotype.to_id(phenotype, user=user)
    
    # Returns REPO IDs (Reproductive Trait and Phenotype Ontology).
    def repo_id(phenotype, user=None):
        return get_repo_id(phenotype, user=user)
    
    # Returns SNOMED CT ID.
    def snomed_ct_id(phenotype, user=None):
        return get_snomed_ct_id(phenotype, user=user)
    
    # Returns SPTO IDs (Solanaceae Phenotype Ontology).
    def spto_id(phenotype, user=None):
        return get_spto_id(phenotype, user=user)
    
    # Returns TO IDs (Plant Trait Ontology).
    def to_id(phenotype, user=None):
        return get_to_id(phenotype, user=user)
    
    # Returns UMLS CUI.
    def umls_cui(phenotype, user=None):
        return get_umls_cui(phenotype, user=user)
    
    # Returns UPHENO IDs (Combined Phenotype Ontology).
    def upheno_id(phenotype, user=None):
        return get_upheno_id(phenotype, user=user)
    
    # Returns VT IDs (Vertebrate Trait Ontology).
    def vt_id(phenotype, user=None):
        return get_vt_id(phenotype, user=user)
    
    # Returns WB-PHENOTYPE IDs (C. elegans Phenotype Vocabulary).
    def wbphenotype_id(phenotype, user=None):
        return get_wbphenotype_id(phenotype, user=user)
    
    """
        Interaction objects:
        
        Anatomical structures
        Variations
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(phenotype, user=None):
        interaction_obj = {}
        interaction_obj["Anatomical_Structures"] = Phenotype.anatomical_structures(phenotype, user=user)
        interaction_obj["Variations"] = Phenotype.variations(phenotype, user=user)
        return interaction_obj
    
    # Get anatomical structures.
    def anatomical_structures(phenotype, user=None):
        return get_anatomical_structures(phenotype)
    
    # Get variations.
    def variations(phenotype, user=None):
        return get_variations(phenotype)
    
    """
        Other properties
        
    """
    
    def all_properties(phenotype, user=None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
        APO BioPortal URL
        ATOL BioPortal URL
        DDPHENO BioPortal URL
        FLOPO BioPortal URL
        FYPO BioPortal URL
        HP BioPortal URL
        MP BioPortal URL
        MPO BioPortal URL
        OMP BioPortal URL
        REPO BioPortal URL
        SPTO BioPortal URL
        UPHENO BioPortal URL
        WB-PHENOTYPE BioPortal URL
    """
    
    # Return links.
    def all_urls(phenotype, user=None):
        url_dict = {}
        url_dict["APO BioPortal"] = apo_bioportal_url(phenotype, user=user)
        url_dict["ATOL BioPortal"] = atol_bioportal_url(phenotype, user=user)
        url_dict["DDPHENO BioPortal"] = ddpheno_bioportal_url(phenotype, user=user)
        url_dict["FLOPO BioPortal"] = flopo_bioportal_url(phenotype, user=user)
        url_dict["FYPO BioPortal"] = fypo_bioportal_url(phenotype, user=user)
        url_dict["HP BioPortal"] = hp_bioportal_url(phenotype, user=user)
        url_dict["MP BioPortal"] = mp_bioportal_url(phenotype, user=user)
        url_dict["MPO BioPortal"] = mpo_bioportal_url(phenotype, user=user)
        url_dict["OMP BioPortal"] = omp_bioportal_url(phenotype, user=user)
        url_dict["REPO BioPortal"] = repo_bioportal_url(phenotype, user=user)
        url_dict["SPTO BioPortal"] = spto_bioportal_url(phenotype, user=user)
        url_dict["UPHENO BioPortal"] = upheno_bioportal_url(phenotype, user=user)
        url_dict["WB-PHENOTYPE BioPortal"] = wbphenotype_bioportal_url(phenotype, user=user)
        return url_dict
    
    # Return APO BioPortal URL.
    def apo_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.apo_id(phenotype, user=user):
            url_array.append(Phenotype.apo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return ATOL BioPortal URL.
    def atol_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.atol_id(phenotype, user=user):
            url_array.append(Phenotype.atol_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return DDPHENO BioPortal URL.
    def ddpheno_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.ddpheno_id(phenotype, user=user):
            url_array.append(Phenotype.ddpheno_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return FLOPO BioPortal URL.
    def flopo_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.flopo_id(phenotype, user=user):
            url_array.append(Phenotype.flopo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return FYPO BioPortal URL.
    def fypo_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.fypo_id(phenotype, user=user):
            url_array.append(Phenotype.fypo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return HP BioPortal URL.
    def hp_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.hpo_id(phenotype, user=user):
            url_array.append(Phenotype.hp_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MP BioPortal URL.
    def mp_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.mp_id(phenotype, user=user):
            url_array.append(Phenotype.mp_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MPO BioPortal URL.
    def mpo_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.mpo_id(phenotype, user=user):
            url_array.append(Phenotype.mpo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return OMP BioPortal URL.
    def omp_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.omp_id(phenotype, user=user):
            url_array.append(Phenotype.omp_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return REPO BioPortal URL.
    def repo_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.repo_id(phenotype, user=user):
            url_array.append(Phenotype.repo_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return SPTO BioPortal URL.
    def spto_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.spto_id(phenotype, user=user):
            url_array.append(Phenotype.spto_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return UPHENO BioPortal URL.
    def upheno_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.upheno_id(phenotype, user=user):
            url_array.append(Phenotype.upheno_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return WB-PHENOTYPE BioPortal URL.
    def wbphenotype_bioportal_url(phenotype, user=None):
        url_array = []
        for iden in Phenotype.wbphenotype_id(phenotype, user=user):
            url_array.append(Phenotype.wbphenotype_bioportal_purl + "/" + str(iden))
        return url_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, source="ebi", user=None, taxon=None, search_type=None):
        return search(query, source=source, taxon=taxon, search_type=search_type)
    
    """
        External files
        
    """
        
#   UNIT TESTS
def phenotype_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()