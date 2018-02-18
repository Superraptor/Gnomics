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
#

#
#   Create instance of a cellular component.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Other imports.
from bioservices import QuickGO
import timeit

#   Import sub-methods.
from gnomics.objects.cellular_component_files.go import get_go_accession, get_quickgo_obj
from gnomics.objects.cellular_component_files.search import search
from gnomics.objects.cellular_component_files.uniprot import get_uniprotkb_kw
from gnomics.objects.cellular_component_files.wiki import get_english_wikipedia_accession

#   Import further methods.
from gnomics.objects.interaction_objects.cellular_component_protein_family import get_protein_families

#   MAIN
def main():
    cellular_component_unit_tests()

#   CELLULAR COMPONENT CLASS
class CellularComponent:
    """
        Cellular component class
        
        Cellular components are unique, highly
        organized substances of which cells and
        living organisms are composed.
    """
    
    # GO BioPortal PURL.
    go_bioportal_purl = "http://purl.bioontology.org/ontology/GO"
    
    """
        Cellular component attributes:
        
        Identifier      = A particular way to identify the
                          cellular component in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the cellular component.
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of cellular comonent objects.
        self.cellular_component_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a cellular_component.
    def add_identifier(cellular_component, identifier=None, identifier_type=None, language=None, source=None, name=None):
        cellular_component.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a cellular component.
    def add_object(cellular_component, obj=None, object_type=None):
        cellular_component.cellular_component_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Cellular component objects
        
        QuickGO Object
        
    """
    
    # Return Ensembl GO object.
    #
    # TODO: move to ensembl.py in cellular_component_files
    def ensembl_go(cellular_component):
        ens_obj_array = []
    
        for ens_obj in cellular_component.cellular_component_objects:
            if 'object_type' in ens_obj:
                if ens_obj['object_type'].lower() in ['ensembl', 'ensembl go', 'ensembl object', 'ensembl go object']:
                    ens_obj_array.append(ens_obj['object'])

        if ens_obj_array:
            return ens_obj_array
        
        for acc in CellularComponent.go_accession(cellular_component):
            proc_acc = acc
            if "_" in proc_acc:
                proc_acc = proc_acc.replace("_", ":")
            
            server = "https://rest.ensembl.org"
            ext = "/ontology/id/GO:" + str(proc_acc) + "?"
            r = requests.get(server + ext, headers = {
                "Content-Type" : "application/json"
            })

            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                ens_obj_array.append(decoded)
                gnomics.objects.cellular_component.CellularComponent.add_object(cellular_component, obj = decoded, object_type = "Ensembl Object")
                
        return ens_obj_array
    
    # Return QuickGO object.
    def quickgo(cellular_component, user=None):
        return get_quickgo_obj(cellular_component)
    
    """
        Cellular component identifiers
        
        GO Accession
        UniProtKB Keywords
        Wikipedia Accession
    
    """
    
    # Return all identifiers.
    def all_identifiers(cellular_component, user=None):
        CellularComponent.go_accession(cellular_component, user=user)
        CellularComponent.uniprotkb_kw(cellular_component, user=user)
        CellularComponent.wikipedia_accession(cellular_component, language="english", user=user)
        return cellular_component.identifiers
    
    # Return GO accession.
    def go_accession(cellular_component, user=None):
        return get_go_accession(cellular_component)
    
    # Return UniProtKB-KW (keywords).
    def uniprotkb_kw(cellular_component, user=None):
        return get_uniprotkb_kw(cellular_component)
    
    # Return Wikipedia accession.
    def wikipedia_accession(molecular_function, language="en", user=None):
        if language.lower() in ["eng", "en", "english", "all"]:
            return get_english_wikipedia_accession(molecular_function)
        else:
            print("The given language is not currently supported.")
    
    """
        Interaction objects
        
        Protein families
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(cellular_component, user=None):
        interaction_obj = {}
        interaction_obj["Protein_Families"] = CellularComponent.protein_families(cellular_component, user=user)
        return interaction_obj
    
    # Return protein families.
    def protein_families(cellular_component, user=None):
        return get_protein_families(cellular_component)
    
    """
        Other properties
        
        Definition
        
    """
    
    def all_properties(cellular_component, user=None):
        property_dict = {}
        property_dict["Definition"] = CellularComponent.definition(cellular_component)
        return property_dict
    
    # Return definition.
    def definition(cellular_component, user=None):
        def_array = []
        for obj in CellularComponent.quickgo(cellular_component):
            def_array.append(obj["definition"])
        return def_array
    
    """
        Cellular component URLs
        
        GO-REACTOME URL
    """
    
    # Return links.
    def all_urls(cellular_component, user=None):
        url_dict = {}
        url_dict["GO-REACTOME"] = CellularComponent.reactome_go_url(cellular_component, user=user)
        return url_dict
    
    # Returns GO-REACTOME URL.
    def reactome_go_url(cellular_component, user=None):
        url_array = []
        for go_acc in CellularComponent.go_accession(cellular_component):
            url_array.append("http://www.reactome.org/content/query?cluster=true&q=" + str(self.go_acc))
        return url_array
    
    """
        Auxiliary functions
    
        Search
        
    """
    
    def search(query, search_type="exact", user=None):
        return search(query, search_type=search_type)
    
    """
        External files
        
    """

#   UNIT TESTS
def cellular_component_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()