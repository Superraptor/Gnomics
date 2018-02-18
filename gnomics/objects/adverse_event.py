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
#
#

#
#   Create instance of an adverse event.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Import sub-methods.
from gnomics.objects.adverse_event_files.aero import get_aero_id
from gnomics.objects.adverse_event_files.meddra import get_meddra_id, get_meddra_term, get_meddra_obj
from gnomics.objects.adverse_event_files.mesh import get_mesh_uid
from gnomics.objects.adverse_event_files.oae import get_oae_id
from gnomics.objects.adverse_event_files.ocvdae import get_ocvdae_id
from gnomics.objects.adverse_event_files.odnae import get_odnae_id
from gnomics.objects.adverse_event_files.ovae import get_ovae_id
from gnomics.objects.adverse_event_files.search import search

#   Other imports.
import timeit

#   Import further methods.
from gnomics.objects.interaction_objects.adverse_event_drug import get_drugs
from gnomics.objects.interaction_objects.adverse_event_phenotype import get_phenotypes

#   MAIN
def main():
    adverse_event_unit_tests("10011224")

#   ADVERSE EVENT CLASS
class AdverseEvent:
    """
        Adverse event class:
        
        According to the U.S. Food & Drug Administration
        (FDA) an adverse event (AE) is "any undesirable
        experience associated with the use of a medical
        product in a patient."
    """
    
    # AERO BioPortal PURL.
    aero_bioportal_purl = "http://purl.bioontology.org/ontology/AERO"
    
    # COSTART BioPortal PURL.
    costart_bioportal_purl = "http://purl.bioontology.org/ontology/COSTART"
    
    # CTCAE BioPortal PURL.
    ctcae_bioportal_purl = "http://purl.bioontology.org/ontology/CTCAE"
    
    # MEDDRA BioPortal PURL.
    meddra_bioportal_purl = "http://purl.bioontology.org/ontology/MEDDRA"
    
    # MeSH BioPortal PURL.
    mesh_bioportal_purl = "http://purl.bioontology.org/ontology/MESH"
    
    # OAE BioPortal PURL.
    oae_bioportal_purl = "http://purl.bioontology.org/ontology/OAE"
    
    # OCVDAE BioPortal PURL.
    ocvdae_bioportal_purl = "http://purl.bioontology.org/ontology/OCVDAE"
    
    # ODNAE BioPortal PURL.
    odnae_bioportal_purl = "http://purl.bioontology.org/ontology/ODNAE"
    
    # OVAE BioPortal PURL.
    ovae_bioportal_purl = "http://purl.bioontology.org/ontology/OVAE"
    
    # SSE BioPortal PURL.
    sse_bioportal_purl = "http://purl.bioontology.org/ontology/SSE"
    
    # WHO-ART BioPortal PURL.
    whoart_bioportal_purl = "http://purl.bioontology.org/ontology/WHO-ART"
    
    """
        Adverse event attributes:
        
        Identifier      = A particular way to identify the
                          adverse event in question. Usually a database unique identifier, but could also be natural language.
        Identifier Type = Typically, the database or origin 
                          or type of identifier being 
                          provided.
        Language        = The natural language of the 
                          identifier, if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the adverse event.
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

        # Initialize dictionary of adverse event objects.
        self.adverse_event_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to an adverse event.
    def add_identifier(adverse_event, identifier=None, identifier_type=None, language=None, source=None, name=None):
        adverse_event.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to an adverse event.
    def add_object(adverse_event, obj=None, object_type=None):
        adverse_event.adverse_event_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Adverse event objects:
        
        MedDRA Object
        
    """
    
    # Get MedDRA object.
    def meddra_obj(adverse_event, user=None, source="umls"):
        return get_meddra_obj(adverse_event, user=user, source="umls")
        
    """
        Adverse event identifiers:
        
        AERO ID
        MedDRA ID
        MedDRA Term
        MeSH UID
        OAE ID
        OCVDAE ID
        ODNAE ID
        OVAE ID
        
    """
    
    # Return all identifiers.
    def all_identifiers(adverse_event, user = None):
        AdverseEvent.aero_id(adverse_event, user=user)
        AdverseEvent.meddra_id(adverse_event, user=user)
        AdverseEvent.meddra_term(adverse_event, user=user)
        AdverseEvent.mesh_uid(adverse_event, user=user)
        AdverseEvent.oae_id(adverse_event, user=user)
        AdverseEvent.ocvdae_id(adverse_event, user=user)
        AdverseEvent.odnae_id(adverse_event, user=user)
        AdverseEvent.ovae_id(adverse_event, user=user)
        return adverse_event.identifiers
    
    # Return AERO ID.
    def aero_id(adverse_event, user=None):
        return get_aero_id(adverse_event, user=user)
    
    # Return MedDRA ID.
    def meddra_id(adverse_event, user=None):
        return get_meddra_id(adverse_event, user=user)
        
    # Return MedDRA Term.
    def meddra_term(adverse_event, user=None):
        return get_meddra_term(adverse_event, user=user)
        
    # Return MeSH UID.
    def mesh_uid(adverse_event, user=None):
        return get_mesh_uid(adverse_event, user=user)
    
    # Return OAE ID.
    def oae_id(adverse_event, user=None):
        return get_oae_id(adverse_event, user=user)
    
    # Return OCVDAE ID.
    def ocvdae_id(adverse_event, user=None):
        return get_ocvdae_id(adverse_event, user=user)

    # Return ODNAE ID.
    def odnae_id(adverse_event, user=None):
        return get_odnae_id(adverse_event, user=user)
    
    # Return OVAE ID.
    def ovae_id(adverse_event, user=None):
        return get_ovae_id(adverse_event, user=user)
    
    """
        Interaction objects:
        
        Drugs
        Phenotypes
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(adverse_event, user=None):
        interaction_obj = {}
        interaction_obj["Drugs"] = AdverseEvent.drugs(adverse_event, user=user)
        interaction_obj["Phenotypes"] = AdverseEvent.phenotypes(adverse_event, user=user)
        return interaction_obj
    
    # Return phenotypes related to an AE.
    def phenotypes(adverse_event, user=None):
        return get_phenotypes(adverse_event, user=user)

    # Return drugs related to an AE.
    def drugs(adverse_event, user=None):
        return get_drugs(adverse_event, user=user)
    
    """
        Other properties:
        
    """
    
    # Return all properties associated with an AE.
    def all_properties(adverse_event, user=None):
        property_dict = {}
        return property_dict
    
    """
        URLs:
        
        AERO BioPortal URL
        MedDRA BioPortal URL
        MeSH BioPortal URL
        OAE BioPortal URL
        OCVDAE BioPortal URL
        ODNAE BioPortal URL
        OVAE BioPortal URL
    """
    
    # Return all URLs associated with AE.
    def all_urls(adverse_event, user=None):
        url_dict = {}
        url_dict["AERO BioPortal"] = AdverseEvent.aero_bioportal_url(adverse_event, user=user)
        url_dict["MedDRA BioPortal"] = AdverseEvent.meddra_bioportal_url(adverse_event, user=user)
        url_dict["MeSH BioPortal"] = AdverseEvent.mesh_bioportal_url(adverse_event, user=user)
        url_dict["OAE BioPortal"] = AdverseEvent.oae_bioportal_url(adverse_event, user=user)
        url_dict["OCVDAE BioPortal"] = AdverseEvent.ocvdae_bioportal_url(adverse_event, user=user)
        url_dict["ODNAE BioPortal"] = AdverseEvent.odnae_bioportal_url(adverse_event, user=user)
        url_dict["OVAE BioPortal"] = AdverseEvent.ovae_bioportal_url(adverse_event, user=user)
        return url_dict
    
    # Return AERO BioPortal URL.
    def aero_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.aero_id(adverse_event, user=user):
            url_array.append(AdverseEvent.aero_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MedDRA BioPortal URL.
    def meddra_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.meddra_id(adverse_event, user=user):
            url_array.append(AdverseEvent.meddra_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return MeSH BioPortal URL.
    def mesh_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.mesh_uid(adverse_event, user=user):
            url_array.append(AdverseEvent.mesh_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return OAE BioPortal URL.
    def oae_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.oae_id(adverse_event, user=user):
            url_array.append(AdverseEvent.oae_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return OCVDAE BioPortal URL.
    def ocvdae_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.ocvdae_id(adverse_event, user=user):
            url_array.append(AdverseEvent.ocvdae_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return ODNAE BioPortal URL.
    def odnae_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.odnae_id(adverse_event, user=user):
            url_array.append(AdverseEvent.odnae_bioportal_purl + "/" + str(iden))
        return url_array
    
    # Return OVAE BioPortal URL.
    def ovae_bioportal_url(adverse_event, user=None):
        url_array = []
        for iden in AdverseEvent.ovae_id(adverse_event, user=user):
            url_array.append(AdverseEvent.ovae_bioportal_purl + "/" + str(iden))
        return url_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Search for AEs.
    def search(query, user=None):
        return search(query, user=user)

#   UNIT TESTS
def adverse_event_unit_tests(meddra_id):
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()