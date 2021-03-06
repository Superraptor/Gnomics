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
#   Create instance of a protein domain.
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
import gnomics.objects.protein

#   Other imports.
import timeit

#   Import sub-methods.

#   Import further methods.

#   MAIN
def main():
    protein_domain_unit_tests()

#   PROTEIN DOMAIN CLASS
class ProteinDomain():
    """
        Protein domaain class
        
        A protein domain is a conserved part of a given
        protein sequence and tertiary structure that
        can evolve, function, and exist independently
        of the rest of the protein chain.
    """
    
    """
        Protein domain attributes:
        
        Identifier      = A particular way to identify the
                          protein domain in question. Usually a
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
    
    # Initialize the protein domain.
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
        
        # Initialize dictionary of protein domain objects.
        self.protein_domain_objects = []
        
    # Add an identifier to a protein domain.
    def add_identifier(protein_famliy, identifier=None, identifier_type=None, taxon=None, language=None, source=None, name=None):
        protein_domain.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Protein domain objects:
        
    """
    
        
    """
        Protein domain identifiers:
        
        CDD ID
        SMART ID
    """
    
    # Return all identifiers.
    def all_identifiers(protein_domain, user=None):
        return protein_domain.identifiers
    
    # Return CDD (Conserved Domain Database) ID.
    def cdd_id(prot, user=None):
        print("NOT FUNCTIONAL.")
        
    # Return SMART (Simple Modular Architecture Research Tool) ID.
    def smart_id(prot, user=None):
        print("NOT FUNCTIONAL.")
    
    """
        Interaction objects:
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(protein_domain, user=None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties:
        
    """
    
    def all_properties(protein_domain, user=None):
        property_dict = {}
        return property_dict
    
    """
        Protein Domain URLs:
        
    """
    
    # Return links.
    def all_urls(protein_domain, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user=None):
        print("NOT FUNCTIONAL.")
        
    """
        External files
        
    """

#   UNIT TESTS
def protein_domain_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()