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
#   Create instance of a protein.
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
import gnomics.objects.compound

#   Import sub-methods.
from gnomics.objects.protein_files.uniprot import get_uniprot_obj

#   Import further methods.
from gnomics.objects.interaction_objects.protein_compound import get_compounds
from gnomics.objects.interaction_objects.protein_gene import get_gene
from gnomics.objects.interaction_objects.protein_taxon import get_taxon
from gnomics.objects.interaction_objects.protein_tissue import get_tissues

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   PROTEIN CLASS
class Protein():
    """
        Protein class
        
        
    """
    
    """
        Protein attributes:
        
        Identifier      = A particular way to identify the
                          protein in question. Usually a
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
    
    # Initialize the protein.
    def __init__(self, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        
        # Initialize compound.
            # TODO: Does this actually work???
        gnomics.objects.compound.Compound.__init__(self, identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        
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
        
        # Initialize dictionary of protein objects.
        self.protein_objects = []
        
    # Add an identifier to a protein.
    def add_identifier(protein, identifier = None, identifier_type = None, taxon = None, language = None, source = None, name = None):
        gnomics.objects.compound.Compound.add_identifier(protein, identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        
        protein.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Protein objects:
        
        UniProt Object
    """
    
    # Return UniProt Object.
    def uniprot(prot):
        return get_uniprot_obj(prot) 
        
    """
        Protein identifiers:
        
        MINT Identifier
        STRING Identifier
        UniProtKB Accession
        UniProtKB Identifier
    """
    
    # Return MINT ID.
    def mint_id(prot):
        print("NOT FUNCTIONAL.")
    
    # Return STRING ID.
    def string_id(prot):
        print("NOT FUNCTIONAL.")
    
    # Return UniProtKB Accession.
    def uniprot_kb_acc(prot):
        print("NOT FUNCTIONAL.")
    
    """
        Interaction objects:
        
        References
        Taxon
    """
    
    # Return taxon
    def taxon(prot):
        return get_taxon(prot)
    
    """
        Other properties:
        
        Catalytic activity
        Domain
        Function
        Sequence
        Sequence caution
        Sequence length
        Similarity
        Subcellular location
        Subunit
    """
    
    def all_properties(protein, user = None):
        property_dict = {}
        return property_dict
    
    """
        Protein URLs:
        
    """
    
    
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query):
        print("NOT FUNCTIONAL.")
        
    """
        External files
        
    """

#   UNIT TESTS

#   MAIN
if __name__ == "__main__": main()