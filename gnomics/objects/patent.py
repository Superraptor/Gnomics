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
#   Create instance of a patent.
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

#   Other imports.
import timeit

#   Import sub-methods.

#   MAIN
def main():
    patent_unit_tests()

#   PATENT CLASS
class Patent:
    """
        Patent class
        
        A patent is a set of exclusive rights granted by a
        sovereign state to an inventor or assignee for a 
        limited period of time in exchange for detailed 
        public disclosure of an invention.
    """
    
    """
        Patent attributes:
        
        Identifier      = A particular way to identify the
                          patent in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
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
        
        # Initialize dictionary of patent objects.
        self.patent_objects = []
        
    # Add an identifier to a patent.
    def add_identifier(patent, identifier=None, identifier_type=None, language=None, source=None, name=None):
        patent.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Patent objects
        
    """
    
    

    """
        Patent identifiers:
        
        Patent ID
    """
    
    # Return all identifiers.
    def all_identifiers(patent, user=None):
        Patent.patent_id(patent, user=user)
        return patent.identifiers
    
    # Returns Patent ID.
    def patent_id(patent, user=None):
        return get_patent_id(patent)
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(patent, user=None):
        property_dict = {}
        return property_dict
    
    """
        Patent URLs
        
    """
    
    # Return links.
    def all_urls(patent, user=None):
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
def patent_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()