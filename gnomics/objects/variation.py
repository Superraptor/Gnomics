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
#   Create instance of a variation.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   VARIATION CLASS
class Variation:
    """
        Variation class:
        
    """
    
    """
        Variation attributes:
        
        Identifier      = A particular way to identify the
                          variation in question. Usually a 
                          database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the variation.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of variation objects.
        self.variation_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a variation.
    def add_identifier(variation, identifier = None, identifier_type = None, language = None, source = None, name = None):
        variation.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a variation.
    def add_object(variation, obj = None, object_type = None):
        variation.variation_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Variation objects:
        
        
    """
    
    
        
    """
        Variation identifiers:
        
        RSID
    """
    
    
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
        
    """
    
    def all_properties(molecular_function, user = None):
        property_dict = {}
        return property_dict
    
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