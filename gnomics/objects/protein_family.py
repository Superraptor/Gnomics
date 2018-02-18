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
#   Create instance of a protein family.
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
from gnomics.objects.interaction_objects.protein_family_protein import get_proteins

#   MAIN
def main():
    protein_family_unit_tests()

#   PROTEIN FAMILY CLASS
class ProteinFamily():
    """
        Protein family class
        
        A protein family is a group of evolutionarily-related
        proteins.
    """
    
    """
        Protein family attributes:
        
        Identifier      = A particular way to identify the
                          protein family in question. Usually a
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
    
    # Initialize the protein family.
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
        
        # Initialize dictionary of protein family objects.
        self.protein_family_objects = []
        
    # Add an identifier to a protein family.
    def add_identifier(protein_famliy, identifier=None, identifier_type=None, taxon=None, language=None, source=None, name=None):
        protein_family.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Protein family objects:
        
    """
    
        
    """
        Protein family identifiers:
        
        InterPro ID
        Pfam ID
        TIGRFAM ID

    """
    
    # Return all identifiers.
    def all_identifiers(protein_family, user=None):
        return protein_family.identifiers
    
    # Return InterPro ID
    def interpro_id(prot, user=None):
        print("NOT FUNCTIONAL.")
    
    # Return Pfam ID.
    def pfam_id(prot, user=None):
        print("NOT FUNCTIONAL.")
        
    # Return TIGRFAM ID.
    def tigrfam_id(prot, user=None):
        print("NOT FUNCTIONAL.")
    
    """
        Interaction objects:
        
        Proteins
    """
    
    # Return interaction objects.
    def all_interaction_objects(protein_family, user=None):
        interaction_obj = {}
        interaction_obj["Proteins"] = ProteinFamily.proteins(protein_family, user=user)
        return interaction_obj
    
    # Return proteins.
    def proteins(protein_family, user=None):
        return get_proteins(protein_family)
    
    """
        Other properties:
        
    """
    
    def all_properties(protein_family, user=None):
        property_dict = {}
        return property_dict
    
    """
        Protein URLs:
        
    """
    
    # Return links.
    def all_urls(protein_family, user=None):
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
def protein_family_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()