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
#   Create instance of a cellular component.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   CELLULAR COMPONENT CLASS
class CellularComponent:
    """
        Cellular component class
        
        Cellular components are unique, highly
        organized substances of which cells and
        living organisms are composed.
    """
    
    """
        Cellular component attributes:
        
        Identifier      = A particular way to identify the
                          cellular component in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the cellular component.
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
        
        # Initialize dictionary of cellular comonent objects.
        self.cellular_component_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a cellular_component.
    def add_identifier(cellular_component, identifier = None, identifier_type = None, language = None, source = None, name = None):
        cellular_component.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Cellular component objects
        
    """
    
    
    
    """
        Cellular component identifiers
    
    """
    
    
    
    """
        Interaction objects
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(cellular_component, user = None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties
        
    """
    
    def all_properties(cellular_component, user = None):
        property_dict = {}
        return property_dict
    
    """
        Cellular component URLs
        
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