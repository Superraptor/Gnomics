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

#   Other imports.
import json
import requests
import sys

#   Import sub-methods
from gnomics.objects.disease_files.icd10 import get_icd10, get_icd_10_disease
from gnomics.objects.disease_files.icd9 import get_icd9
from gnomics.objects.disease_files.kegg import get_kegg_disease_id, get_kegg_disease
from gnomics.objects.disease_files.mesh import get_mesh
from gnomics.objects.disease_files.nci import get_nci_thesaurus_code
from gnomics.objects.disease_files.omim import get_omim, get_omim_disease
from gnomics.objects.disease_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.disease_compound import get_compounds
from gnomics.objects.interaction_objects.disease_gene import get_genes
from gnomics.objects.interaction_objects.disease_patent import get_patents
from gnomics.objects.interaction_objects.disease_pathway import get_pathways
from gnomics.objects.interaction_objects.disease_phenotype import get_phenotypes
from gnomics.objects.interaction_objects.disease_reference import get_references

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

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
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of disease objects.
        self.disease_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a disease.
    def add_identifier(dis, identifier = None, identifier_type = None, language = None, source = None, name = None):
        dis.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Disease objects
        
        ICD-10 Disease
        KEGG DISEASE
        OMIM Disease
    """
    
    # Return ICD-10 disease object.
    def icd_10_disease(dis):
        return get_icd_10_disease(dis)
        
    # Return KEGG disease object.
    def kegg_disease(dis):
        return get_kegg_disease(dis)
    
    # Return OMIM disease object.
    def omim_disease(dis, user = None):
        return get_omim_disease(dis, user)
        
    """
        Disease identifiers
        
        ICD-10-CM
        ICD-9-CM
        KEGG DISEASE ID
        MESH UID
        MIM Number
        NCI Thesaurus Code
        ORDO ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(disease, user = None):
        Disease.icd_10(disease)
        Disease.icd_9(disease)
        Disease.kegg_disease_id(disease)
        Disease.nci_thesaurus_code(disease)
        return disease.identifiers
            
    # Return ICD-10 codes.
    def icd_10(dis):
        return get_icd10(dis)
    
    # Return ICD-9 codes.
    def icd_9(dis):
        return get_icd9(dis)
    
    # Return KEGG disease identifier.
    def kegg_disease_id(dis):
        return get_kegg_disease_id(dis)
    
    # Return MeSH codes.
    def mesh(dis):
        return get_mesh(dis)
    
    def nci_thesaurus_code(dis):
        return get_nci_thesaurus_code(dis)
    
    # Return OMIM identifiers.
    def omim(dis):
        return get_omim(dis)
    
    # Return ORDO ID.
    def ordo(dis):
        return get_ordo(dis)
    
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
    def all_interaction_objects(disease, user = None):
        interaction_obj = {}
        interaction_obj["Compounds"] = Disease.compounds(disease)
        interaction_obj["Genes"] = Disease.genes(disease)
        #interaction_obj["Patents"] = Disease.patents(disease)
        interaction_obj["Pathways"] = Disease.pathways(disease)
        interaction_obj["Phenotypes"] = Disease.phenotypes(disease)
        #interaction_obj["References"] = Disease.references(disease)
        print(interaction_obj)
        return interaction_obj
    
    # Return compounds.
    def compounds(dis):
        return get_compounds(dis)
    
    # Return disease drugs.
    def drugs(dis):
        print("NOT FUNCTIONAL.")
        # TODO: Figure out where to put this???
        return Disease.kegg_disease(dis)["DRUG"]
    
    # Return genes.
    def genes(dis):
        return get_genes(dis)
    
    # Return phenotypes.
    def patents(dis):
        return get_patents(dis)
    
    # Return pathways.
    #
    # Note that only inferred pathways will be returned.
    def pathways(dis):
        return get_pathways(dis)
    
    # Return phenotypes.
    def phenotypes(dis):
        return get_phenotypes(dis)
        
    # Return references.
    def references(dis):
        return get_references(dis)
    
    """
        Other properties:
        
        Category
        Description
        Parents (ICD-10-CM)
        Ancestors (ICD-10-CM)
        Relations (ICD-10-CM)
        Inclusions (ICD-10-CM)
        Exclusions (ICD-10-CM)
        
    """
    
    def all_properties(disease, user = None):
        property_dict = {}
        return property_dict
    
    # Return disease category.
    def category(dis):
        print("NOT FUNCTIONAL.")
        return Disease.kegg_disease(dis)["CATEGORY"]

    # Return description.
    def description(dis):
        return Disease.kegg_disease(dis)["DESCRIPTION"]
        
    # Return parents of an ICD-10 code.
    def icd_10_parents(disease, icd_10_code):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].parents
        
    # Return the ancestors of an ICD-10 code.
    def icd_10_ancestors(disease, icd_10_code):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].ancestors()
            
    # Return relations.
    def icd_10_relations(disease, icd_10_code):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].relations
    
    # Return inclusions.
    def icd_10_exclusion(disease, icd_10_code):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].exclusion
    
    # Return exclusions.
    def icd_10_inclusion(disease, icd_10_code):
        print("NOT FUNCTIONAL.")
        for obj in self.icd_10_disease:
            if obj['object_identifier'] == icd_10_code and (obj['object_type'].lower() == "icd-10" or obj['object_type'].lower() == "icd-10 code"):    
                return ICD10[icd_10_code].inclusion
            
    """
        Disease URLs.
        
        MeSH URL
        
    """
    
    # Return MeSH link.
    def mesh_url(disease, mesh_uid):
        print("NOT FUNCTIONAL.")
        base_url = "https://meshb.nlm.nih.gov/record/ui?ui="
        return base_url + mesh_uid
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # TODO: Move to 'search.py' in disease_files
    #
    # Return search.
    #
    # Most of the parameters originate from OMIM search, as
    # can be seen here:
    # https://www.omim.org/help/api
    #
    def search(query, search_type = None, user = None, source = "omim", filter_type = None, fields_type = None, sort_type = None, operator_type = None, start = 0, limit = 10, retrieve = None, format_param = "jsonp"):
        return search(query, search_type = search_type, user = user, source = source, filter_type = filter_type, fields_type = fields_type, sort_type = sort_type, operator_type = operator_type, start = start, limit = limit, retrieve = retrieve, format_param = format_param)
    
    """
        External files:
        
        Images
    """
    
    # Return images.
    def images(disease):
        image_array = []
        return image_array
    
#   UNIT TESTS
def disease_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()