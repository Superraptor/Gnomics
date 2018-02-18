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
#   Create instance of a genotype.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import timeit

#   MAIN
def main():
    genotype_unit_tests()

#   GENOTYPE CLASS
class Genotype:
    """
        Genotype class
        
        A genotype is the part of the genetic makeup of 
        a cell which determines a specific characteristic 
        of that cell, organism, or individual.
    """
    
    # GENO BioPortal PURL.
    geno_bioportal_purl = "http://purl.bioontology.org/ontology/GENO"
    
    """
        Genotype attributes:
        
        Identifier      = A particular way to identify the
                          genotype in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the genotype.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [
                {
                    'identifier': identifier,
                    'language': language,
                    'identifier_type': identifier_type,
                    'source': source,
                    'name': name
                }
            ]
        
        # Initialize dictionary of enzyme objects.
        self.genotype_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a genotype.
    def add_identifier(genotype, identifier = None, identifier_type = None, language = None, source = None, name = None):
        genotype.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Genotype objects
        
    """
    
    
    
    """
        Genotype identifiers
    
    """
    
    # Return all identifiers.
    def all_identifiers(genotype, user = None):
        return genotype.identifiers
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(genotype, user = None):
        property_dict = {}
        return property_dict
    
    """
        Genotype URLs
        
    """
    
    # Return links.
    def all_urls(genotype, user=None):
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
def genotype_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()