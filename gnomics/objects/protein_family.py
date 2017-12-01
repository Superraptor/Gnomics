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

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   PROTEIN FAMILY CLASS
class ProteinFamily():
    """
        Protein family class
        
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
    def __init__(self, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'taxon': taxon,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of protein family objects.
        self.protein_family_objects = []
        
    # Add an identifier to a protein family.
    def add_identifier(protein_famliy, identifier = None, identifier_type = None, taxon = None, language = None, source = None, name = None):
        
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
        
        Pfam ID
        TIGRFAM ID

    """
    
    # Return Pfam ID.
    def pfam_id(prot):
        print("NOT FUNCTIONAL.")
        
    # Return TIGRFAM ID.
    def tigrfam_id(prot):
        print("NOT FUNCTIONAL.")
    
    """
        Interaction objects:
        
    """
    
    
    """
        Other properties:
        
    """
    
    def all_properties(protein_family, user = None):
        property_dict = {}
        return property_dict
    
    """
        Protein URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query):
        print("NOT FUNCTIONAL.")
        
    """
        External files
        
    """

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()