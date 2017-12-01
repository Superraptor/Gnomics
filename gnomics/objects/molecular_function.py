#
#
#
#
#

#
#   Create instance of a molecular function.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   MOLECULAR FUNCTION CLASS
class MolecularFunction:
    """
        Molecular function class
    """
    
    """
        Molecular function attributes:
        
        Identifier      = A particular way to identify the
                          molecular function in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the molecular function.
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
        
        # Initialize dictionary of molecular function objects.
        self.molecular_function_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a molecular function.
    def add_identifier(molecular_function, identifier = None, identifier_type = None, language = None, source = None, name = None):
        molecular_function.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Molecular function objects
        
    """
    
    
    
    """
        Molecular function identifiers
    
    """
    
    
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(molecular_function, user = None):
        property_dict = {}
        return property_dict
    
    """
        Molecular function URLs
        
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