#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Create instance of a compound.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.compound

#   Other imports.
import json
import re
import requests
import signal

#   Import sub-methods.
from gnomics.objects.drug_files.atc import get_atc_codes
from gnomics.objects.drug_files.ban import get_ban
from gnomics.objects.drug_files.drugbank import get_drugbank_id
from gnomics.objects.drug_files.drugcentral import get_drugcentral_id
from gnomics.objects.drug_files.fda import get_fda_id, get_fda_obj
from gnomics.objects.drug_files.inn import get_inns
from gnomics.objects.drug_files.jan import get_jan
from gnomics.objects.drug_files.kegg import get_kegg_drug_id
from gnomics.objects.drug_files.mesh import get_mesh_uid
from gnomics.objects.drug_files.rxcui import get_rxnorm_obj, get_rxcui, get_related_rxcuis
from gnomics.objects.drug_files.search import search
from gnomics.objects.drug_files.trade_names import  get_trade_names
from gnomics.objects.drug_files.usan import get_usan
from gnomics.objects.drug_files.usp import get_usp

#   Import further methods.
from gnomics.objects.interaction_objects.drug_adverse_event import get_adverse_events
from gnomics.objects.interaction_objects.drug_compound import get_compounds
from gnomics.objects.interaction_objects.drug_drug import get_drug_drug_interactions
from gnomics.objects.interaction_objects.drug_gene import get_genes

#   MAIN
def main():
    drug_unit_tests("856834", "0093-0311-01")

