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
#   Create instance of a biological process.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.biological_process_files.go import get_go_accession, get_quickgo_obj
from gnomics.objects.biological_process_files.search import search
from gnomics.objects.biological_process_files.wiki import get_english_wikipedia_accession

#   Other imports.
from bioservices import QuickGO
import timeit

#   MAIN
def main():
    biological_process_unit_tests()

#   BIOLOGICAL PROCESS CLASS
class BiologicalProcess:
    """
        Biological process class
        
        Biological processes are the processes
        vital for a living organism to live.
    """
    
    # GO BioPortal PURL.
    go_bioportal_purl = "http://purl.bioontology.org/ontology/GO"
    
    """
        Biological process attributes:
        
        Identifier      = A particular way to identify the
                          biological process in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the biological process.
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
        
        # Initialize dictionary of biological process objects.
        self.biological_process_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a biological process.
    def add_identifier(biological_process, identifier=None, identifier_type=None, language=None, source=None, name=None):
        biological_process.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a biological process.
    def add_object(biological_process, obj=None, object_type=None):
        biological_process.biological_process_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Biological process objects
        
        QuickGO Object
        
    """
    
    # Return Ensembl GO object.
    def ensembl_go(biological_process):
        ens_obj_array = []
    
        for ens_obj in biological_process.biological_process_objects:
            if 'object_type' in ens_obj:
                if ens_obj['object_type'].lower() in ['ensembl', 'ensembl go', 'ensembl object', 'ensembl go object']:
                    ens_obj_array.append(ens_obj['object'])

        if ens_obj_array:
            return ens_obj_array
        
        for acc in BiologicalProcess.go_accession(biological_process):
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
                gnomics.objects.biological_process.BiologicalProcess.add_object(biological_process, obj = decoded, object_type = "Ensembl Object")
                
        return ens_obj_array
    
    # Return QuickGO object.
    def quickgo(biological_process):
        return get_quickgo_obj(biological_process)
    
    """
        Biological process identifiers
    
        GO Accession
        Wikipedia Accession
    
    """
    
    # Return all identifiers.
    def all_identifiers(biological_process, user=None):
        BiologicalProcess.go_accession(biological_process)
        BiologicalProcess.wikipedia_accession(biological_process, language="english")
        return biological_process.identifiers
    
    # Return GO accession.
    def go_accession(biological_process):
        return get_go_accession(biological_process)
    
    # Return Wikipedia accession.
    def wikipedia_accession(biological_process, language="en"):
        if language == "eng" or language == "en" or language.lower() == "english":
            return get_english_wikipedia_accession(biological_process)
        else:
            print("The given language is not currently supported.")
    
    """
        Interaction objects
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(biological_process, user=None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties
        
        Definition
        
    """
    
    def all_properties(biological_process, user=None):
        property_dict = {}
        property_dict["Definition"] = BiologicalProcess.definition(biological_process)
        return property_dict
    
    # Return definition
    def definition(biological_process):
        def_array = []
        for obj in BiologicalProcess.quickgo(biological_process):
            def_array.append(obj["definition"])
        return def_array
    
    """
        URLs:
        
        GO-REACTOME URL
    """
    
    # Return links.
    def all_urls(biological_process, user=None):
        url_dict = {}
        url_dict["GO-REACTOME"] = biological_process.reactome_go_url(biological_process, user=user)
        return url_dict
    
    # Returns GO-REACTOME URL.
    def reactome_go_url(biological_process, user=None):
        url_array = []
        for go_acc in BiologicalProcess.go_accession(biological_process):
            url_array.append("http://www.reactome.org/content/query?cluster=true&q=" + str(self.go_acc))
        return url_array
    
    """
        Auxiliary functions
    
        Search
        
    """
    
    def search(query, search_type="exact", user=None):
        return search(query, search_type = search_type)
    
    """
        External files
        
    """

#   UNIT TESTS
def biological_process_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()