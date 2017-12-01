#
#
#
#
#

#
#   IMPORT SOURCES:
#       CLINICAL_TRIALS
#           https://pypi.python.org/pypi/clinical_trials/1.1
#

#
#   Create instance of a clinical trial.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS
import clinical_trials

#   Import sub-methods.
from gnomics.objects.clinical_trial_files.nct import get_nct_id, get_nct_obj
from gnomics.objects.clinical_trial_files.search import search

#   MAIN
def main():
    clinical_trial_unit_tests("NCT03270111")

#   CLINICAL TRIAL CLASS
class ClinicalTrial:
    """
        Clinical trial class:
        
        According to the World Health Organization
        (WHO), a clinical trial is "any research study
        that prospectively assigns human participants
        or groups of humans to one or more
        health-related interventions to evaluate
        the effects on health outcomes."
    """
    
    """
        Clinical trial attributes:
        
        Identifier      = A particular way to identify the
                          clinical trial in question. 
                          Usually a database unique identifier, 
                          but could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
        
    # Initialize the clinical trial.
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
        
        # Initialize dictionary of clinical trial objects.
        self.clinical_trial_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a clinical trial.
    def add_identifier(clinical_trial, identifier = None, identifier_type = None, language = None, source = None, name = None):
        clinical_trial.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a clinical trial.
    def add_object(clinical_trial, obj = None, object_type = None):
        clinical_trial.clinical_trial_objects.append({
            'object': obj,
            'object_type': object_type
        })

    """
        Clinical trial objects:
        
        ClinicalTrials.gov Object
    """
    
    # Return ClinicalTrials.gov Object.
    def clinicaltrials_gov_obj(clinical_trial):
        return get_nct_obj(clinical_trial) 
        
    """
        Clinical trial identifiers:
        
        NCI ID
        NCT ID
    """
    
    # Return all identifiers.
    def all_identifiers(clinical_trial, user = None):
        ClinicalTrial.nci_id(clinical_trial)
        ClinicalTrial.nct_id(clinical_trial)
        return clinical_trial.identifiers
    
    # Return NCI ID.
    def nci_id(clinical_trial):
        print("NOT FUNCTIONAL.")
    
    # Return NCT ID.
    def nct_id(clinical_trial):
        return get_nct_id(clinical_trial)
    
    """
        Interaction objects:
        
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(clinical_trial, user = None):
        interaction_obj = {}
        return interaction_obj
    
    """
        Other properties:
        
        Brief summary
        Brief title
        Condition summary
        Detailed description
        Intervention summary
        Last changed
        Last update posted
        Last update submitted
        Lead sponsor
        Official title
        Order
        Procedure
        Score
        Sponsors
        Status
        Title
    """
    
    def all_properties(clinical_trial, user = None):
        property_dict = {}
        property_dict["Brief Summary"] = ClinicalTrial.brief_summary(clinical_trial)
        property_dict["Brief Title"] = ClinicalTrial.brief_title(clinical_trial)
        property_dict["Completion Date"] = ClinicalTrial.completion_date(clinical_trial)
        property_dict["Country"] = ClinicalTrial.country(clinical_trial)
        property_dict["Detailed Description"] = ClinicalTrial.detailed_description(clinical_trial)
        property_dict["First Received Date"] = ClinicalTrial.first_received_date(clinical_trial)
        property_dict["Official Title"] = ClinicalTrial.official_title(clinical_trial)
        property_dict["Overall Status"] = ClinicalTrial.overall_status(clinical_trial)
        property_dict["Phase"] = ClinicalTrial.phase(clinical_trial)
        property_dict["Primary Completion Date"] = ClinicalTrial.primary_completion_date(clinical_trial)
        property_dict["Start Date"] = ClinicalTrial.start_date(clinical_trial)
        property_dict["Study Type"] = ClinicalTrial.study_type(clinical_trial)
        property_dict["Status"] = ClinicalTrial.status(clinical_trial)
        return property_dict
    
    # Get brief summary.
    def brief_summary(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["brief_summary"])
        return prop_array
        
    # Get brief title.
    def brief_title(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["brief_title"])
        return prop_array
    
    # Get trial completion date.
    def completion_date(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["completion_date"])
        return prop_array
    
    # Get condition summary.
    def condition_summary():
        print("NOT FUNCTIONAL.")
    
    # Get country in which trial takes place.
    def country(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["country"])
        return prop_array
    
    # Get detailed description.
    def detailed_description(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["detailed_description"])
        return prop_array
    
    # Get date first received.
    def first_received_date(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["firstreceived_date"])
        return prop_array
    
    # Get intervention summary.
    def intervention_summary():
        print("NOT FUNCTIONAL.")
        
    # Get date entry was last changed.
    def last_changed():
        print("NOT FUNCTIONAL.")
        
    # Get date last update was posted for entry.
    def last_update_posted():
        print("NOT FUNCTIONAL.")
        
    # Get date last update was submitted for entry.
    def last_update_submitted():
        print("NOT FUNCTIONAL.")
    
    # Get lead sponsor.
    def lead_sponsor():
        print("NOT FUNCTIONAL.")
    
    # Get official title.
    def official_title(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["official_title"])
        return prop_array
    
    # Get order.
    def order():
        print("NOT FUNCTIONAL.")
    
    # Get overall status.
    def overall_status(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["overall_status"])
        return prop_array
    
    # Get trial phase.
    def phase(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["phase"])
        return prop_array
    
    # Get primary completion date.
    def primary_completion_date(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["primary_completion_date"])
        return prop_array
        
    # Get procedure.
    def procedure():
        print("NOT FUNCTIONAL.")
    
    # Get clinical trial score.
    def score():
        print("NOT FUNCTIONAL.")
        
    # Get sponsors.
    def sponsors():
        print("NOT FUNCTIONAL.")
        
    # Get trial start date.
    def start_date(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["start_date"])
        return prop_array
    
    # Get study type.
    def study_type(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["study_type"])
        return prop_array
        
    # Get clinical trial status.
    def status(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["status"])
        return prop_array
        
    # Get clinical trial title.
    def title():
        print("NOT FUNCTIONAL.")
    
    """
        URLs:
        
        ClinicalTrials.gov URL
    """
    
    # Get URL at ClinicalTrials.gov.
    def clinicaltrials_gov_url(clinical_trial):
        prop_array = []
        for obj in ClinicalTrial.clinicaltrials_gov_obj(clinical_trial):
            prop_array.extend(obj["url"])
        return prop_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Search for clinical trials.
    def search(query=None, condition=None, count=None, intervention=None, recruiting=None, sponsor=None, output_format=None, state=None, country=None, download=None, size=None, from_result=None, include=None, exclude=None, fulltext=None, org_name_fulltext=None, trialids=None, nci_id=None, nct_id=None, protocol_id=None, ccr_id=None, ctep_id=None, dcp_id=None, current_trial_status=None, phase=None, study_protocol_type=None, brief_title=None, brief_summary=None, official_title=None, primary_purpose_code=None, accepts_healthy_volunteers_indicator=None, acronym=None, amendment_date=None, anatomic_sites=None, arm_description=None, arm_name=None, arm_type=None, intervention_code=None, intervention_description=None, intervention_type=None, intervention_synonyms=None, study_id=None, study_id_type=None, gender=None, max_age_in_years_lte=None, max_age_in_years_gte=None, min_age_in_years_lte=None, min_age_in_years_gte=None, min_age_unit=None, max_age_unit=None, max_age_number_lte=None, max_age_number_gte=None, min_age_number_lte=None, min_age_number_gte=None, current_trial_status_date_lte=None, current_trial_status_date_gte=None, record_verification_date_lte=None, record_vertification_date_gte=None, org_coordinates_lat=None, org_coordinates_lon=None, contact_email=None, contact_name=None, contact_phone=None, generic_contact=None, org_address_line_1=None, org_address_line_2=None, org_city=None, org_postal_code=None, org_state_or_province=None, org_country=None, org_email=None, org_family=None, org_fax=None, org_name=None, org_phone=None, org_status=None, org_status_date=None, org_to_family_relationship=None, org_tty=None, recruitment_status=None, recruitment_status_date=None, source="ClinicalTrials.gov", user=None):
        return search(query=query, condition=condition, count=count, intervention=intervention, recruiting=recruiting, sponsor=sponsor, output_format=output_format, state=state, country=country, download=download, size=size, from_result=from_result, include=include, exclude=exclude, fulltext=fulltext, org_name_fulltext=org_name_fulltext, trialids=trialids, nci_id=nci_id, nct_id=nct_id, protocol_id=protocol_id, ccr_id=ccr_id, ctep_id=ctep_id, dcp_id=dcp_id, current_trial_status=current_trial_status, phase=phase, study_protocol_type=study_protocol_type, brief_title=brief_title, brief_summary=brief_summary, official_title=official_title, primary_purpose_code=primary_purpose_code, accepts_healthy_volunteers_indicator=accepts_healthy_volunteers_indicator, acronym=acronym, amendment_date=amendment_date, anatomic_sites=anatomic_sites, arm_description=arm_description, arm_name=arm_name, arm_type=arm_type, intervention_code=intervention_code, intervention_description=intervention_description, intervention_type=intervention_type, intervention_synonyms=intervention_synonyms, study_id=study_id, study_id_type=study_id_type, gender=gender, max_age_in_years_lte=max_age_in_years_lte, max_age_in_years_gte=max_age_in_years_gte, min_age_in_years_lte=min_age_in_years_lte, min_age_in_years_gte=min_age_in_years_gte, min_age_unit=min_age_unit, max_age_unit=max_age_unit, max_age_number_lte=max_age_number_lte, max_age_number_gte=max_age_number_gte, min_age_number_lte=min_age_number_lte, min_age_number_gte=min_age_number_gte, current_trial_status_date_lte=current_trial_status_date_lte, current_trial_status_date_gte=current_trial_status_date_gte, record_verification_date_lte=record_verification_date_lte, record_vertification_date_gte=record_vertification_date_gte, org_coordinates_lat=org_coordinates_lat, org_coordinates_lon=org_coordinates_lon, contact_email=contact_email, contact_name=contact_name, contact_phone=contact_phone, generic_contact=generic_contact, org_address_line_1=org_address_line_1, org_address_line_2=org_address_line_2, org_city=org_city, org_postal_code=org_postal_code, org_state_or_province=org_state_or_province, org_country=org_country, org_email=org_email, org_family=org_family, org_fax=org_fax, org_name=org_name, org_phone=org_phone, org_status=org_status, org_status_date=org_status_date, org_to_family_relationship=org_to_family_relationship, org_tty=org_tty, recruitment_status=recruitment_status, recruitment_status_date=recruitment_status_date, source=source)

#   UNIT TESTS
def clinical_trial_unit_tests(nct_id):
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()