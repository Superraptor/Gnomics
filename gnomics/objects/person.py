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
#   Create instance of a person.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   PERSON CLASS
class Person:
    """
        Person class
    """
    
    """
        Person attributes:
        
        Identifier      = A particular way to identify the
                          person in question. Usually a 
                          database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the person.
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
        
        # Initialize dictionary of person objects.
        self.person_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a person.
    def add_identifier(person, identifier = None, identifier_type = None, language = None, source = None, name = None):
        person.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Person objects
        
    """
    
    
    
    """
        Person identifiers
    
    """
    
    
    
    """
        Interaction objects
        
    """
    
    
    
    """
        Other properties
        
    """
    
    def all_properties(person, user = None):
        property_dict = {}
        return property_dict
    
    """
        Person URLs
        
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