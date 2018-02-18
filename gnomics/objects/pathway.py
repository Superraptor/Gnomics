#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       GOATOOLS
#           https://github.com/tanghaibao/goatools/
#

#
#   Create instance of a pathway.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import modules.
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.user as user

#   Other imports.
from bioservices import *
from goatools import obo_parser
import requests
import sys

#   Import sub-methods.
from gnomics.objects.pathway_files.bsid import get_bsid
from gnomics.objects.pathway_files.kegg import get_kegg_map_pathway, get_kegg_map_pathway_id, get_kegg_ko_pathway, get_kegg_ko_pathway_id
from gnomics.objects.pathway_files.search import search
from gnomics.objects.pathway_files.wikipathways import get_wikipathways_id

#   Import further methods.
from gnomics.objects.interaction_objects.pathway_biological_process import get_biological_processes
from gnomics.objects.interaction_objects.pathway_cellular_component import get_cellular_components
from gnomics.objects.interaction_objects.pathway_compound import get_compounds
from gnomics.objects.interaction_objects.pathway_disease import get_diseases
from gnomics.objects.interaction_objects.pathway_drug import get_drugs
from gnomics.objects.interaction_objects.pathway_enzyme import get_enzymes
from gnomics.objects.interaction_objects.pathway_molecular_function import get_molecular_functions
from gnomics.objects.interaction_objects.pathway_reference import get_references

#   MAIN
def main():
    pathway_unit_tests()

#   PATHWAY CLASS
class Pathway(object):
    """
        Pathway class:
        
        A biological pathway is a series of interactions 
        among molecules in a cell that leads to a certain 
        product or change in a cell.
        
    """
    
    # BioPAX Ontology of Biological Pathways (BP) BioPortal PURL.
    bp_bioportal_purl = "http://purl.bioontology.org/ontology/BP"
    
    # Pathway Ontology (PW) BioPortal PURL.
    pw_bioportal_purl = "http://purl.bioontology.org/ontology/PW"
    
    # WikiPathways BioPortal PURL.
    wikipathways_bioportal_purl = "http://purl.bioontology.org/ontology/WIKIPATHWAYS"
    
    """
        Pathway attributes:
    
    """
    
    # Initialize the pathway.
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None, taxon=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name,
                'taxon': taxon
            }]
        
        # Initialize dictionary of objects.
        self.pathway_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a pathway.
    def add_identifier(pathway, identifier=None, identifier_type=None, language=None, source=None, name=None, taxon=None):
        pathway.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name,
            'taxon': taxon
        })
        
    """
        Pathway objects:
        
        KEGG KO pathway
        KEGG MAP pathway
        
    """
    
    # Get KO pathway for a given KEGG ko ID.
    # ko = reference pathway highlighting KOs.
    def kegg_ko_pathway(pathway, user=None):
        return get_kegg_ko_pathway(pathway)
    
    # Get KEGG pathway for a given KEGG map ID.
    # map = manually drawn reference pathway.
    def kegg_map_pathway(pathway, user=None):
        return get_kegg_map_pathway(pathway)
    
    """
        Pathway identifiers:
        
        BSID (BioSystems ID)
        KEGG KO PATHWAY identifier
        KEGG MAP PATHWAY identifier
        WikiPathways ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(pathway, user=None):
        Pathway.bsid(pathway, user=user)
        Pathway.kegg_ko_pathway_id(pathway, user=user)
        Pathway.kegg_map_pathway_id(pathway, user=user)
        Pathway.wikipathways_id(pathway, user=user)
        return pathway.identifiers
    
    def bsid(pathway, user=None):
        return get_bsid(pathway)
    
    # Get KEGG PATHWAY KO identifier.
    def kegg_ko_pathway_id(pathway, user=None):
        return get_kegg_ko_pathway_id(pathway)
    
    # Get KEGG PATHWAY MAP identifier.
    def kegg_map_pathway_id(pathway, user=None):
        return get_kegg_map_pathway_id(pathway)
    
    # Get WikiPathways ID.
    def wikipathways_id(pathway, user=None):
        return get_wikipathways_id(pathway)
    
    """
        Interaction objects:
        
        Biological processes
        Cellular components
        Compounds
        Diseases
        Drugs
        Enzymes
        Molecular functions
        References
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(pathway, user=None):
        interaction_obj = {}
        interaction_obj["Biological_Processes"] = Pathway.biological_processes(pathway, user=user)
        interaction_obj["Cellular_Components"] = Pathway.cellular_components(pathway)
        interaction_obj["Compounds"] = Pathway.compounds(pathway, user=user)
        interaction_obj["Diseases"] = Pathway.diseases(pathway, user=user)
        interaction_obj["Drugs"] = Pathway.drugs(pathway, user=user)
        interaction_obj["Enzymes"] = Pathway.enzymes(pathway, user=user)
        interaction_obj["Molecular_Functions"] = Pathway.molecular_functions(pathway, user=user)
        interaction_obj["References"] = Pathway.references(pathway, user=user)
        return interaction_obj
    
    # Get biological processes.
    def biological_processes(pathway, user=None):
        return get_biological_processes(pathway)
    
    # Get cellular components.
    def cellular_components(pathway, user=None):
        return get_cellular_components(pathway)
    
    # Get compounds.
    def compounds(pathway, user=None):
        return get_compounds(pathway)
    
    # Get diseases.
    def diseases(pathway, user=None):
        return get_diseases(pathway)
    
    # Get drugs.
    def drugs(pathway, user=None):
        return get_drugs(pathway)
        
    # Get enzymes.
    def enzymes(pathway, user=None):
        return get_enzymes(pathway)
        
    # Get molecular functions.
    def molecular_functions(pathway, user=None):
        return get_molecular_functions(pathway)
    
    # Get references.
    def references(pathway, user=None):
        return get_references(pathway)
    
    """
        Pathway attributes
        
        Class
        Description
        Name
    """
    
    def all_properties(pathway, user=None):
        property_dict = {}
        property_dict["Name"] = Pathway.name(pathway, user=user)
        property_dict["Class"] = Pathway.pathway_class(pathway, user=user)
        property_dict["Description"] = Pathway.description(pathway, user=user)
        return property_dict
    
    # Get pathway name.
    def name(pathway, user=None):
        prop_array = []
        for obj in Pathway.kegg_map_pathway(pathway):
            if "NAME" in obj:
                for sub_name in obj["NAME"]:
                    prop_array.append(sub_name)
        return prop_array
    
    # Get pathway class.
    def pathway_class(pathway, user=None):
        prop_array = []
        for obj in Pathway.kegg_ko_pathway(pathway):
            if "CLASS" in obj:
                prop_array.append(obj["CLASS"])
        return prop_array
    
    # Get description.
    def description(pathway, user=None):
        prop_array = []
        for obj in Pathway.kegg_ko_pathway(pathway):
            if "DESCRIPTION" in obj:
                prop_array.append(obj["DESCRIPTION"])
        for obj in Pathway.kegg_map_pathway(pathway):
            if "DESCRIPTION" in obj:
                prop_array.append(obj["DESCRIPTION"])
        return prop_array
    
    """
        URLs
        
    """
    
    # Return links.
    def all_urls(pathway, user=None):
        url_dict = {}
        return url_dict
    
    """
        Auxiliary functions
    
        Search
        
    """
    
    def search(query, source="all", result_format="xml", user=None):
        return search(query, source=source, result_format=result_format, user=user)
    
    """
        External files
        
    """
    
#   UNIT TESTS
def pathway_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()