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
#   Create instance of an assay.
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
from gnomics.objects.assay_files.bao import get_bao_id
from gnomics.objects.assay_files.chembl import get_chembl_id, get_chembl_assay
from gnomics.objects.assay_files.oidd import get_oidd_bioassay_id, get_oidd_bioassay_obj
from gnomics.objects.assay_files.pubchem import get_aids, get_pubchem_assay
from gnomics.objects.assay_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.assay_assay import get_assays
from gnomics.objects.interaction_objects.assay_gene import get_genes
from gnomics.objects.interaction_objects.assay_reference import get_references
from gnomics.objects.interaction_objects.assay_taxon import get_taxon

#   MAIN
def main():
    assay_unit_tests("1000")

#   ASSAY CLASS
class Assay():
    """
        Assay class
        
        A biochemical assay is an analytical in vitro
        procedure used to detect, quantify, and/or study
        the binding or activity of a biological molecule,
        such as an enzyme.
    """
    
    # BAO BioPortal PURL.
    bao_bioportal_purl = "http://purl.bioontology.org/ontology/BAO"
    
    """
        Assay attributes:
        
        Identifier      = A particular way to identify the
                          assay in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
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
        
        # Initialize dictionary of assay objects.
        self.assay_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an assay.
    def add_identifier(assay, identifier=None, identifier_type=None, language=None, taxon=None, source=None, name=None):
        assay.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    """
        Assay objects:
        
        ChEMBL Assay
        OIDD Bioassay
        PubChem Assay
        
    """
    
    # Return ChEMBL assay object.
    def chembl_assay(assay, user=None):
        return get_chembl_assay(assay)
    
    # Return OIDD Bioassay object.
    def oidd_bioassay(assay, user=None):
        return get_oidd_bioassay_obj(assay, user=user)
    
    # Return PubChem assay object.
    def pubchem_assay(assay, user=None):
        return get_pubchem_assay(assay)
        
    """
        Assay identifiers:
        
        BAO ID
        ChEMBL ID
        OIDD Bioassay ID
        PubChem AID
        PubChem Name
        
    """
    
    # Return all identifiers.
    def all_identifiers(assay, user=None):
        Assay.bao_id(assay, user=user)
        Assay.chembl_id(assay, user=user)
        Assay.oidd_bioassay_id(assay, user=user)
        Assay.pubchem_aid(assay, user=user)
        return assay.identifiers
    
    # Returns BAO ID.
    def bao_id(assay, user=None):
        return get_bao_id(assay)
        
    # Returns ChEMBL IDs for assays.
    def chembl_id(assay, user=None):
        return get_chembl_id(assay)
        
    # Returns OIDD Bioassay IDs.
    def oidd_bioassay_id(assay, user=None):
        return get_oidd_bioassay_id(assay)
        
    # Returns PubChem AIDs (bioassay records).
    def pubchem_aid(assay, user=None):
        return get_aids(assay)
        
    """
        Interaction objects:
        
        Assays
        Genes
        References
        Targets
        Taxa
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(assay, user=None):
        interaction_obj = {}
        interaction_obj["Assays"] = Assay.assays(assay, user=user)
        interaction_obj["Compounds"] = Assay.compounds(assay, user=user, compound_type="all")
        interaction_obj["Genes"] = Assay.genes(assay, user=user)
        interaction_obj["References"] = Assay.references(assay, user=user)
        interaction_obj["Taxon"] = Assay.taxon(assay, user=user)
        interaction_obj["Tissue"] = Assay.tissue(assay, user=user)
        return interaction_obj

    # Return assays.
    def assays(assay, user=None):
        return get_assays(assay)
        
    # Return compounds.
    def compounds(assay, user=None, compound_type="all"):
        return get_compounds(assay, user=None, compound_type=compound_type)
        
    # Return genes.
    def genes(assay, user=None):
        return get_genes(assay)
    
    # Return references.
    def references(assay, user=None):
        return get_references(assay)
        
    # Return targets.
        # TODO: ???
    def targets(assay, user=None):
        print("NOT FUNCTIONAL.")
        
    # Return taxa.
    def taxon(assay, user=None):
        return get_taxon(assay)
    
    # Return tissue.
    def tissue(assay, user=None):
        return get_tissue(assay)
    
    """
        Other properties:
        
        Assay category
        Assay subcellular fraction
        Assay test type
        Assay type
        Assay type description
        Comment
        Confidence description
        Confidence score
        Description
        Protocol
        Relationship description
        Relationship type
        Result
    """
    
    def all_properties(assay, user=None):
        property_dict = {}
        property_dict["Assay Categories"] = Assay.assay_category(assay, user=user)
        property_dict["Assay Subcellular Fraction"] = Assay.assay_subcellular_fraction(assay, user=user)
        property_dict["Assay Test Type"] = Assay.assay_test_type(assay, user=user)
        property_dict["Assay Type"] = Assay.assay_type(assay, user=user)
        property_dict["Assay Type Description"] = Assay.assay_type_description(assay, user=user)
        property_dict["Comments"] = Assay.comment(assay, user=user)
        property_dict["Confidence Description"] = Assay.confidence_description(assay, user=user)
        property_dict["Confidence Score"] = Assay.confidence_score(assay, user=user)
        property_dict["Description"] = Assay.description(assay, user=user)
        property_dict["Protocol"] = Assay.protocol(assay, user=user)
        property_dict["Relationship Description"] = Assay.relationship_description(assay, user=user)
        property_dict["Relationship Type"] = Assay.relationship_type(assay, user=user)
        property_dict["Result"] = Assay.result(assay, user=user)
        property_dict["Title"] = Assay.title(assay, user=user)
        return property_dict
    
    # Return assay category.
    def assay_category(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["assay_category"])
        return prop_array
    
    # Return assay subcellular fraction.
    def assay_subcellular_fraction(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["assay_subcellular_fraction"])
        return prop_array
    
    # Return assay test type.
    def assay_test_type(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["assay_test_type"])
        return prop_array
    
    # Return assay type.
    def assay_type(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["assay_type"])
        return prop_array
    
    # Return assay type description.
    def assay_type_description(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["assay_type_description"])
        return prop_array
    
    # Return comments.
    def comment(assay, source="pubchem", user=None):
        if source == "pubchem":
            comment_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    comment_array.extend(list(filter(None, infrassay["assay"]["descr"]["comment"])))
            return comment_array
        
    # Return confidence description.
    def confidence_description(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["confidence_description"])
        return prop_array
        
    # Return confidence score.
    def confidence_score(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["confidence_score"])
        return prop_array
        
    # Return description.
    def description(assay, source="pubchem", user=None):
        if source == "pubchem":
            desc_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    desc_array.extend(list(filter(None, infrassay["assay"]["descr"]["description"])))
            return desc_array
    
    # Return protocol.
    def protocol(assay, source="pubchem", user=None):
        if source == "pubchem":
            protocol_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    protocol_array.extend(list(filter(None, infrassay["assay"]["descr"]["protocol"])))
            return protocol_array
    
    # Return relationship description.
    def relationship_description(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["relationship_description"])
        return prop_array
    
    # Return relationship type.
    def relationship_type(assay, user=None):
        prop_array = []
        for x in Assay.chembl_assay(assay):
            prop_array.append(x["relationship_type"])
        return prop_array
    
    # Return results.
    def result(assay, source="pubchem", user=None):
        if source == "pubchem":
            result_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    result_array.extend(list(filter(None, infrassay["assay"]["descr"]["results"])))
            return result_array
        
    # Return title.
    def title(assay, source="openphacts", user=None):
        if source == "openphacts" and user is not None:
            title_array = []
            for obj in Assay.oidd_bioassay(assay, user = user):
                temp_title = obj["primaryTopic"]["exactMatch"]["title"]
                title_array.append(temp_title)
        elif source == "openphacts" and user is None:
            return []
        else:
            return []
        
    """
        URLs:
        
    """
    
    # Return links.
    def all_urls(assay, user=None):
        url_dict = {}
        return url_dict

    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Return assays from search.
    def search(query, assay_type_description=None, tissue_chembl_id=None, src_id=None, assay_organism=None, relationship_type=None, description=None, assay_chembl_id=None, assay_type=None, confidence_description=None, confidence_score=None, assay_tissue=None, target_chembl_id=None, relationship_description=None, assay_strain=None, src_assay_id=None, assay_tax_id=None, assay_cell_type=None, document_chembl_id=None, assay_category=None, assay_subcellular_fraction=None, cell_chembl_id=None, score=None, assay_test_type=None, bao_format=None, user = None):
        return search(query, assay_type_description=assay_type_description, tissue_chembl_id=tissue_chembl_id, src_id=src_id, assay_organism=assay_organism, relationship_type=relationship_type, description=description, assay_chembl_id=assay_chembl_id, assay_type=assay_type, confidence_description=confidence_description, confidence_score=confidence_score, assay_tissue=assay_tissue, target_chembl_id=target_chembl_id, relationship_description=relationship_description, assay_strain=assay_strain, src_assay_id=src_assay_id, assay_tax_id=assay_tax_id, assay_cell_type=assay_cell_type, document_chembl_id=document_chembl_id, assay_category=assay_category, assay_subcellular_fraction=assay_subcellular_fraction, cell_chembl_id=cell_chembl_id, score=score, assay_test_type=assay_test_type, bao_format=bao_format)
        
    
#   UNIT TESTS
def assay_unit_tests(pubchem_aid):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    
    # Get all identifiers.
    print("Getting assay identifiers from PubChem CID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    results_array = Assay.all_identifiers(pubchem_assay)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for iden in results_array:
        print("\t- %s: %s (%s)" % (iden["identifier_type"], iden["identifier"], iden["source"]))
    
    # Get all properties.
    print("\nGetting assay properties from PubChem AID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    results_dict = Assay.all_properties(pubchem_assay)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for prop_type, prop in results_dict.items():
        print("\t- %s: %s" % (prop_type, prop))

#   MAIN
if __name__ == "__main__": main()