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

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

#   Import modules.
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.user as user

#   Other imports.
from goatools import obo_parser
import requests

# Import sub-methods.
from gnomics.objects.pathway_files.kegg import get_kegg_map_pathway, get_kegg_map_pathway_id, get_kegg_ko_pathway, get_kegg_ko_pathway_id

#   Import further methods.
from gnomics.objects.interaction_objects.pathway_compound import get_compounds
from gnomics.objects.interaction_objects.pathway_reference import get_references

#   MAIN
def main():
    pathway_unit_tests()
    

#   PATHWAY CLASS
class Pathway(object):
    """
        Pathway class:
        
        
        
    """
    
    """
        Pathway attributes:
    
    """
    
    # Initialize the pathway.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None, taxon = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name,
                'taxon': taxon
            }
        ]
        
        # Initialize dictionary of objects.
        self.pathway_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a pathway.
    def add_identifier(pathway, identifier = None, identifier_type = None, language = None, source = None, name = None, taxon = None):
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
        
        Ensembl GO accession
        KEGG KO pathway
        KEGG MAP pathway
        KEGG orthology
        QuickGO
        
    """
    
    # Get KO pathway for a given KEGG ko ID.
    # ko = reference pathway highlighting KOs.
    def kegg_ko_pathway(pathway):
        return get_kegg_ko_pathway(pathway)
    
    # Get KEGG pathway for a given KEGG map ID.
    # map = manually drawn reference pathway.
    def kegg_map_pathway(pathway):
        return get_kegg_map_pathway(pathway)
    
    # Get Ensembl information from GO accession.
    # Based off of documentation here:
    # https://rest.ensembl.org/documentation/info/ontology_id
    # In addition, example located here:
    # https://rest.ensembl.org/ontology/id/GO:0005667?content-type=application/json
    def ensembl_go(pathway):
        server = "https://rest.ensembl.org"
        ext = "/ontology/id/GO:" + str(Pathway.go_accession(pathway)) + "?"
        r = requests.get(server + ext, headers = {
            "Content-Type" : "application/json"
        })
        if not r.ok:
            r.raise_for_status()
            sys.exit
        decoded = r.json()
        return decoded
    
    # Get KEGG orthology object.
    def kegg_orthology_object(pathway):
        return gnomics.objects.auxiliary_files.kegg.get_kegg_orthology(pathway)
    
    # Get QuickGO object from GO accession.
    def quick_go(pathway, go_accession):
        g = QuickGO(verbose = False)
        return(g.Term(go_accession, frmt = "obo"))
    
    """
        Pathway identifiers:
        
        BSID
        GO accession
        KEGG KO identifier
        KEGG MAP identifier
        
    """
    
    # Return all identifiers.
    def all_identifiers(pathway, user = None):
        Pathway.kegg_ko_id(pathway)
        Pathway.kegg_map_id(pathway)
        return pathway.identifiers
    
    # Get BSID.
    def bsid(pathway, source = "kegg", identifier_type = "ko"):
        if source == "kegg" and identifier_type == "ko":
            return Pathway.kegg_map_pathway(pathway)["DBLINKS"]["BSID"]
    
    # Get GO accession.
    def go_accession(pathway, source = "kegg", identifier_type = "map"):
        if source == "kegg" and identifier_type == "map":
            return Pathway.kegg_map_pathway(pathway)["DBLINKS"]["GO"]
        elif source == "kegg" and identifier_type == "ko":
            return Pathway.kegg_ko_pathway(pathway)["DBLINKS"]["GO"]
    
    # Get KEGG KO identifier.
    def kegg_ko_id(pathway):
        return get_kegg_ko_pathway_id(pathway)
    
    # Get KEGG MAP identifier.
    def kegg_map_id(pathway):
        return get_kegg_map_pathway_id(pathway)
    
    """
        Pathway attributes
        
        
    """
    
    # Get compounds related to pathway.
    def compounds(pathway, source = "kegg", identifier_type = "ko"):
        if source == "kegg" and identifier_type == "ko":
            compound_array = []
            for kegg_com, norm_name in Pathway.kegg_ko_pathway(pathway)["COMPOUND"]:
                if "C" in kegg_com:
                    temp_compound = compound.Compound(identifier = compound, identifier_type = "KEGG COMPOUND accession", source = "KEGG")
                    compound_array.append(temp_compound)
                elif "D" in kegg_com:
                    temp_compound = compound.Compound(identifier = compound, identifier_type = "KEGG DRUG accession", source = "KEGG")
                    compound_array.append(temp_compound)
    
    # Get pathway name.
    def name(pathway, source = "kegg", identifier_type = "map"):
        if source == "kegg" and prefix == "map":
            return Pathway.kegg_map_pathway(pathway)["NAME"]
    
    # Get pathway class.
    def pathway_class(pathway):
        return Pathway.kegg_ko_pathway(pathway)["CLASS"]
    
    # Get description.
    def description(self, source = "kegg", identifier_type = "map"):
        if source == "kegg" and identifier_type == "map":
            return Pathway.kegg_map_pathway(pathway)["DESCRIPTION"]
        elif source == "kegg" and identifier_type == "ko":
            return Pathway.kegg_ko_pathway(pathway)["DESCRIPTION"]

    # Get related diseases.
    def diseases(pathway, source = "kegg", identifier_type = "map"):
        if source == "kegg" and identifier_type == "map":
            return Pathway.kegg_map_pathway(pathway)["DISEASE"]
        elif source == "kegg" and identifier_type == "ko":
            return Pathway.kegg_ko_pathway(pathway)["DISEASE"]
    
    # Get KEGG disease IDs.
    def kegg_disease_ids(pathway, source = "kegg", identifier_type = "map"):
        disease_array = []
        for identifier, name in Pathway.diseases(pathway, source = source, identifier_type = identifier_type).items():
            disease_array.append(identifier)
        return disease_array
    
    # Get KEGG orthology, which includes what are considered "molecular-level" functions.
    def kegg_orthology(pathway):
        ortho_array = []
        for ortho in Pathway.kegg_ko_pathway(pathway):
            if ortho["ORTHOLOGY"] not in ortho_array:
                ortho_array.append(ortho["ORTHOLOGY"])
        return ortho_array
    
    # Get EC numbers from KEGG orthology.
    def kegg_orthology_ec_numbers(pathway):
        ec_numbers = []
        for identifier, name in Pathway.kegg_orthology(pathway).items():
            capture_ec = re.compile("^(\[EC:(.*?)\])$")
            if capture_ec:
                ec_string = capture_ec[0].split("EC:")[1]
                ec_numbers.append(ec_string)
        return ec_numbers
    
    # Get KEGG orthology IDs.
    def kegg_orthology_ids(pathway):
        kegg_orthology_id_array = []
        for subpath in Pathway.kegg_orthology(pathway):
            for identifier, name in subpath.items():
                if identifier not in kegg_orthology_id_array:
                    kegg_orthology_id_array.append(identifier)
        return kegg_orthology_id_array
    
    # Return references as array.
    def references(pathway, source = "kegg", identifier_type = "map"):
        if source == "kegg" and identifier_type == "map":
            return Pathway.kegg_map_pathway(pathway)["REFERENCE"]
        elif source == "kegg" and identifier_type == "ko":
            return Pathway.kegg_ko_pathway(pathway)["REFERENCE"]
    
    """
        URLs
    """
    
    # Returns GO-REACTOME URL.
    def reactome_go_url(pathway):
        return "http://www.reactome.org/content/query?cluster=true&q=" + str(Pathway.go_accession(pathway))
    
    
#   MAIN
if __name__ == "__main__": main()