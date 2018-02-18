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

#   Other imports.
import timeit

#   Import sub-methods.
from gnomics.objects.protein_files.dip import get_dip_id
from gnomics.objects.protein_files.disprot import get_disprot_id
from gnomics.objects.protein_files.ensembl import get_ensembl_protein_id, get_ensembl_protein
from gnomics.objects.protein_files.mint import get_mint_id
from gnomics.objects.protein_files.pdb import get_pdb_id
from gnomics.objects.protein_files.pir import get_pir_id
from gnomics.objects.protein_files.refseq import get_refseq_acc
from gnomics.objects.protein_files.search import search
from gnomics.objects.protein_files.string_db import get_string_id
from gnomics.objects.protein_files.uniprot import get_uniprot_obj, get_uniprot_kb_ac, get_uniprot_kb_id

#   Import further methods.
from gnomics.objects.interaction_objects.protein_compound import get_compounds
from gnomics.objects.interaction_objects.protein_drug import get_drugs
from gnomics.objects.interaction_objects.protein_enzyme import get_enzyme
from gnomics.objects.interaction_objects.protein_gene import get_gene
from gnomics.objects.interaction_objects.protein_pathway import get_pathways
from gnomics.objects.interaction_objects.protein_protein_domain import get_protein_domains
from gnomics.objects.interaction_objects.protein_protein_family import get_protein_families
from gnomics.objects.interaction_objects.protein_reference import get_references
from gnomics.objects.interaction_objects.protein_taxon import get_taxon
from gnomics.objects.interaction_objects.protein_tissue import get_tissues, get_tissue_expression
from gnomics.objects.interaction_objects.protein_transcript import get_transcript

#   MAIN
def main():
    protein_unit_tests()

