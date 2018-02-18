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
#   Create instance of an enzyme.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.enzyme_files.ec import get_ec_number

#   MAIN
def main():
    enzyme_unit_tests()

#   ENZYME CLASS
class Enzyme:
    """
        Enzyme class
        
        An enzyme is a macromolecular biological catalyst.
    """
    
    """
        Enzyme attributes:
        
        Identifier      = A particular way to identify the
                          enzyme in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the enzyme.
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
        
        # Initialize dictionary of enzyme objects.
        self.enzyme_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a enzyme.
    def add_identifier(enzyme, identifier=None, identifier_type=None, language=None, source=None, name=None):
        enzyme.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Enzyme objects
        
    """
    
    
    
    """
        Enzyme identifiers
    
        EC Number
    """
    
    # Return all identifiers.
    def all_identifiers(enzyme, user=None):
        Enzyme.ec_number(enzyme, user=user)
        return enzyme.identifiers
    
    # Return EC Number.
    def ec_number(enzyme, user=None):
        return get_ec_number(enzyme)
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(enzyme, user=None):
        property_dict = {}
        return property_dict
    
    """
        Enzyme URLs
        
    """
    
    # Return links.
    def all_urls(enzyme, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions
    
        Search
        
    """
    
    def search():
        print("NOT FUNCTIONAL.")
    
    """
        External files
        
    """

#   UNIT TESTS
def enzyme_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()