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
#   Create instance of a molecular function.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import modules.
from gnomics.objects.user import User

#   Other imports.
from bioservices import QuickGO
import timeit

#   Import sub-methods.
from gnomics.objects.molecular_function_files.go import get_go_accession, get_quickgo_obj
from gnomics.objects.molecular_function_files.ncit import get_nci_thesaurus_id, get_nci_synonyms
from gnomics.objects.molecular_function_files.kegg import get_kegg_orthology
from gnomics.objects.molecular_function_files.search import search
from gnomics.objects.molecular_function_files.uniprot import get_uniprotkb_kw
from gnomics.objects.molecular_function_files.wiki import get_english_wikipedia_accession

#   Import further methods.
from gnomics.objects.interaction_objects.molecular_function_enzyme import get_enzymes
from gnomics.objects.interaction_objects.molecular_function_gene import get_genes
from gnomics.objects.interaction_objects.molecular_function_pathway import get_pathways
from gnomics.objects.interaction_objects.molecular_function_protein_family import get_protein_families
from gnomics.objects.interaction_objects.molecular_function_reference import get_references

#   MAIN
def main():
    molecular_function_unit_tests()

#   MOLECULAR FUNCTION CLASS
class MolecularFunction:
    """
        Molecular function class
        
        Molecular functions are the elemental activities of
        a gene product at the molecular level, such as 
        binding or catalysis.
    """
    
    # GO BioPortal PURL.
    go_bioportal_purl = "http://purl.bioontology.org/ontology/GO"
    
    # NCIT BioPortal PURL.
    ncit_bioportal_purl = "http://purl.bioontology.org/ontology/NCIT"
    
    """
        Molecular function attributes:
        
        Identifier      = A particular way to identify the
                          molecular function in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the molecular function.
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
        
        # Initialize dictionary of molecular function objects.
        self.molecular_function_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a molecular function.
    def add_identifier(molecular_function, identifier=None, identifier_type=None, language=None, source=None, name=None):
        molecular_function.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a molecular function.
    def add_object(molecular_function, obj=None, object_type=None):
        molecular_function.molecular_function_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Molecular function objects
        
        Ensembl GO Object
        KEGG ORTHOLOGY
        QuickGO Object
        
    """
    
    # Return Ensembl GO object.
    def ensembl_go(molecular_function, user=None):
        ens_obj_array = []
    
        for ens_obj in molecular_function.molecular_function_objects:
            if 'object_type' in ens_obj:
                if ens_obj['object_type'].lower() in ['ensembl', 'ensembl go', 'ensembl object', 'ensembl go object']:
                    ens_obj_array.append(ens_obj['object'])

        if ens_obj_array:
            return ens_obj_array
        
        for acc in MolecularFunction.go_accession(molecular_function):
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
                gnomics.objects.molecular_function.MolecularFunction.add_object(molecular_function, obj = decoded, object_type = "Ensembl Object")
                
        return ens_obj_array
    
    # Return KEGG ORTHOLOGY object.
    def kegg_orthology(molecular_function, user=None):
        return get_kegg_orthology(molecular_function)
    
    # Return QuickGO object.
    def quickgo(molecular_function, user=None):
        return get_quickgo_obj(molecular_function)
    
    """
        Molecular function identifiers
    
        GO Accession
        NCI Thesaurus ID
        NCI Thesaurus Synonyms
        UniProtKB Keywords
        Wikipedia Accession (English)
    
    """
    
    # Return all identifiers.
    def all_identifiers(molecular_function, user=None):
        MolecularFunction.go_accession(molecular_function, user=user)
        MolecularFunction.nci_thesaurus_id(molecular_function, user=user)
        MolecularFunction.nci_thesaurus_synonyms(molecular_function, user=user)
        MolecularFunction.uniprotkb_kw(molecular_function, user=user)
        MolecularFunction.wikipedia_accession(molecular_function, language="english", user=user)
        return molecular_function.identifiers
    
    # Return GO Accession.
    def go_accession(molecular_function, user=None):
        return get_go_accession(molecular_function)
    
    # Return NCI Thesaurus ID.
    def nci_thesaurus_id(molecular_function, user=None):
        return get_nci_thesaurus_id(molecular_function)
        
    # Return NCI Thesaurus synonyms.
    def nci_thesaurus_synonyms(molecular_function, user=None):
        return get_nci_synonyms(molecular_function)
    
    # Return UniProtKB-KW (keywords).
    def uniprotkb_kw(molecular_function, user=None):
        return get_uniprotkb_kw(molecular_function)
    
    # Return Wikipedia accession.
    def wikipedia_accession(molecular_function, language="en", user=None):
        if language.lower() in ["eng", "en", "english", "all"]:
            return get_english_wikipedia_accession(molecular_function)
        else:
            print("The given language is not currently supported.")
    
    """
        Interaction objects
        
        Enzymes
        Genes
        Pathways
        Protein families
        References
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(molecular_function, user=None):
        interaction_obj = {}
        interaction_obj["Protein_Families"] = MolecularFunction.protein_families(molecular_function, user=user)
        return interaction_obj
    
    # Return enzymes.
    def enzymes(molecular_function, user=None):
        return get_enzymes(molecular_function)
    
    # Return genes.
    def genes(molecular_function, user=None):
        return get_genes(molecular_function)
    
    # Return pathways.
    def pathways(molecular_function, user=None):
        return get_pathways(molecular_function)
    
    # Return protein families.
    def protein_families(molecular_function, user=None):
        return get_protein_families(molecular_function)
    
    # Return references.
    def references(molecular_function, user=None):
        return get_references(molecular_function)
    
    """
        Other properties
        
        Definition
        
    """
    
    def all_properties(molecular_function, user=None):
        property_dict = {}
        property_dict["Definition"] = MolecularFunction.definition(molecular_function, user=user)
        return property_dict
    
    # Return definition.
    def definition(molecular_function, user=None):
        def_array = []
        for obj in MolecularFunction.quickgo(molecular_function):
            def_array.append(obj["definition"])
        for obj in MolecularFunction.kegg_orthology(molecular_function):
            def_array.append(obj["DEFINITION"])
        return def_array
    
    """
        Molecular function URLs
        
        GO-REACTOME URL
    """
    
    # Return links.
    def all_urls(molecular_function, user=None):
        url_dict = {}
        return url_dict
    
    # Returns GO-REACTOME URL.
    def reactome_go_url(molecular_function, user=None):
        url_array = []
        for go_acc in MolecularFunction.go_accession(molecular_function):
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
def molecular_function_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()