#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       PYMEDTERMINO:
#           http://pythonhosted.org/PyMedTermino/

#
#   Create instance of a disease.
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
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
import json
import requests
import wikipedia

#   Import sub-methods
from gnomics.objects.disease_files.diseasesdb import get_diseasesdb_id
from gnomics.objects.disease_files.doid import get_doid, get_do_synonyms
from gnomics.objects.disease_files.emedicine import get_emedicine_id
from gnomics.objects.disease_files.freebase import get_freebase_id
from gnomics.objects.disease_files.gnd import get_gnd_id
from gnomics.objects.disease_files.icd10 import get_icd10, get_icd_10_disease
from gnomics.objects.disease_files.icd9 import get_icd9
from gnomics.objects.disease_files.internetmedicinse import get_internetmedicin_se_id
from gnomics.objects.disease_files.jstor import get_jstor_topic_id
from gnomics.objects.disease_files.kegg import get_kegg_disease_id, get_kegg_disease
from gnomics.objects.disease_files.meddra import get_meddra_id
from gnomics.objects.disease_files.medlineplus import get_medlineplus_id
from gnomics.objects.disease_files.mesh import get_mesh
from gnomics.objects.disease_files.mondo import get_mondo_id
from gnomics.objects.disease_files.nci import get_nci_thesaurus_code
from gnomics.objects.disease_files.ndl import get_ndl_auth_id
from gnomics.objects.disease_files.omim import get_omim, get_omim_disease
from gnomics.objects.disease_files.ordo import get_ordo
from gnomics.objects.disease_files.patientplus import get_patientplus_id
from gnomics.objects.disease_files.quora import get_quora_topic_id
from gnomics.objects.disease_files.search import search
from gnomics.objects.disease_files.snomed import get_snomed
from gnomics.objects.disease_files.umls import get_umls, get_umls_terms
from gnomics.objects.disease_files.wiki import get_english_wikipedia_accession, get_wikidata_object, get_wikidata_accession, get_wikidata_synonyms

#   Import further methods.
from gnomics.objects.interaction_objects.disease_compound import get_compounds
from gnomics.objects.interaction_objects.disease_gene import get_genes
from gnomics.objects.interaction_objects.disease_patent import get_patents
from gnomics.objects.interaction_objects.disease_pathway import get_pathways
from gnomics.objects.interaction_objects.disease_phenotype import get_phenotypes
from gnomics.objects.interaction_objects.disease_reference import get_references

#   MAIN
def main():
    disease_unit_tests()

