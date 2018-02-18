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
#   Create instance of a variation.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
import myvariant
import timeit

#   Import sub-methods.
from gnomics.objects.variation_files.dbsnp import get_dbsnp_obj, get_rs_number
from gnomics.objects.variation_files.hgvs import get_hgvs_obj, get_hgvs_id, get_coding_hgvs_id, get_genomic_hgvs_id
from gnomics.objects.variation_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.variation_gene import get_gene
from gnomics.objects.interaction_objects.variation_phenotype import get_phenotypes
from gnomics.objects.interaction_objects.variation_protein import get_protein
from gnomics.objects.interaction_objects.variation_transcript import get_transcript

#   MAIN
def main():
    variation_unit_tests()

#   VARIATION CLASS
class Variation:
    """
        Variation class:
        
        A variation, according to Encyclopædia Britannica, 
        is "any difference between cells, individual 
        organisms, or groups of organisms of any species 
        caused either by genetic differences (genotypic 
        variation) or by the effect of environmental 
        factors on the expression of the genetic potentials 
        (phenotypic variation)."
    """
    
    """
        Variation attributes:
        
        Identifier      = A particular way to identify the
                          variation in question. Usually a 
                          database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The taxon from which the variation
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the variation.
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
        
        # Initialize dictionary of variation objects.
        self.variation_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a variation.
    def add_identifier(variation, identifier=None, identifier_type=None, language=None, source=None, name=None, taxon=None):
        variation.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name,
            'taxon': taxon
        })
        
    # Add an object to a variation.
    def add_object(variation, obj=None, object_type=None):
        variation.variation_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Variation objects:
        
        dbSNP Object
        HGVS Object
    """
    
    # Return dbSNP object.
    def dbsnp(variation, user=None):
        return get_dbsnp_obj(variation)
                             
    # Return HGVS object.
    def hgvs(variation, user=None):
        return get_hgvs_obj(variation)
        
    """
        Variation identifiers:
        
        Coding HGVS ID
        Genomic HGVS ID
        HGVS ID
        RSID (RS Number)
    """
    
    # Return all identifiers.
    def all_identifiers(variation, user=None):
        Variation.coding_hgvs_id(variation, user=user)
        Variation.genomic_hgvs_id(variation, user=user)
        Variation.hgvs_id(variation, user=user)
        Variation.rs_number(variation, user=user)
        return variation.identifiers
    
    # Return coding HGVS ID.
    def coding_hgvs_id(variation, user=None):
        return get_coding_hgvs_id(variation)
    
    # Return genomic HGVS ID.
    def genomic_hgvs_id(variation, user=None):
        return get_genomic_hgvs_id(variation)
    
    # Return HGVS ID.
    def hgvs_id(variation, user=None):
        return get_hgvs_id(variation)
    
    # Return RS number.
    def rs_number(variation, user=None):
        return get_rs_number(variation)
    
    """
        Interaction objects:
        
        Gene
        Phenotypes
        Protein
        Transcript
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(variation, user=None):
        interaction_obj = {}
        interaction_obj["Gene"] = Variation.gene(variation, user=user)
        interaction_obj["Phenotypes"] = Variation.phenotypes(variation, user=user)
        interaction_obj["Protein"] = Variation.protein(variation, user=user)
        interaction_obj["Transcript"] = Variation.transcript(variation, user=user)
        return interaction_obj
    
    # Return gene.
    def gene(variation, user=None):
        return get_gene(variation)
    
    # Return phenotypes.
    def phenotypes(variation, user=None):
        return get_phenotypes(variation)
    
    # Return protein.
    def protein(variation, user=None):
        return get_protein(variation)
    
    # Return transcript.
    def transcript(variation, user=None):
        return get_transcript(variation)
    
    """
        Other properties:
       
        Alleles
        Allele origin
        Alternative sequence
        Chromosome
        Consequence
        Is known variant
        Length
        Position
        Reference sequence
        Validated
        Variation class
        Variation type
        
    """
    
    def all_properties(variation, user=None):
        property_dict = {}
        property_dict["Allele"] = Variation.alleles(variation, user=user)
        property_dict["Allele Origin"] = Variation.allele_origin(variation, user=user)
        property_dict["Alternative"] = Variation.alternative_sequence(variation, user=user)
        property_dict["Chromosome"] = Variation.chromosome(variation, user=user)
        property_dict["Consequence"] = Variation.consequence(variation, user=user)
        property_dict["Known Variant"] = Variation.is_known_variant(variation, user=user)
        property_dict["Length"] = Variation.length(variation, user=user)
        property_dict["Position"] = Variation.position(variation, user=user)
        property_dict["Reference"] = Variation.reference_sequence(variation, user=user)
        property_dict["Validated"] = Variation.validated(variation, user=user)
        property_dict["Class"] = Variation.variation_class(variation, user=user)
        property_dict["Type"] = Variation.variation_type(variation, user=user)
        return property_dict
    
    # Return alleles.
    def alleles(variation, user=None):
        all_array = []
        for obj in Variation.hgvs(variation):
            if "dbsnp" in obj:
                if "alleles" in obj["dbsnp"]:
                    for allele in obj["dbsnp"]["alleles"]:
                        all_array.append(allele["allele"])
        return all_array
    
    # Return allele origin.
    def allele_origin(variation, user=None):
        all_array = []
        for obj in Variation.hgvs(variation):
            if "dbsnp" in obj:
                if "allele_origin" in obj["dbsnp"]:
                    all_array.append(obj["dbsnp"]["allele_origin"])
        return all_array
    
    # Return alternate sequence or nucleotide.
    def alternate_sequence(variation, user=None):
        return alternative_sequence(variation, user=user)
    
    # Return alternative sequence or nucleotide.
    def alternative_sequence(variation, user=None):
        alt_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "alt" in obj["cadd"]:
                    alt_array.append(obj["cadd"]["alt"])
            if "dbsnp" in obj:
                if "alt" in obj["dbsnp"]:
                    alt_array.append(obj["dbsnp"]["alt"])
        return alt_array
    
    # Return chromosome.
    def chromosome(variation, user=None):
        chrom_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "chrom" in obj["cadd"]:
                    chrom_array.append(obj["cadd"]["chrom"])
            if "dbsnp" in obj:
                if "chrom" in obj["dbsnp"]:
                    chrom_array.append(obj["dbsnp"]["chrom"])
        return chrom_array
    
    # Return consequence.
    def consequence(variation, user=None):
        con_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "consequence" in obj["cadd"]:
                    con_array.append(obj["cadd"]["consequence"])
        return con_array
    
    # Return known variant status.
    def is_known_variant(variation, user=None):
        var_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "isknownvariant" in obj["cadd"]:
                    var_array.append(obj["cadd"]["isknownvariant"])
        return var_array
    
    # Return length.
    def length(variation, user=None):
        len_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "length" in obj["cadd"]:
                    len_array.append(obj["cadd"]["length"])
        return len_array
    
    # Return position.
    def position(variation, user=None):
        pos_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "pos" in obj["cadd"]:
                    pos_array.append(obj["cadd"]["pos"])
        return pos_array
    
    # Return reference sequence or nucleotide.
    def reference_sequence(variation, user=None):
        ref_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "ref" in obj["cadd"]:
                    ref_array.append(obj["cadd"]["ref"])
            if "dbsnp" in obj:
                if "ref" in obj["dbsnp"]:
                    ref_array.append(obj["dbsnp"]["ref"])
        return ref_array
    
    # Return if validated.
    def validated(variation, user=None):
        val_array = []
        for obj in Variation.hgvs(variation):
            if "dbsnp" in obj:
                if "validated" in obj["dbsnp"]:
                    val_array.append(obj["dbsnp"]["validated"])
        return val_array
    
    # Return variation class.
    def variation_class(variation, user=None):
        type_array = []
        for obj in Variation.hgvs(variation):
            if "dbsnp" in obj:
                if "class" in obj["dbsnp"]:
                    type_array.append(obj["dbsnp"]["class"])
        return type_array
    
    # Return variation type.
    def variation_type(variation, user=None):
        type_array = []
        for obj in Variation.hgvs(variation):
            if "cadd" in obj:
                if "type" in obj["cadd"]:
                    type_array.append(obj["cadd"]["type"])
            if "dbsnp" in obj:
                if "vartype" in obj["dbsnp"]:
                    type_array.append(obj["dbsnp"]["vartype"])
        return type_array
    
    """
        URLs:
        
    """
    
    # Return links.
    def all_urls(variation, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user=None, search_type=None, taxon="Homo sapiens", source="all"):
        return search(query, user=user, search_type=search_type, taxon=taxon, source=source)

#   UNIT TESTS
def variation_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()