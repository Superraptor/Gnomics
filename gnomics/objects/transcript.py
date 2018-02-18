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
#   Create instance of a transcript.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.transcript_files.ensembl import get_ensembl_transcript_id, get_ensembl_transcript
from gnomics.objects.transcript_files.refseq import get_refseq_rna_id
from gnomics.objects.transcript_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.transcript_gene import get_gene
from gnomics.objects.interaction_objects.transcript_protein import get_protein

#   MAIN
def main():
    transcript_unit_tests()

#   TRANSCRIPT CLASS
class Transcript:
    """
        Transcript class:
        
        A transcript is a sequence of RNA produced
        by transcription.
        
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
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None, taxon=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name,
                'taxon': taxon
            }]
        
        # Initialize dictionary of transcript objects.
        self.transcript_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a transcript.
    def add_identifier(transcript, identifier=None, identifier_type=None, language=None, source=None, name=None, taxon=None):
        transcript.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name,
            'taxon': taxon
        })
        
    # Add an object to a transcript.
    def add_object(transcript, obj=None, object_type=None):
        transcript.transcript_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Transcript objects:
        
        Ensembl Transcript
        
    """
    
    # Return Ensembl transcript object.
    def ensembl_transcript(transcript, user=None):
        return get_ensembl_transcript(transcript)
        
    """
        Transcript identifiers:
        
        Ensembl Transcript ID
        RefSeq RNA ID
    """
    
    # Return all identifiers.
    def all_identifiers(transcript, user=None):
        Transcript.ensembl_transcript_id(transcript, user=user)
        Transcript.refseq_rna_id(transcript, user=user)
        return transcript.identifiers
    
    # Return Ensembl Transcript ID.
    def ensembl_transcript_id(transcript, user=None):
        return get_ensembl_transcript_id(transcript)
    
    # Return RefSeq RNA ID.
    def refseq_rna_id(transcript, user=None):
        return get_refseq_rna_id(transcript)
    
    """
        Interaction objects:
        
        Gene
        Protein
    """
    
    # Return interaction objects.
    def all_interaction_objects(transcript, user=None):
        interaction_obj = {}
        interaction_obj["Gene"] = Transcript.gene(transcript, user=user)
        interaction_obj["Protein"] = Transcript.protein(transcript, user=user)
        return interaction_obj
    
    # Return gene.
    def gene(transcript, user=None):
        return get_gene(transcript, user=user)
    
    # Return protein.
    def protein(transcript, user=None):
        return get_protein(transcript, user=user)
    
    """
        Other properties:
        
        Assembly name
        Biotype
        Canonical
        End
        Logic name
        Sequence region name
        Start
        Strand
        Version
    """
    
    def all_properties(transcript, user=None):
        property_dict = {}
        property_dict["Assembly Name"] = Transcript.assembly_name(transcript, user=user)
        property_dict["Biotype"] = Transcript.biotype(transcript, user=user)
        property_dict["Canonical"] = Transcript.is_canonical(transcript, user=user)
        property_dict["End"] = Transcript.end(transcript, user=user)
        property_dict["Logic Name"] = Transcript.logic_name(transcript, user=user)
        property_dict["Sequence Region Name"] = Transcript.sequence_region_name(transcript, user=user)
        property_dict["Start"] = Transcript.start(transcript, user=user)
        property_dict["Strand"] = Transcript.strand(transcript, user=user)
        property_dict["Version"] = Transcript.version(transcript, user=user)
        return property_dict
    
    # Get assembly name.
    def assembly_name(transcript, user=None):
        assembly = []
        for obj in Transcript.ensembl_transcript(transcript):
            assembly.append(obj["assembly_name"])
        return assembly
    
    # Get biotype.
    def biotype(transcript, user=None):
        biotype = []
        for obj in Transcript.ensembl_transcript(transcript):
            biotype.append(obj["biotype"])
        return biotype
    
    # Get transcript end.
    def end(transcript, user=None):
        end = []
        for obj in Transcript.ensembl_transcript(transcript):
            end.append(obj["end"])
        return end
    
    # Determine if canonical.
    def is_canonical(transcript, user=None):
        canonical = []
        for obj in Transcript.ensembl_transcript(transcript):
            if obj["is_canonical"] == 1:
                canonical.append(True)
            else:
                canonical.append(False)
        return canonical
    
    # Get logic name.
    def logic_name(transcript, user=None):
        logic_name = []
        for obj in Transcript.ensembl_transcript(transcript):
            logic_name.append(obj["logic_name"])
        return logic_name
    
    # Get sequence region name.
    def sequence_region_name(transcript, user=None):
        seq_region_name = []
        for obj in Transcript.ensembl_transcript(transcript):
            seq_region_name.append(obj["seq_region_name"])
        return seq_region_name
    
    # Get transcript start.
    def start(transcript, user=None):
        start = []
        for obj in Transcript.ensembl_transcript(transcript):
            start.append(obj["start"])
        return start
    
    # Get strand.
    def strand(transcript, user=None):
        strand = []
        for obj in Transcript.ensembl_transcript(transcript):
            strand.append(obj["strand"])
        return strand
    
    # Get version.
    def version(transcript, user=None):
        version = []
        for obj in Transcript.ensembl_transcript(transcript):
            version.append(obj["version"])
        return version
    
    """
        URLs:
        
    """
    
    # Return links.
    def all_urls(transcript, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, source="all", user=None):
        return search(query, source=source, user=user)

#   UNIT TESTS
def transcript_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()