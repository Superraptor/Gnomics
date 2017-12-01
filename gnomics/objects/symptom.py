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
#   Create instance of a symptom.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.symptom_files.search import search

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   SYMPTOM CLASS
class Symptom:
    """
        Symptom class:
        
    """
    
    """
        Symptom attributes:
        
        Identifier      = A particular way to identify the
                          symptom in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the symptom.
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
        
        # Initialize dictionary of symptom objects.
        self.symptom_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a symptom.
    def add_identifier(symptom, identifier = None, identifier_type = None, language = None, source = None, name = None):
        symptom.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a symptom.
    def add_object(symptom, obj = None, object_type = None):
        symptom.symptom_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Symptom objects:
        
    """
    
    
        
    """
        Symptom identifiers:
        
    """
    
    
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
        
        
    """
    
    def all_properties(symptom, user = None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None):
        return search(query)

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()