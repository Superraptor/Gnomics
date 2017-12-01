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
#   Create instance of a cell line.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.cell_line_files.cellosaurus import get_cellosaurus_obj, get_cellosaurus_id
from gnomics.objects.cell_line_files.chembl import get_chembl_obj, get_chembl_id

#   Import further methods.
from gnomics.objects.interaction_objects.cell_line_taxon import get_taxon

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   CELL LINE CLASS
class CellLine:
    """
        Cell line class:
        
        Cell lines are cell cultures developed from
        single cells which therefore consist of cells
        with uniform genetic makeup.
    """
    
    """
        Cell line attributes:
        
        Identifier      = A particular way to identify the
                          cell line in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the cell line.
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
        
        # Initialize dictionary of cell line objects.
        self.cell_line_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a cell line.
    def add_identifier(cell_line, identifier = None, identifier_type = None, language = None, source = None, name = None):
        cell_line.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a cell line.
    def add_object(cell_line, obj = None, object_type = None):
        cell_line.cell_line_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Cell line objects:
        
        Cellosaurus object
        
    """
    
    def cellosaurus_obj(cell_line):
        return get_cellosaurus_obj(cell_line)
        
    """
        Cell line identifiers:
        
        Cellosaurus ID
        ChEMBL ID
    """
    
    # Return all identifiers.
    def all_identifiers(cell_line, user = None):
        CellLine.cellosaurus_id(cell_line)
        CellLine.chembl_id(cell_line)
        return cell_line.identifiers
    
    def cellosaurus_id(cell_line):
        return get_cellosaurus_id(cell_line)
        
    def chembl_id(cell_line):
        return get_chembl_id(cell_line)
    
    """
        Interaction objects:
        
        Taxa
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(cell_line, user = None):
        interaction_obj = {}
        interaction_obj["Taxa"] = CellLine.taxa(cell_line)
        return interaction_obj
    
    def taxa(cell_line):
        return get_taxon(cell_line)
    
    """
        Other properties:
        
        
        
    """
    
    def all_properties(cell_line, user = None):
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