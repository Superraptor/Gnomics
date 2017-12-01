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
#   Create instance of a transcript.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.transcript_files.ensembl import get_ensembl_transcript_id
from gnomics.objects.transcript_files.refseq import get_refseq_rna_id

#   Import further methods.

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   TRANSCRIPT CLASS
class Transcript:
    """
        Transcript class:
        
    """
    
    """
        Transcript attributes:
        
        Identifier      = A particular way to identify the
                          transcript in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The taxon from which the transcript
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the transcript.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None, taxon = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name,
                'taxon': taxon
            }
        ]
        
        # Initialize dictionary of transcript objects.
        self.transcript_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a transcript.
    def add_identifier(transcript, identifier = None, identifier_type = None, language = None, source = None, name = None, taxon = None):
        transcript.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name,
            'taxon': taxon
        })
        
    # Add an object to a transcript.
    def add_object(transcript, obj = None, object_type = None):
        transcript.transcript_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Transcript objects:
        
    """
    
    
        
    """
        Transcript identifiers:
        
    """
    
    
    """
        Interaction objects:
        
    """
    
    
    
    """
        Other properties:
        
    """
    
    def all_properties(transcript, user = None):
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