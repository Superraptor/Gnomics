#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       EUTILS
#           https://github.com/biocommons/eutils
#

#
#   Create instance of a gene.
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
import gnomics.objects.taxon

#   Other imports.
from bioservices import *
from bioservices.uniprot import UniProt
from intermine.webservice import Service
import eutils.client
import re
import requests
import timeit

#   Import sub-methods.
from gnomics.objects.gene_files.ensembl import get_ensembl_gene_id, get_ensembl_gene
from gnomics.objects.gene_files.entrez import get_ncbi_entrez_gene, get_ncbi_entrez_gene_id
from gnomics.objects.gene_files.freebase import get_freebase_id
from gnomics.objects.gene_files.genecards import get_genecards_id
from gnomics.objects.gene_files.hgnc import get_hgnc_gene_id, get_hgnc_gene_symbol
from gnomics.objects.gene_files.homologene import get_homologene_id
from gnomics.objects.gene_files.kegg import get_kegg_gene, get_kegg_gene_id
from gnomics.objects.gene_files.mine import get_flymine_gene_id, get_flymine_primary_gene_id, get_flymine_secondary_gene_id, get_humanmine_gene_id, get_humanmine_primary_gene_id, get_humanmine_secondary_gene_id, get_mousemine_gene_id, get_mousemine_primary_gene_id, get_mousemine_secondary_gene_id, get_ratmine_gene_id, get_ratmine_primary_gene_id, get_ratmine_secondary_gene_id, get_wormmine_gene_id, get_wormmine_primary_gene_id, get_wormmine_secondary_gene_id, get_yeastmine_gene_id, get_yeastmine_primary_gene_id, get_yeastmine_secondary_gene_id, get_zebrafishmine_gene_id, get_zebrafishmine_primary_gene_id, get_zebrafishmine_secondary_gene_id
from gnomics.objects.gene_files.omim import get_omim_gene_id
from gnomics.objects.gene_files.pharos import get_pharos_gene_id
from gnomics.objects.gene_files.search import search
from gnomics.objects.gene_files.vega import get_vega_gene_id
from gnomics.objects.gene_files.wiki import get_arabic_wikipedia_accession, get_catalan_wikipedia_accession, get_german_wikipedia_accession, get_english_wikipedia_accession, get_spanish_wikipedia_accession, get_estonian_wikipedia_accession, get_finnish_wikipedia_accession, get_french_wikipedia_accession, get_italian_wikipedia_accession, get_japanese_wikipedia_accession, get_korean_wikipedia_accession, get_dutch_wikipedia_accession, get_polish_wikipedia_accession, get_portuguese_wikipedia_accession, get_slovenian_wikipedia_accession, get_tamil_wikipedia_accession, get_ukrainian_wikipedia_accession, get_urdu_wikipedia_accession, get_wikidata_accession, get_wikidata_object
from gnomics.objects.gene_files.wikigene import get_wikigene_id

#   Import further methods.
from gnomics.objects.interaction_objects.gene_compound import get_compounds
from gnomics.objects.interaction_objects.gene_disease import get_diseases
from gnomics.objects.interaction_objects.gene_drug import get_drugs
from gnomics.objects.interaction_objects.gene_gene import get_orthologs
from gnomics.objects.interaction_objects.gene_pathway import get_pathways
from gnomics.objects.interaction_objects.gene_phenotype import get_phenotypes
from gnomics.objects.interaction_objects.gene_protein import get_proteins
from gnomics.objects.interaction_objects.gene_reference import get_references
from gnomics.objects.interaction_objects.gene_taxon import get_taxon
from gnomics.objects.interaction_objects.gene_tissue import get_tissue_expression
from gnomics.objects.interaction_objects.gene_transcript import get_transcripts

#   MAIN
def main():
    gene_unit_tests("ENSG00000139618")

