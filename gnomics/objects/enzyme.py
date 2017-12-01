#
#
#
#
#

#
#   Create instance of an enzyme.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   ENZYME CLASS
class Enzyme:
    """
        Enzyme class
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
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
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
        self.enzyme_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a enzyme.
    def add_identifier(enzyme, identifier = None, identifier_type = None, language = None, source = None, name = None):
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
    
    """
    
    
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(enzyme, user = None):
        property_dict = {}
        return property_dict
    
    """
        Enzyme URLs
        
    """
    
    
    
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

#   MAIN
if __name__ == "__main__": main()