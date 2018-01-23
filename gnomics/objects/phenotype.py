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
#   Create instance of a phenotype.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

#   Import modules.
from gnomics.objects.user import User
import gnomics.objects.disease

#   Import sub-methods.
from gnomics.objects.phenotype_files.hpo import get_hpo_id, get_hpo_term
from gnomics.objects.phenotype_files.meddra import get_meddra_id
from gnomics.objects.phenotype_files.mesh import get_mesh_uid
from gnomics.objects.phenotype_files.search import search
from gnomics.objects.phenotype_files.snomed import get_snomed_ct_id

#   Import further methods.
from gnomics.objects.interaction_objects.phenotype_anatomical_structure import get_anatomical_structures

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   PHENOTYPE CLASS
class Phenotype:
    """
        Phenotype class
        
        
    """
    
    """
        Phenotype attributes:
        
        Identifier      = A particular way to identify the
                          phenotype in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The taxon from which the protein
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the phenotype.
    def __init__(self, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'taxon': taxon,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of phenotype objects.
        self.phenotype_objects = []
        
    # Add an identifier to a phenotype.
    def add_identifier(phenotype, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        phenotype.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Phenotype objects
        
    """
    
    

    """
        Phenotype identifiers:
        
        HPO ID
        MedDRA ID
        MeSH UID
        SNOMED-CT ID
    """
    
    # Return all identifiers.
    def all_identifiers(phenotype, user = None):
        Phenotype.hpo(phenotype, user)
        Phenotype.hpo_term(phenotype, user)
        Phenotype.meddra_id(phenotype, user)
        Phenotype.mesh_uid(phenotype, user)
        Phenotype.snomed_ct_id(phenotype, user)
        return phenotype.identifiers
    
    # Returns HPO IDs (Human Phenotype Ontology).
    def hpo(phenotype, user):
        return get_hpo_id(phenotype, user)
    
    # Returns HPO Terms.
    def hpo_term(phenotype, user):
        return get_hpo_term(phenotype, user)
    
    # Returns MedDRA IDs.
    def meddra_id(phenotype, user):
        return get_meddra_id(phenotype, user)
    
    # Returns MeSH UIDs.
    def mesh_uid(phenotype, user):
        return get_mesh_uid(phenotype, user)
    
    # Returns MedDRA Terms.
    def snomed_ct_id(phenotype, user):
        return get_snomed_ct_id(phenotype, user)
    
    """
        Interaction objects:
        
        Anatomical structures
        
    """
    
    # Get anatomical structures.
    def anatomical_structures(phenotype):
        return get_anatomical_structures(phenotype)
    
    """
        Other properties
        
    """
    
    def all_properties(phenotype, user = None):
        property_dict = {}
        return property_dict
    
    """
        Phenotype URLs
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, source = "ebi", user = None):
        print("NOT FUNCTIONAL.")
        return search(query, source = source)
    
    """
        External files
        
    """
        
#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()