#!/usr/bin/env python

#
#   DISCLAIMERS:
#   Do not rely on openFDA to make decisions regarding 
#   medical care. Always speak to your health provider 
#   about the risks and benefits of FDA-regulated products.
#

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       WIKIPEDIA
#           https://pypi.python.org/pypi/wikipedia
#

#
#   Create instance of a drug.
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
import gnomics.objects.clinical_trial
import gnomics.objects.compound

#   Other imports.
from bioservices import *
from chembl_webresource_client.new_client import new_client
import json
import re
import requests
import signal
import timeit
import wikipedia

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
    
    # ATC BioPortal PURL.
    atc_bioportal_purl = "http://purl.bioontology.org/ontology/ATC"
    
    # NDDF BioPortal PURL.
    nddf_bioportal_purl = "http://purl.bioontology.org/ontology/NDDF"
    
    # MESH BioPortal PURL.
    mesh_bioportal_purl = "http://purl.bioontology.org/ontology/MESH"
    
    # RxNORM BioPortal PURL.
    rxnorm_bioportal_purl = "http://purl.bioontology.org/ontology/RXNORM"
    
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
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of drug objects.
        self.drug_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a compound.
    def add_identifier(drug, identifier=None, identifier_type=None, language=None, source=None, name=None):
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
    def fda_drug_obj(drug, user=None):
        return get_fda_obj(drug)
    
    # KEGG database entry (for drug).
    def kegg_drug_db_entry(drug, user=None):
        return get_kegg_drug_db_entry(drug)
    
    # RxNorm object.
    def rxnorm_obj(drug, user=None):
        return get_rxnorm_obj(drug)
    
    """
        Drug identifiers:
        
        ATC codes
        BAN
        DrugBank identifier
        FDA drug name
        INN
        JAN
        KEGG DRUG identifier
        MeSH UID
        RxCUI
        Trade names
        USAN
        USP
        Wikipedia accession
        
    """
    
    # Return all identifiers.
    def all_identifiers(drug, user=None):
        Drug.atc_codes(drug, user=user)
        Drug.ban(drug, user=user)
        Drug.drugbank_id(drug, user=user)
        Drug.drugcentral_id(drug, user=user)
        Drug.fda(drug, user=user)
        Drug.inn(drug, user=user)
        Drug.jan(drug, user=user)
        Drug.kegg_drug_id(drug, user=user)
        Drug.mesh_uid(drug, user=user)
        Drug.rxcui(drug, user=user)
        Drug.trade_names(drug, user=user)
        Drug.usan(drug, user=user)
        Drug.usp(drug, user=user)
        return drug.identifiers
    
    # Returns ATC classifications (codes).
    def atc_codes(drug, user=None):
        return get_atc_codes(drug)
    
    # Returns BAN (British Accepted Name).
    def ban(drug, user=None):
        return get_ban(drug)
    
    # Returns DrugBank identifier.
    def drugbank_id(drug, user=None):
        return get_drugbank_id(drug)
    
    # Returns DrugCentral identifier.
    def drugcentral_id(drug, user=None):
        return get_drugcentral_id(drug)
    
    # Returns FDA drug name.
    def fda(drug, user=None):
        return get_fda_id(drug)
    
    # Returns INNs (International Nonproprietary Names).
    def inn(drug, user=None):
        return get_inns(drug)
    
    # Returns JAN (Japanese Accepted Name).
    def jan(drug, user=None):
        return get_jan(drug)
    
    # Returns KEGG Drug identifier.
    def kegg_drug_id(drug, user=None):
        return get_kegg_drug_id(drug)
    
    # Returns MeSH UID.
    def mesh_uid(drug, user=None):
        return get_mesh_uid(drug)
            
    # Returns RxCUIs.
    def rxcui(drug, user=None):
        return get_rxcui(drug)
    
    # Returns related RxCUIs.
    def related_rxcui(drug, user=None):
        return get_related_rxcuis(drug)
                    
    # Returns trade names.
    def trade_names(drug, user=None):
        return get_trade_names(drug)
            
    # Returns USAN (United States Adopted Names).
    def usan(drug, user=None):
        return get_usan(drug)
            
    # Returns USP (United States Pharmacopeia).
    def usp(drug, user=None):
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
    def all_interaction_objects(drug, user=None):
        interaction_obj = {}
        interaction_obj["Adverse_Events"] = Drug.adverse_events(drug, user=user)
        interaction_obj["Compounds"] = Drug.compounds(drug, user=user)
        interaction_obj["Drug_Interactions"] = Drug.drug_interactions(drug, user=user)
        interaction_obj["Gene_Interactions"] = Drug.gene_interactions(drug, user=user)
        print(interaction_obj)
        return interaction_obj

    # Returns adverse events.
    def adverse_events(drug, user=None, counts=False, exact=True, all_results=True, limit=100, details=True):
        return get_adverse_events(drug, user=user, counts=counts, exact=exact, all_results=all_results, limit=limit, details=details)
        
    # Return compound objects.
    def compounds(drug, user=None):
        return get_compounds(drug, user=user)
    
    # Return disease objects.
    def diseases(drug, user=None):
        print("NOT FUNCTIONAL.")
    
    # Return drug-drug interactions (DDIs).
    def drug_interactions(drug, source="Drugbank", user=None):
        return get_drug_drug_interactions(drug, source=source)
    
    # Get gene interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def gene_interactions(drug, user=None, source=None, interaction_sources=None, interaction_types=None, gene_categories=None, source_trust_levels=None):
        return get_genes(drug, user=user, source=source, interaction_sources=interaction_sources, interaction_types=interaction_types, gene_categories=gene_categories, source_trust_levels=source_trust_levels)
    
    # Get pathways related to compound (KEGG).
    #
    # For pathway associations, either
    # "inferred" or "enriched" may be used.
    def pathways(drug, source=None, pathway_assoc=None, user=None):
        print("NOT FUNCTIONAL.")
    
    # Returns sources/references.
    def references(drug, user=None):
        print("NOT FUNCTIONAL.")
    
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
        Prescribable?
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
    def all_properties(drug, user=None):
        property_dict = {}
        property_dict["Ask Doctor"] = Drug.ask_doctor(drug, user=user)
        property_dict["Ask Doctor or Pharmacist"] = Drug.ask_doctor_or_pharmacist(drug, user=user)
        property_dict["Do Not Use"] = Drug.do_not_use(drug, user=user)
        property_dict["Dosage and Administration"] = Drug.dosage_and_administration(drug, user=user)
        property_dict["Effective Time"] = Drug.effective_time(drug, user=user)
        property_dict["Indication and Usage Information"] = Drug.indications_and_usage_information(drug, user=user)
        property_dict["Is Original Packager?"] = Drug.is_original_packager(drug, user=user)
        property_dict["Keep Out of Reach of Children?"] = Drug.keep_out_of_reach_of_children(drug, user=user)
        property_dict["Manufacturer Name"] = Drug.manufacturer_name(drug, user=user)
        property_dict["Package Label Principal Display Panel"] = Drug.package_label_principal_display_panel(drug, user=user)
        property_dict["Prescribable?"] = Drug.prescribable(drug, user=user)
        property_dict["Product Type"] = Drug.product_type(drug, user=user)
        property_dict["Purpose"] = Drug.purpose(drug, user=user)
        property_dict["Questions"] = Drug.questions(drug, user=user)
        property_dict["Route"] = Drug.route(drug, user=user)
        property_dict["Stop Use"] = Drug.stop_use(drug, user=user)
        property_dict["Version"] = Drug.version(drug, user=user)
        property_dict["Warnings"] = Drug.warnings(drug, user=user)
        property_dict["When Using"] = Drug.when_using(drug, user=user)
        return property_dict
    
    # Return "ask doctor" from label.
    def ask_doctor(drug, user=None):
        #print(str(Drug.fda_drug_obj(drug)).encode('ascii', 'ignore').decode())
        if "ask_doctor" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["ask_doctor"]]
        else:
            return []
    
    # Return "ask doctor or pharmacist" from label.
    def ask_doctor_or_pharmacist(drug, user=None):
        if "ask_doctor_or_pharmacist" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["ask_doctor_or_pharmacist"]]
        else:
            return []
    
    # Get available strength.
    def available_strength(drug, user=None):
        print("NOT FUNCTIONAL.")
        return []
    
    # Return "do not use" from label.
    def do_not_use(drug, user=None):
        if "do_not_use" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["do_not_use"]]
        else:
            return []
    
    # Return dosage and administration information.
    def dosage_and_administration(drug, user=None):
        if "dosage_and_administration" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["dosage_and_administration"]
        else:
            return []
    
    # Return dosage and administration table from label.
    def dosage_and_administration_table(drug, user=None):
        if "dosage_and_administration_table" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["dosage_and_administration_table"]]
        else:
            return []
    
    # Get effective time.
    def effective_time(drug, user=None):
        if "effective_time" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["effective_time"]]
        else:
            return []
    
    # Get indications and usage information.
    def indications_and_usage_information(drug, user=None):
        if "indications_and_usage" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["indications_and_usage"]
        else:
            return []
    
    # Get whether this is the original packager.
    def is_original_packager(drug, user=None):
        if "is_original_packager" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["is_original_packager"]]
        else:
            return []
    
    # Return "keep out of reach of children" statement from label.
    def keep_out_of_reach_of_children(drug, user=None):
        if "keep_out_of_reach_of_children" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["keep_out_of_reach_of_children"]]
        else:
            return []
    
    # Get manufacturer name.
    def manufacturer_name(drug, user=None):
        if "openfda" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["openfda"]["manufacturer_name"]
        else:
            return []
    
    # Return package label principal display panel.
    def package_label_principal_display_panel(drug, user=None):
        if "package_label_principal_display_panel" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["package_label_principal_display_panel"]
        else:
            return []
    
    # Get prescribable.
    def prescribable(drug, user=None):
        print("NOT FUNCTIONAL.")
        return []
        
    # Get product type.
    def product_type(drug, user=None):
        if "product_type" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["openfda"]["product_type"]]
        else:
            return []
    
    # Get drug purpose.
    def purpose(drug, user=None):
        if "purpose" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["purpose"]]
        else:
            return []
    
    # Get questions.
    def questions(drug, user=None):
        if "questions" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["questions"]]
        else:
            return []
    
    # Get drug route.
    def route(drug, user=None):
        if "openfda" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["openfda"]["route"]
        else:
            return []
    
    # Get "stop use" from product label.
    def stop_use(drug, user=None):
        if "stop_use" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["stop_use"]]
        else:
            return []
    
    # Get version.
    def version(drug, user=None):
        if "version" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["version"]]
        else:
            return []
    
    # Get warnings from product label.
    def warnings(drug, user=None):
        if "warnings" in Drug.fda_drug_obj(drug):
            return Drug.fda_drug_obj(drug)["warnings"]
        else:
            return []
    
    # Get "when using" from product label.
    def when_using(drug, user=None):
        if "when_using" in Drug.fda_drug_obj(drug):
            return [Drug.fda_drug_obj(drug)["when_using"]]
        else:
            return []
        
    """
        URLs:
        
        DrugBank URL
        KEGG DRUG URL
        
    """
    
    # Return links.
    def all_urls(drug, user=None):
        url_dict = {}
        url_dict["DrugBank"] = Drug.drugbank_url(drug, user=user)
        url_dict["KEGG DRUG"] = Drug.kegg_drug_url(drug, user=user)
        return url_dict
    
    # Returns DrugBank URL.
    def drugbank_url(drug, user=None):
        url_array = []
        for drugbank_id in Drug.drugbank_id(drug, user=user):
            url_array.append("https://www.drugbank.ca/drugs/" + str(drugbank_id))
        return url_array
    
    # Returns KEGG DRUG URL.
    def kegg_drug_url(drug, user=None):
        url_array = []
        for kegg_drug_id in Drug.kegg_drug_id(drug, user=user):
            url_array.append("http://www.genome.jp/dbget-bin/www_bget?dr:" + str(kegg_drug_url))
        return url_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Returns compounds by search.
    def search(query, search_type="exact", source="rxnorm", user=None):
        return search(query, search_type=search_type, source=source)
    
    """
        External files:
        
        Images
    """
    
    # Return images.
    #   TODO: Maybe move to a different file?
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
    def images(drug, resource="rxnav", reply_format="json", color=None, resolution="full"):
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
    
    # Get all identifiers.
    print("Getting drug identifiers from RxCUI (%s)..." % rxcui)
    start = timeit.timeit()
    results_array = Drug.all_identifiers(rx_drug)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for iden in results_array:
        print("\t- %s: %s (%s)" % (iden["identifier_type"], iden["identifier"], iden["source"]))
    
    # Get all properties.
    print("\nGetting drug properties from RxCUI (%s)..." % rxcui)
    start = timeit.timeit()
    results_dict = Drug.all_properties(rx_drug)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for prop_type, prop in results_dict.items():
        print("\t- %s: %s" % (prop_type, str(prop).encode('ascii', 'ignore').decode()))

#   MAIN
if __name__ == "__main__": main()