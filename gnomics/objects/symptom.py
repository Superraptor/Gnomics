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
#   Create instance of a symptom.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.symptom_files.search import search
from gnomics.objects.symptom_files.symp import get_symp_id
from gnomics.objects.symptom_files.wiki import get_wikidata_object, get_wikidata_accession

#   Other imports.
import timeit

#   MAIN
def main():
    symptom_unit_tests()

#   SYMPTOM CLASS
class Symptom:
    """
        Symptom class:
        
        A symptom is a departure from normal function or
        feeling which is noticed by a patient, typically
        reflecting the presence of an unusual state, 
        disorder, or disease.
    """
    
    # CSSO BioPortal PURL.
    csso_bioportal_purl = "http://purl.bioontology.org/ontology/CSSO"
    
    # SYMP BioPortal PURL.
    symp_bioportal_purl = "http://purl.bioontology.org/ontology/SYMP"
    
    """
        Symptom attributes:
        
        Identifier      = A particular way to identify the
                          symptom in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the symptom.
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of symptom objects.
        self.symptom_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a symptom.
    def add_identifier(symptom, identifier=None, identifier_type=None, language=None, source=None, name=None):
        symptom.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a symptom.
    def add_object(symptom, obj=None, object_type=None):
        symptom.symptom_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Symptom objects:
        
        Wikidata Object
        
    """
    
    # Return Wikidata object.
    def wikidata(symptom, user=None):
        return get_wikidata_object(symptom)
        
    """
        Symptom identifiers:
        
        SYMP ID
        Wikidata Accession
        
    """
    
    # Return all identifiers.
    def all_identifiers(symptom, user=None):
        Symptom.symp_id(symptom, user=user)
        Symptom.wikidata_accession(symptom, user=user)
        return symptom.identifiers
    
    # Return SYMP ID.
    def symp_id(symptom, user=None):
        return get_symp_id(symptom)
    
    # Return Wikidata Accession.
    def wikidata_accession(symptom, user=None):
        return get_wikidata_accession(symptom)
    
    """
        Interaction objects:
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(symptom, user=None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties:
        
    """
    
    # Return all properties.
    def all_properties(symptom, user=None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
        SYMP BioPortal
    """
    
    # Return links.
    def all_urls(symptom, user=None):
        url_dict = {}
        url_dict["SYMP BioPortal"] = Symptom.symp_bioportal_url(symptom, user=user)
        return url_dict
    
    # Return SYMP BioPortal URL.
    def symp_bioportal_url(symptom, user=None):
        url_array = []
        for iden in Symptom.symp_id(symptom, user=user):
            url_array.append(Symptom.symp_bioportal_purl + "/" + str(iden))
        return url_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user=None):
        return search(query)

#   UNIT TESTS
def symptom_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()