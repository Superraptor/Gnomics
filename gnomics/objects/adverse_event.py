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
#   Create instance of an adverse event.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.adverse_event_files.meddra import get_meddra_id, get_meddra_term
from gnomics.objects.adverse_event_files.mesh import get_mesh_uid
from gnomics.objects.adverse_event_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.adverse_event_phenotype import get_phenotypes

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   ADVERSE EVENT CLASS
class AdverseEvent:
    """
        Adverse event class:
        
        According to the U.S. Food & Drug Administration
        (FDA) an adverse event (AE) is "any undesirable
        experience associated with the use of a medical
        product in a patient."
    """
    
    """
        Adverse event attributes:
        
        Identifier      = A particular way to identify the
                          adverse event in question. Usually a database unique identifier, but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the adverse event.
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
        
        # Initialize dictionary of adverse event objects.
        self.adverse_event_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an adverse event.
    def add_identifier(adverse_event, identifier = None, identifier_type = None, language = None, source = None, name = None):
        adverse_event.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to an adverse event.
    def add_object(adverse_event, obj = None, object_type = None):
        adverse_event.adverse_event_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Adverse event objects:
        
    """
    
    
        
    """
        Adverse event identifiers:
        
        MedDRA ID
        MedDRA Term
        MeSH UID
    """
    
    # Return all identifiers.
    def all_identifiers(adverse_event, user = None):
        AdverseEvent.meddra_id(adverse_event)
        AdverseEvent.meddra_term(adverse_event)
        AdverseEvent.mesh_uid(adverse_event)
    
    def meddra_id(adverse_event, user):
        return get_meddra_id(adverse_event, user)
        
    def meddra_term(adverse_event):
        return get_meddra_term(adverse_event)
        
    def mesh_uid(adverse_event, user):
        return get_mesh_uid(adverse_event, user)
    
    """
        Interaction objects:
        
        Phenotypes
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(adverse_event, user = None):
        interaction_obj = {}
        interaction_obj["Phenotypes"] = AdverseEvent.phenotypes(adverse_event)
        return interaction_obj
    
    def phenotypes(adverse_event, user):
        return get_phenotypes(adverse_event, user)
    
    """
        Other properties:
        
    """
    
    def all_properties(adverse_event, user = None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
    """
    
    def all_urls(adverse_event, user = None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None):
        return search(query, user = user)

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()