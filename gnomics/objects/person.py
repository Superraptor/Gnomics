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
#   Create instance of a person.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.person_files.demographics import parse_demographics

#   MAIN
def main():
    person_unit_tests()

#   PERSON CLASS
class Person:
    """
        Person class
        
        A person is a being that has certain capacities or
        attributes such as reason, morality, consciousness,
        or self-consciousness, and being a part of a 
        culturally established form of social relations 
        such as kinship, ownership of property, or legal 
        responsibility.
    """
    
    # Ontology of Medically Related Social Entities 
    # (OMRSE) BioPortal PURL.
    omrse_bioportal_purl = "http://purl.bioontology.org/ontology/OMRSE"
    
    """
        Person attributes:
        
        Identifier      = A particular way to identify the
                          person in question. Usually a 
                          database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the person.
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
        
        # Initialize dictionary of person objects.
        self.person_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a person.
    def add_identifier(person, identifier=None, identifier_type=None, language=None, source=None, name=None):
        person.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Person objects
        
    """
    
    
    
    """
        Person identifiers
    
    """
    
    # Return all identifiers.
    def all_identifiers(person, user=None):
        return person.identifiers
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    # Return all properties.
    def all_properties(person, user=None):
        property_dict = {}
        return property_dict
    
    """
        Person URLs
        
    """
    
    # Return links.
    def all_urls(person, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions
    
        Parse demographic information
        Search
        
    """
    
    # Return parsed demographic information.
    def parse_demographics(raw_string):
        return parse_demographics(raw_string)
    
    # Search for people.
    def search():
        print("NOT FUNCTIONAL.")
    
    """
        External files
        
    """

#   UNIT TESTS
def person_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()