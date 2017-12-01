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
#   Create instance of a procedure.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

# Import sub-methods.
from gnomics.objects.procedure_files.search import search

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   PROCEDURE CLASS
class Procedure:
    """
        Procedure class:
        
    """
    
    """
        Procedure attributes:
        
        Identifier      = A particular way to identify the
                          procedure in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the procedure.
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
        
        # Initialize dictionary of procedure objects.
        self.procedure_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a procedure.
    def add_identifier(symptom, identifier = None, identifier_type = None, language = None, source = None, name = None):
        procedure.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a procedure.
    def add_object(procedure, obj = None, object_type = None):
        procedure.procedure_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Procedure objects:
        
    """
    
    
        
    """
        Procedure identifiers:
        
        
    """
    
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
    """
    
    def all_properties(phenotype, user = None):
        property_dict = {}
        return property_dict
    
    """
        Procedure URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None):
        if user is not None:
            return search(query, user)
        else:
            return []
        
    """
        External files
        
    """

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()