#   PROTEIN CLASS
class Protein():
    """
        Protein class
        
        A protein is any of a group of large biomolecules
        consisting of one or more long chains of amino
        acid residues.
    """
    
    # Protein Ontology (PR) BioPortal PURL.
    pr_bioportal_purl = "http://purl.bioontology.org/ontology/PR"
    
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
    def __init__(self, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'taxon': taxon,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of protein objects.
        self.protein_objects = []
        
    # Add an identifier to a protein.
    def add_identifier(protein, identifier=None, identifier_type=None, taxon=None, language=None, source=None, name=None):
        protein.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    # Add an object to a protein.
    def add_object(protein, obj=None, object_type=None):
        protein.protein_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Protein objects:
        
        Ensembl Protein Object
        UniProt Object
    """
    
    # Return Ensembl Protein.
    def ensembl_protein(prot, user=None):
        return get_ensembl_protein(prot) 
    
    # Return UniProt Object.
    def uniprot(prot, user=None):
        return get_uniprot_obj(prot) 
        
    """
        Protein identifiers:
        
        DIP Identifier
        MINT Identifier
        STRING Identifier
        UniProtKB Accession
        UniProtKB Identifier
    """
    
    # Return all identifiers.
    def all_identifiers(protein, user=None):
        Protein.dip_id(protein, user=user)
        Protein.mint_id(protein, user=user)
        Protein.pdb_id(protein, user=user)
        Protein.pir_id(protein, user=user)
        Protein.refseq_accession(protein, user=user)
        Protein.string_id(protein, user=user)
        Protein.uniprot_kb_accession(protein, user=user)
        Protein.uniprot_kb_id(protein, user=user)
        return protein.identifiers
    
    # Return DIP ID.
    def dip_id(prot, user=None):
        return get_dip_id(prot)
    
    # Return MINT ID.
    def mint_id(prot, user=None):
        return get_mint_id(prot)
    
    # Return PDB ID.
    def pdb_id(prot, user=None):
        return get_pdb_id(prot)
    
    # Return PIR ID.
    def pir_id(prot, user=None):
        return get_pir_id(prot)
    
    # Return RefSeq Accession.
    def refseq_accession(prot, user=None):
        return get_refseq_acc(prot)
    
    # Return STRING ID.
    def string_id(prot, user=None):
        return get_string_id(prot)
    
    # Return UniProtKB Accession.
    def uniprot_kb_accession(prot, user=None):
        return get_uniprot_kb_ac(prot)
    
    # Return UniProtKB Identifier.
    def uniprot_kb_id(prot, user=None):
        return get_uniprot_kb_id(prot)
    
    """
        Interaction objects:
        
        Compounds
        Drugs
        Enzymes
        Gene
        Pathways
        Protein domains
        Protein families
        References
        Taxon
        Tissues
        Transcripts
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(protein, user=None):
        interaction_obj = {}
        interaction_obj["Compounds"] = Protein.compounds(protein, user=user)
        interaction_obj["Drugs"] = Protein.drugs(protein, user=user)
        interaction_obj["Enzyme"] = Protein.enzyme(protein, user=user)
        interaction_obj["Gene"] = Protein.gene(protein, user=user)
        interaction_obj["Pathways"] = Protein.pathways(protein, user=user)
        interaction_obj["Protein_Domains"] = Protein.protein_domains(protein, user=user)
        interaction_obj["Protein_Families"] = Protein.protein_families(protein, user=user)
        interaction_obj["References"] = Protein.references(protein, user=user)
        interaction_obj["Taxon"] = Protein.taxon(protein, user=user)
        interaction_obj["Tissues"] = Protein.tissues(protein, user=user)
        interaction_obj["Transcript"] = Protein.transcript(protein, user=user)
        return interaction_obj
    
    # Return compounds.
    def compounds(prot, user=None):
        return get_compounds(prot)
    
    # Return drugs.
    def drugs(prot, user=None):
        return get_drugs(prot)
    
    # Return enzyme.
    def enzyme(prot, user=None):
        return get_enzyme(prot)
    
    # Return gene.
    def gene(prot, user=None):
        return get_gene(prot)
    
    # Return pathways.
    def pathways(prot, user=None):
        return get_pathways(prot)
    
    # Return protein domains.
    def protein_domains(prot, user=None):
        return get_protein_domains(prot)
    
    # Return protein families.
    def protein_families(prot, user=None):
        return get_protein_families(prot)
    
    # Return references.
    def references(prot, user=None):
        return get_references(prot)
    
    # Return taxon.
    def taxon(prot, user=None):
        return get_taxon(prot)
    
    # Return tissues.
    def tissues(prot, user=None):
        return get_tissues(prot)
    
    # Return tissue expression.
        # TODO: Change this so it takes a tissue parameter?
    def tissue_expression(prot, user=None):
        return get_tissue_expression(prot)
    
    # Return transcript.
    def transcript(prot, user=None):
        return get_transcript(prot)
    
    """
        Other properties:
        
        Catalytic activity
        Domain
        End
        Function
        Length
        Sequence
        Sequence caution
        Sequence length
        Similarity
        Start
        Subcellular location
        Subunit
    """
    
    def all_properties(protein, user=None):
        property_dict = {}
        property_dict["End"] = Protein.end(protein, user=user)
        property_dict["Length"] = Protein.length(protein, user=user)
        property_dict["Start"] = Protein.start(protein, user=user)
        return property_dict
    
    # Get protein end.
    def end(protein, user=None):
        end = []
        for obj in Protein.ensembl_protein(protein):
            end.append(obj["end"])
        return end
    
    # Get protein length.
    def length(protein, user=None):
        length = []
        for obj in Protein.ensembl_protein(protein):
            length.append(obj["length"])
        return length
    
    # Get protein start.
    def start(protein, user=None):
        start = []
        for obj in Protein.ensembl_protein(protein):
            start.append(obj["start"])
        return start
    
    """
        Protein URLs:
        
    """
    
    # Return links.
    def all_urls(protein, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, source="uniprot", result_format="tab", user=None):
        return search(query, source=source, result_format=result_format, user=user)
        
    """
        External files
        
    """

#   UNIT TESTS
def protein_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()