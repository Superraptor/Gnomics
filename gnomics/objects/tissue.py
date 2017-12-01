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
#   Create instance of a tissue.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.tissue_files.bto import get_bto_id
from gnomics.objects.tissue_files.caloha import get_caloha_id, get_caloha_obj
from gnomics.objects.tissue_files.fma import get_fma_id
from gnomics.objects.tissue_files.mesh import get_mesh_uid
from gnomics.objects.tissue_files.uberon import get_uberon_id, get_uberon_term

#   Import further methods.
from gnomics.objects.interaction_objects.tissue_protein import get_proteins

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   TISSUE CLASS
class Tissue:
    """
        Tissue class:
        
    """
    
    """
        Tissue attributes:
        
        Identifier      = A particular way to identify the
                          tissue in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the tissue.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [
                {
                    'identifier': str(identifier),
                    'language': language,
                    'identifier_type': identifier_type,
                    'source': source,
                    'name': name
                }
            ]
        
        # Initialize dictionary of tissue objects.
        self.tissue_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a tissue.
    def add_identifier(tissue, identifier = None, identifier_type = None, language = None, source = None, name = None):
        tissue.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a tissue.
    def add_object(tissue, obj = None, object_type = None):
        tissue.tissue_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Tissue objects:
        
        CALOHA object
        
    """
    
    # Get CALOHA object.
    def caloha_obj(tissue, user = None):
        return get_caloha_obj(tissue, user = user)
        
    """
        Tissue identifiers:
        
        BTO ID
        CALOHA ID
        FMA ID
        MeSH UID
        UBERON ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(tissue, user = None):
        Tissue.bto_id(tissue, user = user)
        Tissue.caloha_id(tissue, user = user)
        Tissue.fma_id(tissue, user = user)
        Tissue.mesh_uid(tissue, user = user)
        Tissue.uberon_id(tissue, user = user)
        Tissue.uberon_term(tissue, user = user)
        return tissue.identifiers
    
    # Get BTO ID.
    def bto_id(tissue, user = None):
        return get_bto_id(tissue, user = user)
    
    # Get CALOHA ID.
    def caloha_id(tissue, user = None):
        return get_caloha_id(tissue, user = user)
    
    # Get FMA ID.
    def fma_id(tissue, user = None):
        return get_fma_id(tissue, user = user)
    
    # Get MeSH UID.
    def mesh_uid(tissue, user = None):
        return get_mesh_uid(tissue, user = user)
    
    # Get UBERON ID.
    def uberon_id(tissue, user = None):
        return get_uberon_id(tissue, user = user)
    
    # Get UBERON Term.
    def uberon_term(tissue, user = None):
        return get_uberon_term(tissue, user = user)
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
        Definition
    """
    
    def all_properties(tissue, user = None):
        property_dict = {}
        return property_dict
    
    # Get definition.
    def definition(tissue, user = None):
        print("NOT FUNCTIONAL.")
    
    """
        URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query):
        print("NOT FUNCTIONAL.")

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()