#   DISEASE CLASS
class Disease:
    """
        Disease class
        
        Representing diseases, which 
        (according to the Encyclopedia Britannica) are
        "any harmful deviation[s] from the normal structural 
        or functional state of an organism, generally 
        associated with certain signs and symptoms and 
        differing in nature from physical injury."
    """
    
    # DOID BioPortal PURL.
    doid_bioportal_purl = "http://purl.bioontology.org/ontology/DOID"
    
    # ICD9CM BioPortal PURL.
    icd9cm_bioportal_purl = "http://purl.bioontology.org/ontology/ICD9CM"
    
    # ICD10CM BioPortal PURL.
    icd10cm_bioportal_purl = "http://purl.bioontology.org/ontology/ICD10CM"
    
    # MEDDRA BioPortal PURL.
    meddra_bioportal_purl = "http://purl.bioontology.org/ontology/MEDDRA"
    
    # MESH BioPortal PURL.
    mesh_bioportal_purl = "http://purl.bioontology.org/ontology/MESH"
    
    # MONDO BioPortal PURL.
    mondo_bioportal_purl = "http://purl.bioontology.org/ontology/MONDO"
    
    # NCIT BioPortal PURL.
    ncit_bioportal_purl = "http://purl.bioontology.org/ontology/NCIT"
    
    # OMIM BioPortal PURL.
    omim_bioportal_purl = "http://purl.bioontology.org/ontology/OMIM"
    
    # ORDO BioPortal PURL.
    ordo_bioportal_purl = "http://purl.bioontology.org/ontology/ORDO"
    
    # SNOMED CT BioPortal PURL.
    snomed_ct_bioportal_purl = "http://purl.bioontology.org/ontology/SNOMEDCT"
    
    """
        Disease attributes:
        
        Identifier      = A particular way to identify the
                          disease in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the disease.
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of disease objects.
        self.disease_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a disease.
    def add_identifier(dis, identifier=None, identifier_type=None, language=None, source=None, name=None):
        dis.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a disease.
    def add_object(disease, obj=None, object_type=None):
        disease.disease_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    # Merge two disease objects if there is overlap in their identifier list.
    def merge(dis1, dis2):
        matches = 0
        for iden1 in dis1.identifiers:
            for iden2 in dis2.identifiers:
                if iden1["identifier"] == iden2["identifier"]:
                    matches += 1
        
        if matches > 0:
            new_id_list = dis1.identifiers
            new_id_list.extend(dis2.identifiers)

            final_id_list = []
            final_name_list = []
            final_obj_list = []
            for iden in new_id_list:
                if (iden["identifier"] not in final_id_list) or (iden["name"] not in final_name_list):
                    final_obj_list.append(iden)
                    final_id_list.append(iden["identifier"])
                    final_name_list.append(iden["name"])
                    
            dis3 = Disease(identifier = final_obj_list[0]["identifier"], identifier_type = final_obj_list[0]["identifier_type"], language = final_obj_list[0]["language"], source = final_obj_list[0]["source"], name = final_obj_list[0]["name"])
            final_obj_list.pop(0)
            for iden_obj in final_obj_list:
                Disease.add_identifier(dis3, identifier = iden_obj["identifier"], identifier_type = iden_obj["identifier_type"], language = iden_obj["language"], source = iden_obj["source"], name = iden_obj["name"])
                
            return dis3
                    
        else:
            return
        
    """
        Disease objects
        
        ICD-10 Disease
        KEGG DISEASE
        OMIM Disease
        Wikidata Object
    """
    
    # Return ICD-10 disease object.
    def icd_10_disease(dis, user=None):
        return get_icd_10_disease(dis)
        
    # Return KEGG disease object.
    def kegg_disease(dis, user=None):
        return get_kegg_disease(dis)
    
    # Return OMIM disease object.
    def omim_disease(dis, user=None):
        return get_omim_disease(dis, user=user)
    
    # Get Wikidata object.
    def wikidata(dis, user=None):
        return get_wikidata_object(dis)
        
    """
        Disease identifiers
        
        DiseasesDB ID
        DOID
        eMedicine ID
        Freebase ID
        GND ID
        ICD-10-CM
        ICD-9-CM
        internetmedicin.se ID
        JSTOR Topic ID
        KEGG DISEASE ID
        MedDRA ID
        MedlinePlus ID
        MESH UID
        MIM Number
        MONDO ID
        NCI Thesaurus Code
        NDL Auth ID
        ORDO ID
        PatientPlus ID
        Quora Topic ID
        SNOMED-CT ID
        UMLS CUI
        UMLS Term
        Wikidata Accession
        Wikipedia Accession (English)
        
    """
    
    # Return all identifiers.
    def all_identifiers(disease, user=None):
        Disease.diseasesdb_id(disease, user=user)
        Disease.doid(disease, user=user)
        Disease.do_synonyms(disease, user=user)
        Disease.emedicine_id(disease, user=user)
        Disease.freebase_id(disease, user=user)
        Disease.gnd_id(disease, user=user)
        Disease.icd_10(disease, user=user)
        Disease.icd_9(disease, user=user)
        Disease.internetmedicin_se_id(disease, user=user)
        Disease.jstor_topic_id(disease, user=user)
        Disease.kegg_disease_id(disease, user=user)
        Disease.meddra_id(disease, user=user)
        Disease.medlineplus_id(disease, user=user)
        Disease.mesh(disease, user=user)
        Disease.mim_number(disease, user=user)
        Disease.mondo_id(disease, user=user)
        Disease.nci_thesaurus_code(disease, user=user)
        Disease.ndl_auth_id(disease, user=user)
        Disease.omim(disease, user=user)
        Disease.ordo_id(disease, user=user)
        Disease.patientplus_id(disease, user=user)
        Disease.quora_topic_id(disease, user=user)
        Disease.snomed_ct_id(disease, user=user)
        Disease.umls_cui(disease, user=user)
        Disease.umls_terms(disease, user=user)
        Disease.wikidata_accession(disease, user=user)
        Disease.wikidata_synonyms(disease, language="en", user=user)
        Disease.wikipedia_accession(disease, language="en", user=user)
        return disease.identifiers
    
    # Return DiseasesDB ID.
    def diseasesdb_id(dis, user=None):
        return get_diseasesdb_id(dis)
    
    # Return DOID.
    def doid(dis, user=None):
        return get_doid(dis)
    
    # Return DO synonyms.
    def do_synonyms(dis, user=None):
        return get_do_synonyms(dis)
    
    # Return eMedicine ID.
    def emedicine_id(dis, user=None):
        return get_emedicine_id(dis)
    
    # Return Freebase ID.
    def freebase_id(dis, user=None):
        return get_freebase_id(dis)
            
    # Return GND ID.
    def gnd_id(dis, user=None):
        return get_gnd_id(dis)
        
    # Return ICD-10 codes.
    def icd_10(dis, user=None):
        return get_icd10(dis)
    
    # Return ICD-9 codes.
    def icd_9(dis, user=None):
        return get_icd9(dis)
    
    # Return internetmedicin.se ID.
    def internetmedicin_se_id(dis, user=None):
        return get_internetmedicin_se_id(dis)

    # Return JSTOR Topic ID.
    def jstor_topic_id(dis, user=None):
        return get_jstor_topic_id(dis)
    
    # Return KEGG disease identifier.
    def kegg_disease_id(dis, user=None):
        return get_kegg_disease_id(dis)
    
    # Return MedDRA ID.
    def meddra_id(dis, user=None):
        return get_meddra_id(dis)
    
    # Return MedlinePlus ID.
    def medlineplus_id(dis, user=None):
        return get_medlineplus_id(dis)
    
    # Return MeSH codes.
    def mesh(dis, user=None):
        return get_mesh(dis)
    
    # Return MIM number.
    def mim_number(dis, user=None):
        return get_omim(dis)
    
    # Return MONDO ID.
    def mondo_id(dis, user=None):
        return get_mondo_id(dis)
    
    def nci_thesaurus_code(dis, user=None):
        return get_nci_thesaurus_code(dis)
    
    # Return NDL Auth ID.
    def ndl_auth_id(dis, user=None):
        return get_ndl_auth_id(dis)
    
    # Return MIM Number.
    def omim(dis, user=None):
        return get_omim(dis)
    
    # Return ORDO ID.
    def ordo_id(dis, user=None):
        return get_ordo(dis)
    
    # Return PatientPlus ID.
    def patientplus_id(dis, user=None):
        return get_patientplus_id(dis)
    
    # Return Quora Topic ID.
    def quora_topic_id(dis, user=None):
        return get_quora_topic_id(dis)
    
    # Return SNOMED-CT ID.
    def snomed_ct_id(dis, user=None):
        return get_snomed(dis)
    
    # Return UMLS CUI.
    def umls_cui(dis, user=None):
        return get_umls(dis)
    
    # Return UMLS Terms.
    def umls_terms(dis, user=None):
        return get_umls_terms(dis)
    
    # Return Wikidata Accession.
    def wikidata_accession(dis, user=None):
        return get_wikidata_accession(dis)
    
    # Return Wikidata Synonyms.
    def wikidata_synonyms(dis, language = "all", user=None):
        return get_wikidata_synonyms(dis, language=language)
    
    # Return Wikipedia Accession.
    def wikipedia_accession(dis, language="en", user=None):
        if language.lower() in ["en", "eng", "english", "all"]:
            return get_english_wikipedia_accession(dis)
        else:
            print("The provided language (%s) is not currently supported." % language)
    
    """
        Interaction objects:
        
        Compounds
        Drugs
        Genes
        Patents
        Pathways
        Phenotypes
        References
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(disease, user=None):
        interaction_obj = {}
        interaction_obj["Compounds"] = Disease.compounds(disease, user=user)
        interaction_obj["Genes"] = Disease.genes(disease, user=user)
        interaction_obj["Patents"] = Disease.patents(disease, user=user)
        interaction_obj["Pathways"] = Disease.pathways(disease, user=user)
        interaction_obj["Phenotypes"] = Disease.phenotypes(disease, user=user)
        interaction_obj["References"] = Disease.references(disease, user=user)
        return interaction_obj
    
    # Return compounds.
    def compounds(dis, user=None):
        return get_compounds(dis)
    
    # Return disease drugs.
        # Move to disease_drug.py
    def drugs(dis, user=None):
        print("NOT FUNCTIONAL.")
        # TODO: Figure out where to put this???
        return Disease.kegg_disease(dis)["DRUG"]
    
    # Return genes.
    def genes(dis, user=None):
        return get_genes(dis, user=user)
    
    # Return phenotypes.
    def patents(dis, user=None):
        return get_patents(dis, user=user)
    
    # Return pathways.
    #
    # Note that only inferred pathways will be returned.
    def pathways(dis, user=None):
        return get_pathways(dis, user=user)
    
    # Return phenotypes.
    def phenotypes(dis, user=None):
        return get_phenotypes(dis)
        
    # Return references.
    def references(dis, user=None):
        return get_references(dis, user=user)
    
    """
        Other properties:
        
        ## TODO: Figure out properties?? ##
        
        Category
        Description
        Parents (ICD-10-CM)
        Ancestors (ICD-10-CM)
        Relations (ICD-10-CM)
        Inclusions (ICD-10-CM)
        Exclusions (ICD-10-CM)
        
    """
    
    def all_properties(disease, user=None):
        property_dict = {}
        return property_dict
    
    # Return disease category.
    def category(dis, user=None):
        print("NOT FUNCTIONAL.")
        return Disease.kegg_disease(dis)["CATEGORY"]

    # Return description.
    def description(dis, user=None):
        return Disease.kegg_disease(dis)["DESCRIPTION"]
        
    # Return parents of an ICD-10 code.
    def icd_10_parents(disease, icd_10_code, user=None):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].parents
        
    # Return the ancestors of an ICD-10 code.
    def icd_10_ancestors(disease, icd_10_code, user=None):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].ancestors()
            
    # Return relations.
    def icd_10_relations(disease, icd_10_code, user=None):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].relations
    
    # Return inclusions.
    def icd_10_exclusion(disease, icd_10_code, user=None):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].exclusion
    
    # Return exclusions.
    def icd_10_inclusion(disease, icd_10_code, user=None):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].inclusion
            
    # Returns Wikipedia content.
    def wikipedia_content(disease, user=None, language="en"):
        wiki_array = []
        if Disease.wikipedia_page(disease, user=user, language=language) is not None and Disease.wikipedia_page(disease, user=user, language=language) != "":
            for x in Disease.wikipedia_page(disease, user=user, language=language):
                wiki_array.append(x.content)
        return wiki_array
    
    # Returns Wikipedia links.
    def wikipedia_links(disease, user=None):
        wiki_array = []
        if Disease.wikipedia_page(disease, user=user, language=language) is not None and Disease.wikipedia_page(disease, user=user, language=language) != "":
            for x in Disease.wikipedia_page(disease, user=user, language=language):
                wiki_array.append(x.links)
        return wiki_array
        
    # Returns Wikipedia page.
    def wikipedia_page(disease, user=None, language="en"):
        wiki_array = []
        if Disease.wikipedia_accession(disease, user=user, language=language) is not None and Disease.wikipedia_accession(disease, user=user, language=language) != "":
            for x in Disease.wikipedia_accession(disease, user=user, language=language):
                wiki_array.append(wikipedia.page(x))
        return wiki_array
    
    # Returns Wikipedia page title.
    def wikipedia_title(disease, user=None):
        wiki_array = []
        if Disease.wikipedia_page(disease, user=user, language=language) is not None and Disease.wikipedia_page(disease, user=user, language=language) != "":
            for x in Disease.wikipedia_page(disease, user=user, language=language):
                wiki_array.append(x.title)
        return wiki_array
            
    """
        Disease URLs.
        
        MeSH URL
        
    """
    
    # Return links.
    def all_urls(disease, user=None):
        url_dict = {}
        return url_dict
    
    # Return MeSH link.
    def mesh_url(disease, mesh_uid, user=None):
        print("NOT FUNCTIONAL.")
        base_url = "https://meshb.nlm.nih.gov/record/ui?ui="
        return base_url + mesh_uid
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Return search.
    #
    # Most of the parameters originate from OMIM search, as
    # can be seen here:
    # https://www.omim.org/help/api
    def search(query, search_type=None, user=None, source="omim", filter_type=None, fields_type=None, sort_type=None, operator_type=None, start=0, limit=10, retrieve=None, format_param="jsonp"):
        return search(query, search_type = search_type, user = user, source = source, filter_type = filter_type, fields_type = fields_type, sort_type = sort_type, operator_type = operator_type, start = start, limit = limit, retrieve = retrieve, format_param = format_param)
    
    """
        External files:
        
        Images
    """
    
    # Return images.
    def images(disease, user=None):
        image_array = []
        return image_array
    
#   UNIT TESTS
def disease_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()