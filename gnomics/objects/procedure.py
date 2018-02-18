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
#   Create instance of a procedure.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.procedure_files.cpt import get_cpt_id
from gnomics.objects.procedure_files.search import search

#   MAIN
def main():
    procedure_unit_tests()

#   PROCEDURE CLASS
class Procedure:
    """
        Procedure class:
        
        A procedure is a course of action intended to 
        achieve a result in the delivery of healthcare.
    """
    
    # CPT BioPortal PURL.
    cpt_bioportal_purl = "http://purl.bioontology.org/ontology/CPT"
    
    # HCPCS BioPortal PURL.
    hcpcs_bioportal_purl = "http://purl.bioontology.org/ontology/HCPCS"
    
    # ICD10PCS BioPortal PURL.
    icd10pcs_bioportal_purl = "http://purl.bioontology.org/ontology/ICD10PCS"
    
    """
        Procedure attributes:
        
        Identifier      = A particular way to identify the
                          procedure in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the procedure.
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
        
        # Initialize dictionary of procedure objects.
        self.procedure_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a procedure.
    def add_identifier(procedure, identifier=None, identifier_type=None, language=None, source=None, name=None):
        procedure.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a procedure.
    def add_object(procedure, obj=None, object_type=None):
        procedure.procedure_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Procedure objects:
        
    """
    
    
        
    """
        Procedure identifiers:
        
        CPT ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(procedure, user=None):
        Procedure.cpt_id(procedure, user=user)
        return procedure.identifiers
    
    # Return CPT ID.
    def cpt_id(procedure, user=None):
        return get_cpt_id(procedure, user=user)
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
    """
    
    def all_properties(procedure, user=None):
        property_dict = {}
        return property_dict
    
    """
        Procedure URLs:
        
    """
    
    # Return links.
    def all_urls(procedure, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None):
        if user is not None:
            return search(query, user)
        else:
            return []
        
    """
        External files
        
    """

#   UNIT TESTS
def procedure_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()