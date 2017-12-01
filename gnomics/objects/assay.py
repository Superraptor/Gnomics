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

#   Import sub-methods.
from gnomics.objects.assay_files.chembl import get_chembl_id, get_chembl_assay
from gnomics.objects.assay_files.oidd import get_oidd_bioassay_id, get_oidd_bioassay_obj
from gnomics.objects.assay_files.pubchem import get_aids, get_pubchem_assay
from gnomics.objects.assay_files.search import search

#   Import further methods.
from gnomics.objects.interaction_objects.assay_assay import get_assays
from gnomics.objects.interaction_objects.assay_gene import get_genes
from gnomics.objects.interaction_objects.assay_taxon import get_taxa

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
        
        # Initialize dictionary of assay objects.
        self.assay_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an assay.
    def add_identifier(assay, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
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
    def chembl_assay(assay):
        return get_chembl_assay(assay)
    
    # Return OIDD Bioassay object.
    def oidd_bioassay(assay, user = None):
        return get_oidd_bioassay_obj(assay, user = user)
    
    # Return PubChem assay object.
    def pubchem_assay(assay):
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
    def all_identifiers(assay, user = None):
        Assay.bao_id(assay)
        Assay.chembl_id(assay)
        Assay.oidd_bioassay.id(assay)
        Assay.pubchem_aid(assay)
        return assay.identifiers
    
    # Returns BAO ID.
    def bao_id(assay):
        return get_bao_id(assay)
        
    # Returns ChEMBL IDs for assays.
    def chembl_id(assay):
        return get_chembl_id(assay)
        
    # Returns OIDD Bioassay IDs.
    def oidd_bioassay_id(assay):
        return get_oidd_bioassay_id(assay)
        
    # Returns PubChem AIDs (bioassay records).
    def pubchem_aid(assay):
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
    def all_interaction_objects(assay, user = None):
        interaction_obj = {}
        interaction_obj["Assays"] = Assay.assays(assay)
        interaction_obj["Genes"] = Assay.genes(assay)
        interaction_obj["References"] = Assay.references(assay)
        interaction_obj["Taxa"] = Assay.taxa(assay)
        return interaction_obj

    # Return assays.
    def assays(assay):
        return get_assays(assay)
        
    # Return compounds.
    def compounds(assay):
        print("NOT FUNCTIONAL.")
    
    # Return genes.
    def genes(assay):
        return get_genes(assay)
    
    # Return references.
    def references(assay):
        return get_references(assay)
        
    # Return targets.
    def targets(assay):
        print("NOT FUNCTIONAL.")
        
    # Return taxa.
    def taxa(assay):
        return get_taxa(assay)
    
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
    
    def all_properties(assay, user = None):
        property_dict = {}
        return property_dict
    
    # Return assay category.
    def assay_category(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["assay_category"])
        return prop_array
    
    # Return assay subcellular fraction.
    def assay_subcellular_fraction(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["assay_subcellular_fraction"])
        return prop_array
    
    # Return assay test type.
    def assay_test_type(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["assay_test_type"])
        return prop_array
    
    # Return assay type.
    def assay_type(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["assay_type"])
        return prop_array
    
    # Return assay type description.
    def assay_type_description(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["assay_type_description"])
        return prop_array
    
    # Return comments.
    def comment(assay, source = "pubchem"):
        if source == "pubchem":
            comment_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    comment_array.extend(list(filter(None, infrassay["assay"]["descr"]["comment"])))
            return comment_array
        
    # Return confidence description.
    def confidence_description(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["confidence_description"])
        return prop_array
        
    # Return confidence score.
    def confidence_score(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["confidence_score"])
        return prop_array
        
    # Return description.
    def description(assay, source = "pubchem"):
        if source == "pubchem":
            desc_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    desc_array.extend(list(filter(None, infrassay["assay"]["descr"]["description"])))
            return desc_array
    
    # Return protocol.
    def protocol(assay, source = "pubchem"):
        if source == "pubchem":
            protocol_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    protocol_array.extend(list(filter(None, infrassay["assay"]["descr"]["protocol"])))
            return protocol_array
    
    # Return relationship description.
    def relationship_description(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["relationship_description"])
        return prop_array
    
    # Return relationship type.
    def relationship_type(assay):
        prop_array = []
        for x in chembl_assay(assay):
            prop_array.append(x["relationship_type"])
        return prop_array
    
    # Return results.
    def result(assay, source = "pubchem"):
        if source == "pubchem":
            result_array = []
            for subassay in Assay.pubchem_assay(assay):
                for infrassay in subassay["PC_AssayContainer"]:
                    result_array.extend(list(filter(None, infrassay["assay"]["descr"]["results"])))
            return result_array
        
    # Return title.
    def title(assay, source = "openphacts", user = None):
        if source == "openphacts" and user is not None:
            title_array = []
            for obj in Assay.oidd_bioassay(assay, user = user):
                temp_title = obj["primaryTopic"]["exactMatch"]["title"]
                title_array.append(temp_title)

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
    print("Getting assay properties from PubChem AID (%s)..." % pubchem_aid)
    print("Comments:")
    for comment in Assay.comment(pubchem_assay):
        print(comment)
    print("\nDescriptions:")
    for desc in Assay.description(pubchem_assay):
        print(desc)
    print("\nProtocol:")
    for protocol in Assay.protocol(pubchem_assay):
        print(protocol)
    print("\nResults:")
    for result in Assay.result(pubchem_assay):
        print(result)

#   MAIN
if __name__ == "__main__": main()