#   GENE CLASS
class Gene:
    """
        Gene class:
        
        According to Gerstein et al. (2007), a gene is a
        "genomic sequence (DNA or RNA) directly encoding
        functional product molecules, either RNA or protein."
        
    """
    
    # HUGO BioPortal PURL.
    hugo_bioportal_purl = "http://purl.bioontology.org/ontology/HUGO"
    
    # OMIM BioPortal PURL.
    hugo_bioportal_purl = "http://purl.bioontology.org/ontology/OMIM"
    
    """
        Gene attributes:
        
        Identifier      = A particular way to identify the
                          gene in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The species from which the gene
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the gene.
    def __init__(self, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        
        # If HGNC-related, set taxon to "Homo sapiens."
        if identifier is not None:
            if identifier_type.lower() in ["hgnc id", "hgnc identifier", "hgnc gene id", "hgnc gene identifier", "hgnc symbol", "hgnc gene symbol", "hgnc gene symbol"]:
                taxon = "Homo sapiens"
        
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
        
        # Initialize dictionary of gene objects.
        self.gene_objects = []
        
    # Add an identifier to a gene.
    def add_identifier(gene, identifier=None, identifier_type=None, taxon=None, language=None, source=None, name=None):
        gene.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    # Add an object to a gene.
    def add_object(gene, obj=None, object_type=None):
        gene.gene_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Gene objects:
        
        Ensembl Gene
        KEGG Gene
        NCBI Entrez Gene (NCBI Gene ID)
        Wikidata Object
        
    """
    
    # Return Ensembl gene object.
    def ensembl_gene(gene, user=None):
        return get_ensembl_gene(gene)
    
    # Get KEGG gene object.
    def kegg_gene(gene, user=None):
        return get_kegg_gene(gene)
    
    # Get NCBI Entrez gene object.
    def ncbi_entrez_gene(gene, user=None):
        return get_ncbi_entrez_gene(gene)
    
    # Get Wikidata object.
    def wikidata(gene, user=None):
        return get_wikidata_object(gene)
    
    """
        Gene identifiers:
        
        Ensembl gene identifier
        Freebase ID
        GeneCards ID
        FlyMine Gene ID
        FlyMine Primary Gene ID
        FlyMine Secondary Gene ID
        HGNC gene identifier
        HGNC gene symbol
        HomoloGene ID
        HumanMine Gene ID
        HumanMine Primary Gene ID
        HumanMine Secondary Gene ID
        KEGG gene identifier
        MouseMine Gene ID
        MouseMine Primary Gene ID
        MouseMine Secondary Gene ID
        NCBI gene identifier (Entrez)
        NCBI protein identifier
        OMIM identifier
        Pharos (Tchem) identifier
        RatMine Gene ID
        RatMine Primary Gene ID
        RatMine Secondary Gene ID
        Reactome identifier # Possibly a gene thing?
        UniProt identifier  # Move this to protein.py???
        Vega gene identifier
        Wikidata accession
        WikiGene ID
        WormMine Gene ID
        WormMine Primary Gene ID
        WormMine Secondary Gene ID
        YeastMine Gene ID
        YeastMine Primary Gene ID
        YeastMine Secondary Gene ID
        ZebrafishMine Gene ID
        ZebrafishMine Primary Gene ID
        ZebrafishMine Secondary Gene ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(gene, user=None):
        Gene.ensembl_gene_id(gene, user=user)
        Gene.flymine_gene_id(gene, user=user)
        Gene.flymine_primary_gene_id(gene, user=user)
        Gene.flymine_secondary_gene_id(gene, user=user)
        Gene.hgnc_gene_id(gene, user=user)
        Gene.hgnc_gene_symbol(gene, user=user)
        Gene.humanmine_gene_id(gene, user=user)
        Gene.humanmine_primary_gene_id(gene, user=user)
        Gene.humanmine_secondary_gene_id(gene, user=user)
        Gene.kegg_gene_id(gene, user=user)
        Gene.mousemine_gene_id(gene, user=user)
        Gene.mousemine_primary_gene_id(gene, user=user)
        Gene.mousemine_secondary_gene_id(gene, user=user)
        Gene.ncbi_entrez_gene_id(gene, user=user)
        Gene.omim_id(gene, user=user)
        Gene.pharos_gene_id(gene, user=user)
        Gene.ratmine_gene_id(gene, user=user)
        Gene.ratmine_primary_gene_id(gene, user=user)
        Gene.ratmine_secondary_gene_id(gene, user=user)
        Gene.vega_gene_id(gene, user=user)
        Gene.wikidata_accession(gene, user=user)
        Gene.wikigene_id(gene, user=user)
        Gene.wikipedia_accession(gene, language="arabic", user=user)
        Gene.wikipedia_accession(gene, language="catalan", user=user)
        Gene.wikipedia_accession(gene, language="dutch", user=user)
        Gene.wikipedia_accession(gene, language="english", user=user)
        Gene.wikipedia_accession(gene, language="estonian", user=user)
        Gene.wikipedia_accession(gene, language="finnish", user=user)
        Gene.wikipedia_accession(gene, language="french", user=user)
        Gene.wikipedia_accession(gene, language="german", user=user)
        Gene.wikipedia_accession(gene, language="italian", user=user)
        Gene.wikipedia_accession(gene, language="japanese", user=user)
        Gene.wikipedia_accession(gene, language="korean", user=user)
        Gene.wikipedia_accession(gene, language="polish", user=user)
        Gene.wikipedia_accession(gene, language="portuguese", user=user)
        Gene.wikipedia_accession(gene, language="slovenian", user=user)
        Gene.wikipedia_accession(gene, language="spanish", user=user)
        Gene.wikipedia_accession(gene, language="tamil", user=user)
        Gene.wikipedia_accession(gene, language="ukrainian", user=user)
        Gene.wikipedia_accession(gene, language="urdu", user=user)
        Gene.wormmine_gene_id(gene, user=user)
        Gene.wormmine_primary_gene_id(gene, user=user)
        Gene.wormmine_secondary_gene_id(gene, user=user)
        Gene.yeastmine_gene_id(gene, user=user)
        Gene.yeastmine_primary_gene_id(gene, user=user)
        Gene.yeastmine_secondary_gene_id(gene, user=user)
        Gene.zebrafishmine_gene_id(gene, user=user)
        Gene.zebrafishmine_primary_gene_id(gene, user=user)
        Gene.zebrafishmine_secondary_gene_id(gene, user=user)
        
        return gene.identifiers
    
    # Returns Ensembl gene identifier.
    def ensembl_gene_id(gene, user=None):
        return get_ensembl_gene_id(gene, user=user)
    
    # Returns FlyMine gene identifier.
    def flymine_gene_id(gene, user=None):
        return get_flymine_gene_id(gene)
    
    # Returns primary FlyMine gene identifier.
    def flymine_primary_gene_id(gene, user=None):
        return get_flymine_primary_gene_id(gene)
    
    # Returns secondary FlyMine gene identifier.
    def flymine_secondary_gene_id(gene, user=None):
        return get_flymine_secondary_gene_id(gene)
    
    # Returns Freebase ID.
    def freebase_id(gene, user=None):
        return get_freebase_id(gene)
    
    # Returns GeneCards ID
    def genecards_id(gene, user=None):
        return get_genecards_id(gene)
    
    # Returns HGNC gene identifier.
    def hgnc_gene_id(gene, user=None):
        return get_hgnc_gene_id(gene)
    
    # Returns HGNC gene symbol.
    def hgnc_gene_symbol(gene, user=None):
        return get_hgnc_gene_symbol(gene)
    
    # Returns HomoloGene ID.
    def homologene_id(gene, user=None):
        return get_homologene_id(gene)
    
    # Returns HumanMine gene identifier.
    def humanmine_gene_id(gene, user=None):
        return get_humanmine_gene_id(gene)
    
    # Returns primary HumanMine gene identifier.
    def humanmine_primary_gene_id(gene, user=None):
        return get_humanmine_primary_gene_id(gene)
    
    # Returns secondary HumanMine gene identifier.
    def humanmine_secondary_gene_id(gene, user=None):
        return get_humanmine_secondary_gene_id(gene)
    
    # Returns MouseMine gene identifier.
    def mousemine_gene_id(gene, user=None):
        return get_mousemine_gene_id(gene)
    
    # Returns primary MouseMine gene identifier.
    def mousemine_primary_gene_id(gene, user=None):
        return get_mousemine_primary_gene_id(gene)
    
    # Returns secondary MouseMine gene identifier.
    def mousemine_secondary_gene_id(gene, user=None):
        return get_mousemine_secondary_gene_id(gene)
        
    # Returns NCBI gene identifier.
    def ncbi_entrez_gene_id(gene, user=None):
        return get_ncbi_entrez_gene_id(gene)
    
    # Returns OMIM gene identifier.
    def omim_id(gene, user=None):
        return get_omim_gene_id(gene)
    
    # Returns KEGG gene identifier.
    def kegg_gene_id(gene, user=None):
        return get_kegg_gene_id(gene)
    
    # Returns Pharos (Tchem) identifier.
    def pharos_gene_id(gene, user=None):
        return get_pharos_gene_id(gene)
    
    # Returns RatMine gene identifier.
    def ratmine_gene_id(gene, user=None):
        return get_ratmine_gene_id(gene)
    
    # Returns primary RatMine gene identifier.
    def ratmine_primary_gene_id(gene, user=None):
        return get_ratmine_primary_gene_id(gene)
    
    # Returns secondary RatMine gene identifier.
    def ratmine_secondary_gene_id(gene, user=None):
        return get_ratmine_secondary_gene_id(gene)
    
    # Returns Vega gene identifier.
    def vega_gene_id(gene, user=None):
        return get_vega_gene_id(gene)
    
    # Returns Wikidata accession.
    def wikidata_accession(gene, user=None):
        return get_wikidata_accession(gene)
    
    # Returns WikiGene ID.
    def wikigene_id(gene, user=None):
        return get_wikigene_id(gene)
    
    def wikipedia_accession(gene, language="en", user=None):
        if language.lower() in ["ara", "ar", "arabic", "all"]:
            return get_arabic_wikipedia_accession(gene)
        elif language == "cat" or language == "ca" or language.lower() == "catalan":
            return get_catalan_wikipedia_accession(gene)
        elif language == "dut" or language == "nl" or language.lower() == "dutch":
            return get_dutch_wikipedia_accession(gene)
        elif language == "eng" or language == "en" or language.lower() == "english":
            return get_english_wikipedia_accession(gene)
        elif language == "est" or language == "et" or language.lower() == "estonian":
            return get_estonian_wikipedia_accession(gene)
        elif language == "fin" or language == "fi" or language.lower() == "finnish":
            return get_finnish_wikipedia_accession(gene)
        elif language == "fre" or language == "fr" or language.lower() == "french":
            return get_french_wikipedia_accession(gene)
        elif language == "ger" or language == "de" or language.lower() == "german":
            return get_german_wikipedia_accession(gene)
        elif language == "ita" or language == "it" or language.lower() == "italian":
            return get_italian_wikipedia_accession(gene)
        elif language == "jpn" or language == "ja" or language.lower() == "japanese":
            return get_japanese_wikipedia_accession(gene)
        elif language == "kor" or language == "ko" or language.lower() == "korean":
            return get_korean_wikipedia_accession(gene)
        elif language == "pol" or language == "pl" or language.lower() == "polish":
            return get_polish_wikipedia_accession(gene)
        elif language == "por" or language == "pt" or language.lower() == "portuguese":
            return get_portuguese_wikipedia_accession(gene)
        elif language == "slv" or language == "sl" or language.lower() == "slovenian":
            return get_slovenian_wikipedia_accession(gene)
        elif language == "spa" or language == "es" or language.lower() == "spanish":
            return get_spanish_wikipedia_accession(gene)
        elif language == "tam" or language == "ta" or language.lower() == "tamil":
            return get_tamil_wikipedia_accession(gene)
        elif language == "ukr" or language == "uk" or language.lower() == "ukrainian":
            return get_ukrainian_wikipedia_accession(gene)
        elif language == "urd" or language == "ur" or language.lower() == "urdu":
            return get_urdu_wikipedia_accession(gene)
        else:
            print("The given language is not currently supported.")
            
    # Returns WormMine gene identifier.
    def wormmine_gene_id(gene, user=None):
        return get_wormmine_gene_id(gene)
    
    # Returns primary WormMine gene identifier.
    def wormmine_primary_gene_id(gene, user=None):
        return get_wormmine_primary_gene_id(gene)
    
    # Returns secondary WormMine gene identifier.
    def wormmine_secondary_gene_id(gene, user=None):
        return get_wormmine_secondary_gene_id(gene)
    
    # Returns YeastMine gene identifier.
    def yeastmine_gene_id(gene, user=None):
        return get_yeastmine_gene_id(gene)
    
    # Returns primary YeastMine gene identifier.
    def yeastmine_primary_gene_id(gene, user=None):
        return get_yeastmine_primary_gene_id(gene)
    
    # Returns secondary YeastMine gene identifier.
    def yeastmine_secondary_gene_id(gene, user=None):
        return get_yeastmine_secondary_gene_id(gene)

    # Returns ZebrafishMine gene identifier.
    def zebrafishmine_gene_id(gene, user=None):
        return get_zebrafishmine_gene_id(gene)
    
    # Returns primary ZebrafishMine gene identifier.
    def zebrafishmine_primary_gene_id(gene, user=None):
        return get_zebrafishmine_primary_gene_id(gene)
    
    # Returns secondary ZebrafishMine gene identifier.
    def zebrafishmine_secondary_gene_id(gene, user=None):
        return get_zebrafishmine_secondary_gene_id(gene)
    
    """
        Interaction objects:
        
        Compounds
        Diseases
        Drugs
        Pathways
        Taxa
        Tissue Expression
        Transcripts
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(gene, user=None):
        interaction_obj = {}
        interaction_obj["Compound_Interactions"] = Gene.compound_interactions(gene, user=user)
        interaction_obj["Diseases"] = Gene.diseases(gene, user=user)
        interaction_obj["Drug_Interactions"] = Gene.drug_interactions(gene, user=user)
        interaction_obj["Orthologs"] = Gene.orthologs(gene, user=user)
        interaction_obj["Pathways"] = Gene.pathways(gene, user=user)
        interaction_obj["Phenotypes"] = Gene.phenotypes(gene, user=user)
        interaction_obj["Proteins"] = Gene.proteins(gene, user=user)
        interaction_obj["Taxon"] = Gene.taxon(gene, user=user)    # TODO: ???
        interaction_obj["Transcripts"] = Gene.transcripts(gene, user=user)
        return interaction_obj
    
    # Get compound interactions.
    def compound_interactions(gene, user=None):
        return get_compounds(gene)
    
    # Get diseases.
    def diseases(gene, user=None):
        return get_diseases(gene)

    # Get drug interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def drug_interactions(gene, source="dgidb", interaction_sources=None, interaction_types=None, drug_types=None, source_trust_levels=None, user=None):
        return get_drugs(gene, source=source, interaction_sources=interaction_sources, interaction_types=interaction_types, drug_types=drug_types, source_trust_levels=source_trust_levels)
    
    # Get orthologs.
    def orthologs(gene, user=None):
        return get_orthologs(gene)
    
    # Get orthologues.
    def orthologues(gene, user=None):
        return orthologs(gene)
    
    # Get pathways.
    def pathways(gene, user=None):
        return get_pathways(gene)
    
    # Get phenotypes.
    def phenotypes(gene, user=None):
        return get_phenotypes(gene)
        
    # Get proteins.
    def proteins(gene, taxon="Homo sapiens", user=None):
        return get_proteins(gene, taxon=taxon)
    
    # Get references.
    def references(gene, user=None):
        return get_references(gene)
    
    # Get taxon.
    def taxon(gene, user=None):
        return get_taxon(gene, user=user)
       
    # Get tissue expression.
    def tissue_expression(gene, user=None):
        return get_tissue_expression(gene)
    
    # Get transcript.
    def transcripts(gene, user=None):
        return get_transcripts(gene)
    
    """
        Gene properties:
        
        Assembly name
        Biotype
        Chromosomal position
        Definition
        Description
        End
        Gene Type
        Locus
        Map location
        Start
        Strand
        Summary
        Version
        
    """
    
    def all_properties(gene, user=None):
        property_dict = {}
        property_dict["Assembly Name"] = Gene.assembly_name(gene, user=user)
        property_dict["Biotype"] = Gene.biotype(gene, user=user)
        property_dict["Definition"] = Gene.definition(gene, user=user)
        property_dict["Description"] = Gene.description(gene, user=user)
        property_dict["End"] = Gene.end(gene, user=user)
        property_dict["Length"] = Gene.gene_length(gene, user=user)
        property_dict["Locus"] = Gene.locus(gene, user=user)
        property_dict["Map Location"] = Gene.map_location(gene, user=user)
        property_dict["Sequence"] = Gene.sequence(gene, user=user)
        property_dict["Start"] = Gene.start(gene, user=user)
        property_dict["Strand"] = Gene.strand(gene, user=user)
        property_dict["Summary"] = Gene.summary(gene, user=user)
        property_dict["Type"] = Gene.gene_type(gene, user=user)
        property_dict["Version"] = Gene.version(gene, user=user)
        return property_dict
    
    # Get assembly name.
    def assembly_name(gene, user=None):
        assembly = []
        for obj in Gene.ensembl_gene(gene):
            assembly.append(obj["assembly_name"])
        return assembly
    
    # Get biotype.
    def biotype(gene, user=None):
        biotype = []
        for obj in Gene.ensembl_gene(gene):
            biotype.append(obj["biotype"])
        return biotype
    
    # Get definition.
    def definition(gene, source="kegg", user=None):
        definitions = []
        for obj in Gene.kegg_gene(gene):
            definitions.append(obj["DEFINITION"])
        return definitions
    
    # Get description.
    def description(gene, source="ncbi", user=None):
        descriptions = []
        for obj in Gene.ensembl_gene(gene):
            descriptions.append(obj["description"])
        for obj in Gene.ncbi_entrez_gene(gene):
            descriptions.append(obj.description)
        return descriptions
    
    # Get gene end.
    def end(gene, user=None):
        end = []
        for obj in Gene.ensembl_gene(gene):
            end.append(obj["end"])
        return end
    
    # Get gene length (bp).
    def gene_length(gene, source="ensembl", user=None):
        gene_length = []
        for ensembl_obj in Gene.ensembl_gene(gene):
            gene_length.append(ensembl_obj["end"] - ensembl_obj["start"])
        return gene_length
    
    # Get gene type.
    def gene_type(gene, user=None):
        gene_type = []
        for obj in Gene.ncbi_entrez_gene(gene):
            gene_type.append(obj.type)
        return gene_type
    
    # Get locus.
    def locus(gene, verbose=False, user=None):
        locus = []
        for obj in Gene.ncbi_entrez_gene(gene):
            try:
                locus.append(obj.locus)
            except NameError:
                if verbose:
                    print("A name error occurred, as the Entrez Gene Locus is not defined.")
        return locus
    
    # Get map location.
    def map_location(gene, user=None):
        map_loc = []
        for obj in Gene.ncbi_entrez_gene(gene):
            map_loc.append(obj.maploc)
        return map_loc
    
    # Get position (chromosomal).
    def position(gene, source="kegg", user=None):
        pos = []
        for obj in Gene.kegg_gene(gene):
            pos.append(obj["POSITION"])
        return pos
    
    # Get nucleotide sequence.
    def sequence(gene, source="kegg", user=None):
        seq = []
        for obj in Gene.kegg_gene(gene):
            seq.append("".join(obj["NTSEQ"].split()))
        return seq
    
    # Get gene start.
    def start(gene, user=None):
        start = []
        for obj in Gene.ensembl_gene(gene):
            start.append(obj["start"])
        return start
    
    # Get strand.
    def strand(gene, user=None):
        strand = []
        for obj in Gene.ensembl_gene(gene):
            strand.append(obj["strand"])
        return strand
    
    # Get summary.
    def summary(gene, user=None):
        summary = []
        for obj in Gene.ncbi_entrez_gene(gene):
            summary.append(obj.summary)
        return summary
    
    # Get version.
    def version(gene, user=None):
        version = []
        for obj in Gene.ensembl_gene(gene):
            version.append(obj["version"])
        return version
        
    """
        Gene URLs:
        
        KEGG gene URL
        OMIM URL
        UniProt URL
        
    """
    
    # Return links.
    def all_urls(gene, user=None):
        url_dict = {}
        return url_dict
    
    # Get KEGG gene URL.
    def kegg_gene_url(gene, user=None):
        url_array = []
        for gene_id in Gene.kegg_gene_id(gene):
            base_url = "http://www.kegg.jp/entry/" 
            gene_array = re.findall(r"[^\W\d_]+|\d+", gene_id)
            final_gene_from_array = gene_array[0] + ":" + gene_array[1]
            url_array.append(base_url + final_gene_from_array + ":" + kegg_identifier)
        return url_array
    
    # Get OMIM URL.
    def omim_url(gene, user=None):
        url_array = []
        for gene_id in Gene.omim_id(gene, user=user):
            base_url = "https://www.omim.org/entry/"
            url_array.append(base_url + gene_id)
        return url_array
    
    # Get UniProt URL.
    def uniprot_url(gene, user=None):
        url_array = []
        for gene_id in Gene.uniprot_id(gene, user=user):
            base_url = "http://www.uniprot.org/uniprot/"
            url_array.append(base_url + gene_id)
        return url_array
    
    """
        Auxiliary functions:
        
        NCBI BLAST
        Search
    """
    
    # NCBI BLAST from gene sequence.
    # Gene MUST be just the sequence, without a header
    # and without newlines or spaces.
    #
    # Example programs:
    # 'blastp', 'blastn', 'blastx', 'tblastn', 'tblastx'
    #
    # Possible stypes:
    # (Not sure) 'protein', 'nucleotide'
    def ncbi_blast(gene, user=None, program="blastp", sequence="amino acid", database="uniprotkb", taxon=None):
        s = NCBIblast(verbose=False)
        if sequence == "nucleotide":
            jobid = s.run(program=program, sequence=gene.nucleotide_sequence, stype="nucleotide", database=database, email=user.email)
            if taxon == None:
                return s.getResult(jobid, "out")[0:1000]
            elif taxon == "Homo sapiens":
                return [x for x in s.getResult(jobid, "out").split("\n") if "HUMAN" in x]
        elif sequence == "amino acid":
            jobid = s.run(program=program, sequence=gene.amino_acid_sequence, stype="protein", database=database, email=user.email)
            if taxon == None:
                return s.getResult(jobid, "out")[0:1000]
            elif taxon == "Homo sapiens":
                return [x for x in s.getResult(jobid, "out").split("\n") if "HUMAN" in x]
        
    """
        External files:
        
        FASTA file
    """
    
    def fasta_file():       # This is for a single sequence.
        print("NOT FUNCTIONAL.")
        
    def group_fasta_file(): # This is for multiple sequences
        print("NOT FUNCTIONAL.")
        
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user=None, search_type=None, taxon="Homo sapiens", source="all"):
        return search(query, user=user, search_type=search_type, taxon=taxon, source=source)

#   UNIT TESTS
def gene_unit_tests(ensembl_gene_id):
    ensembl_gene = Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, source = "Ensembl")
    
    # Get all identifiers.
    print("Getting gene identifiers from Ensembl Gene ID (%s)..." % ensembl_gene_id)
    start = timeit.timeit()
    results_array = Gene.all_identifiers(ensembl_gene)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for iden in results_array:
        print("\t- %s: %s (%s)" % (iden["identifier_type"], str(iden["identifier"]).encode('ascii', 'ignore').decode(), iden["source"]))
    
    # Get all properties.
    print("\nGetting gene properties from Ensembl Gene ID (%s)..." % ensembl_gene_id)
    start = timeit.timeit()
    results_dict = Gene.all_properties(ensembl_gene)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for prop_type, prop in results_dict.items():
        print("\t- %s: %s" % (prop_type, str(prop).encode('ascii', 'ignore').decode()))

#   MAIN
if __name__ == "__main__": main()