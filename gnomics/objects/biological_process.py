#
#
#
#
#

#
#   Create instance of a biological process.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   BIOLOGICAL PROCESS CLASS
class BiologicalProcess:
    """
        Biological process class
        
        Biological processes are the processes
        vital for a living organism to live.
    """
    
    """
        Biological process attributes:
        
        Identifier      = A particular way to identify the
                          biological process in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the biological process.
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
        
        # Initialize dictionary of biological process objects.
        self.molecular_function_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a biological process.
    def add_identifier(biological_process, identifier = None, identifier_type = None, language = None, source = None, name = None):
        biological_process.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Biological process objects
        
    """
    
    
    
    """
        Biological process identifiers
    
    """
    
    
    
    """
        Interaction objects
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(biological_process, user = None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties
        
    """
    
    def all_properties(biological_process, user = None):
        property_dict = {}
        return property_dict
    
    """
        Biological process URLs
        
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