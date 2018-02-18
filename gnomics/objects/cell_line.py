#!/usr/bin/env python

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
from gnomics.objects.cell_line_files.lincs import get_lincs_obj, get_lincs_id
from gnomics.objects.cell_line_files.search import search

#   Other imports.
import timeit

#   Import further methods.
from gnomics.objects.interaction_objects.cell_line_taxon import get_taxon
from gnomics.objects.interaction_objects.cell_line_tissue import get_tissue

#   MAIN
def main():
    cell_line_unit_tests()

#   CELL LINE CLASS
class CellLine:
    """
        Cell line class:
        
        Cell lines are cell cultures developed from
        single cells which therefore consist of cells
        with uniform genetic makeup.
    """
    
    # CLO (Cell Line Ontology) BioPortal PURL.
    clo_bioportal_purl = "http://purl.bioontology.org/ontology/CLO"
    
    # CCONT (Cell Culture Ontology) BioPortal PURL.
    ccont_bioportal_purl = "http://purl.bioontology.org/ontology/CCONT"
    
    # MCBCC BioPortal PURL.
    mcbcc_bioportal_purl = "http://purl.bioontology.org/ontology/MCBCC"
    
    # MCCL BioPortal PURL.
    clo_bioportal_purl = "http://purl.bioontology.org/ontology/MCCL"
    
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
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of cell line objects.
        self.cell_line_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a cell line.
    def add_identifier(cell_line, identifier=None, identifier_type=None, language=None, source=None, name=None):
        cell_line.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a cell line.
    def add_object(cell_line, obj=None, object_type=None):
        cell_line.cell_line_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Cell line objects:
        
        Cellosaurus Object
        LICNS Object
        
    """
    
    # Return Cellosaurus object.
    def cellosaurus(cell_line, user=None):
        return get_cellosaurus_obj(cell_line)
    
    # Return LINCS object.
    def lincs(cell_line, user=None):
        return get_lincs_obj(cell_line)
        
    """
        Cell line identifiers:
        
        Cellosaurus ID
        ChEMBL ID
        LINCS ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(cell_line, user=None):
        CellLine.cellosaurus_id(cell_line, user=user)
        CellLine.chembl_id(cell_line, user=user)
        return cell_line.identifiers
    
    def cellosaurus_id(cell_line, user=None):
        return get_cellosaurus_id(cell_line)
        
    def chembl_id(cell_line, user=None):
        return get_chembl_id(cell_line)
    
    def lincs_id(cell_line, user=None):
        return get_lincs_id(cell_line)
    
    """
        Interaction objects:
        
        Taxa
        Tissue
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(cell_line, user=None):
        interaction_obj = {}
        interaction_obj["Taxon"] = CellLine.taxon(cell_line, user=user)
        interaction_obj["Tissue"] = CellLine.tissue(cell_line, user=user)
        return interaction_obj
    
    def taxon(cell_line, user=None):
        return get_taxon(cell_line)
    
    def tissue(cell_line, user=None):
        return get_tissue(cell_line)
    
    """
        Other properties:
        
        
        
    """
    
    def all_properties(cell_line, user=None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
    """
    
    # Return links.
    def all_urls(cell_line, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, source="ebi", user=None):
        return search(query, source=source)

#   UNIT TESTS
def cell_line_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()