#   DRUG CLASS
class Drug(object):
    """
        Drug class:
    
        Representing drug substances, active pharmaceutical
        ingredients, drug products, and formulations.
    
    """
    
    """
        Drug attributes:
        
        Identifier      = A particular way to identify the
                          drug in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the drug.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of drug objects.
        self.drug_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a compound.
    def add_identifier(drug, identifier = None, identifier_type = None, language = None, source = None, name = None):
        drug.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    """
        Drug objects:
        
        FDA Drug Object
        KEGG DRUG
        RxNorm Object
        
    """
    
    # FDA drug object.
    def fda_drug_obj(drug):
        return get_fda_obj(drug)
    
    # KEGG database entry (for drug).
    def kegg_drug_db_entry(drug):
        return get_kegg_drug_db_entry(drug)
    
    # RxNorm object.
    def rxnorm_obj(drug):
        return get_rxnorm_obj(drug)
    
    """
        Drug identifiers:
        
        ATC codes
        BAN
        DrugBank identifier
        FDA drug name
        INN
        JAN
        KEGG drug identifier
        MeSH UID
        Patent accession
        Trade names
        USAN
        USP
        Wikipedia accession
        
    """
    
    # Return all identifiers.
    def all_identifiers(drug, user = None):
        Drug.atc_codes(drug)
        Drug.ban(drug)
        Drug.drugbank_id(drug)
        Drug.drugcentral_id(drug)
        Drug.fda(drug)
        Drug.inn(drug)
        Drug.jan(drug)
        Drug.kegg_drug_id(drug)
        Drug.mesh_uid(drug)
        Drug.rxcui(drug)
        Drug.trade_names(drug)
        Drug.usan(drug)
        Drug.usp(drug)
        return drug.identifiers
    
    # Returns ATC classifications (codes).
    def atc_codes(drug):
        return get_atc_codes(drug)
    
    # Returns BAN (British Accepted Name).
    def ban(drug):
        return get_ban(drug)
    
    # Returns DrugBank identifier.
    def drugbank_id(drug):
        return get_drugbank_id(drug)
    
    # Returns DrugCentral identifier.
    def drugcentral_id(drug):
        return get_drugcentral_id(drug)
    
    # Returns FDA drug name.
    def fda(drug):
        return get_fda_id(drug)
    
    # Returns INNs (International Nonproprietary Names).
    def inn(drug):
        return get_inns(drug)
    
    # Returns JAN (Japanese Accepted Name).
    def jan(drug):
        return get_jan(drug)
    
    # Returns KEGG Drug identifier.
    def kegg_drug_id(drug):
        return get_kegg_drug_id(drug)
    
    # Returns MeSH UID.
    def mesh_uid(drug):
        return get_mesh_uid(drug)
            
    # Returns RxCUIs.
    def rxcui(drug):
        return get_rxcui(drug)
    
    # Returns related RxCUIs.
    def related_rxcui(drug):
        return get_related_rxcuis(drug)
                    
    # Returns trade names.
    def trade_names(drug):
        return get_trade_names(drug)
            
    # Returns USAN (United States Adopted Names).
    def usan(drug):
        return get_usan(drug)
            
    # Returns USP (United States Pharmacopeia).
    def usp(drug):
        return get_usp(drug)
    
    """
        Interaction objects:
        
        Adverse events
        Compounds
        Diseases
        Genes
        Pathways
        References
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(drug, user = None):
        interaction_obj = {}
        interaction_obj["Adverse Events"] = Drug.adverse_events(drug)
        interaction_obj["Compounds"] = Drug.compounds(drug)
        #interaction_obj["Diseases"] = Drug.diseases(drug)
        interaction_obj["Drug Interactions"] = Drug.drug_drug_interactions(drug)
        interaction_obj["Genes"] = Drug.genes(drug, user = user)
        #interaction_obj["Pathways"] = Drug.pathways(drug, user = user)
        #interaction_obj["References"] = Drug.references(drug)
        print(interaction_obj)
        return interaction_obj

    # Returns adverse events.
    def adverse_events(drug, user = None, counts = False, exact = True, all_results = True, limit = 100, details = True):
        return get_adverse_events(drug, user = user, counts = counts, exact = exact, all_results = all_results, limit = limit, details = details)
        
    # Return compound objects.
    def compounds(drug, user = None):
        return get_compounds(drug, user = user)
    
    # Return disease objects.
    def diseases(drug):
        print("NOT FUNCTIONAL.")
        #return get_diseases(drug)
    
    def drug_drug_interactions(drug, source = "Drugbank"):
        return get_drug_drug_interactions(drug, source = source)
    
    # Get gene interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def genes(drug, user = None, source = None, interaction_sources = None, interaction_types = None, gene_categories = None, source_trust_levels = None):
        return get_genes(drug, user = user, source = source, interaction_sources = interaction_sources, interaction_types = interaction_types, gene_categories = gene_categories, source_trust_levels = source_trust_levels)
    
    # Get pathways related to compound (KEGG).
    #
    # For pathway associations, either
    # "inferred" or "enriched" may be used.
    def pathways(drug, source = None, pathway_assoc = None, user = None):
        print("NOT FUNCTIONAL.")
    
    # Returns sources/references.
    def references(drug):
        print("NOT FUNCTIONAL.")
        return get_references(drug)
    
    """
        Other properties:
        
        Active ingredients # Move to Interaction Objects
        Inactive ingredients # Move to Interaction Objects
        SPL product data elements # Move to Interaction Objects
        
        Ask doctor
        Ask doctor or pharmacist
        Available strength
        Do not use
        Dosage and administration
        Dosage and administration table
        Effective time
        Indications and usage
        Is original packager?
        Keep out of reach of children?
        Manufacturer name
        Package label principal display panel
        Prescribable
        Product type
        Purpose
        Questions
        Route
        Stop Use
        Version
        Warnings
        When Using
        
    """
    
    # Return all properties in this category.
    def all_properties(drug, user = None):
        property_dict = {}
        return property_dict
    
    # Return "ask doctor" from label.
    def ask_doctor(drug):
        return fda_drug_obj(drug)["ask_doctor"]
    
    # Return "ask doctor or pharmacist" from label.
    def ask_doctor_or_pharmacist(drug):
        return fda_drug_obj(drug)["ask_doctor_or_pharmacist"]
    
    # Get available strength.
    def available_strength(drug):
        print("NOT FUNCTIONAL.")
    
    # Return "do not use" from label.
    def do_not_use(drug):
        return fda_drug_obj(drug)["do_not_use"]
    
    # Return dosage and administration information.
    def dosage_and_administration(drug):
        return fda_drug_obj(drug)["dosage_and_administration"]
    
    # Return dosage and administration table from label.
    def dosage_and_administration_table(drug):
        return fda_drug_obj(drug)["dosage_and_administration_table"]
    
    # Get effective time.
    def effective_time(drug):
        return fda_drug_obj(drug)["effective_time"]
    
    # Get indications and usage information.
    def indications_and_usage_information(drug):
        return fda_drug_obj(drug)["indications_and_usage"]
    
    # Get whether this is the original packager.
    def is_original_packager(drug):
        return fda_drug_obj(drug)["is_original_packager"]
    
    # Return "keep out of reach of children" statement from label.
    def keep_out_of_reach_of_children(drug):
        return fda_drug_obj(drug)["keep_out_of_reach_of_children"]
    
    # Get manufacturer name.
    def manufacturer_name(drug):
        return fda_drug_obj(drug)["openfda"]["manufacturer_name"]
    
    # Return package label principal display panel.
    def package_label_principal_display_panel(drug):
        return fda_drug_obj(drug)["package_label_principal_display_panel"]
    
    # Get prescribable.
    def prescribable(drug):
        print("NOT FUNCTIONAL.")
        
    # Get product type.
    def product_type(drug):
        return fda_drug_obj(drug)["openfda"]["product_type"]
    
    # Get drug purpose.
    def purpose(drug):
        return fda_drug_obj(drug)["purpose"]
    
    # Get questions.
    def questions(drug):
        return fda_drug_obj(drug)["questions"]
    
    # Get drug route.
    def route(drug):
        return fda_drug_obj(drug)["openfda"]["route"]
    
    # Get "stop use" from product label.
    def stop_use(drug):
        return fda_drug_obj(drug)["stop_use"]
    
    # Get version.
    def version(drug):
        return fda_drug_obj(drug)["version"]
    
    # Get warnings from product label.
    def warnings(drug):
        return fda_drug_obj(drug)["warnings"]
    
    # Get "when using" from product label.
    def when_using(drug):
        return fda_drug_obj(drug)["when_using"]
        
    """
        URLs:
        
        DrugBank URL
        KEGG Drug URL
        
    """
    
    # Returns DrugBank URL.
    def drugbank_url(drug):
        return "https://www.drugbank.ca/drugs/" + str(Drug.drugbank_id(drug))
    
    # Returns KEGG Drug URL.
    def kegg_drug_url(drug):
        return "http://www.genome.jp/dbget-bin/www_bget?dr:" + str(Drug.kegg_drug_id(drug))
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Returns compounds by search.
    # http://chemspipy.readthedocs.io/en/latest/guide/searching.html
    #
    # Can use SMILES, common name, or ChemSpider identifier.
    # May return many results.
    #
    # Note that searching by mass has a default range of +/- 0.001.
    #
    # PubChem search is also included, but is not currently
    # fully documented.
    def search(query, search_type = "exact", source = "rxnorm", user = None):
        return search(query, search_type = search_type, source = source)
    
    """
        External files:
        
        Images
    """
    
    # Return images.
    #
    # Pattern options off of:
    # https://rximage.nlm.nih.gov/index/visualizer/
    #
    # Ex: https://rximage.nlm.nih.gov/api/rximage/1/rxnav?&resolution=full&rxcui=856834
    #
    # Resource: rxnav, rxbase, enum
    # Reply Format: JSON, XML
    # Color: BLACK, BLUE, BROWN, GRAY, GREEN, ORANGE, PINK, PURPLE, RED, TURQUOISE, WHITE, YELLOW (or any combo of these)
    # Score: ANY, 1, 2, 3, 4
    # Shape:
    # Symbol:
    # Size:
    # SizeT:
    # Imprint:
    # ImprintType:
    # ImprintColor:
    # NDC:
    # MatchPackSize:
    # MatchRelabeled:
    # RxCUI:
    # ID:
    # SetID:
    # RootID:
    # Name:
    # Inactive:
    # Parse:
    def images(drug, resource = "rxnav", reply_format = "json", color = None, resolution = "full"):
        base = "https://rximage.nlm.nih.gov/api/"
        image_url_array = []
        for ident in drug.identifiers:
            if ident["identifier_type"].lower() == "rxcui":
                ext = "rximage/1/" + resource + "?&resolution=" + resolution + "&rxcui=" + ident["identifier"] 
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                for im in decoded["nlmRxImages"]:
                    image_url_array.append(im["imageUrl"])
            if ident["identifier_type"].lower() == "ndc" or ident["identifier_type"].lower() == "national drug code":
                ext = "rximage/1/" + resource + "?&resolution=" + resolution + "&ndc=" + ident["identifier"] 
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                for im in decoded["nlmRxImages"]:
                    image_url_array.append(im["imageUrl"])
        return image_url_array
        
#   UNIT TESTS
def drug_unit_tests(rxcui, ndc):
    rx_drug = Drug(identifier = rxcui, identifier_type = "RxCUI", language = None, source = "RxNorm")
    print("Getting drug images from RxCUI (%s):" % rxcui)
    for imag in Drug.images(rx_drug):
        print("- %s" % str(imag))
    ndc_drug = Drug(identifier = ndc, identifier_type = "NDC", language = None, source = "FDA")
    print("\nGetting drug images from NDC (%s):" % ndc)
    for imag in Drug.images(ndc_drug):
        print("- %s" % str(imag))

#   MAIN
if __name__ == "__main__": main()