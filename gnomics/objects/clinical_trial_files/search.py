#!/usr/bin/env python

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
#   Search for clinical trials.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

#   Import modules.
from gnomics.objects.user import User
import gnomics.objects.clinical_trial

#   Other imports.
from bioservices import *
import clinical_trials
import json
import requests
import timeit

#   MAIN
def main():
    search_unit_tests("cancer")

#   Get search.
#
#   Parameters:
#   - Condition (disease)
#   - Count
#   - Intervention
#   - Recruiting
#   - Sponsor
#   - Output Format
#   - State
#   - Country
#   - Download
def search(query=None, condition=None, count=None, intervention=None, recruiting=None, sponsor=None, output_format=None, state=None, country=None, download=None, size=None, from_result=None, include=None, exclude=None, fulltext=None, org_name_fulltext=None, trialids=None, nci_id=None, nct_id=None, protocol_id=None, ccr_id=None, ctep_id=None, dcp_id=None, current_trial_status=None, phase=None, study_protocol_type=None, brief_title=None, brief_summary=None, official_title=None, primary_purpose_code=None, accepts_healthy_volunteers_indicator=None, acronym=None, amendment_date=None, anatomic_sites=None, arm_description=None, arm_name=None, arm_type=None, intervention_code=None, intervention_description=None, intervention_type=None, intervention_synonyms=None, study_id=None, study_id_type=None, gender=None, max_age_in_years_lte=None, max_age_in_years_gte=None, min_age_in_years_lte=None, min_age_in_years_gte=None, min_age_unit=None, max_age_unit=None, max_age_number_lte=None, max_age_number_gte=None, min_age_number_lte=None, min_age_number_gte=None, current_trial_status_date_lte=None, current_trial_status_date_gte=None, record_verification_date_lte=None, record_vertification_date_gte=None, org_coordinates_lat=None, org_coordinates_lon=None, contact_email=None, contact_name=None, contact_phone=None, generic_contact=None, org_address_line_1=None, org_address_line_2=None, org_city=None, org_postal_code=None, org_state_or_province=None, org_country=None, org_email=None, org_family=None, org_fax=None, org_name=None, org_phone=None, org_status=None, org_status_date=None, org_to_family_relationship=None, org_tty=None, recruitment_status=None, recruitment_status_date=None, source="ClinicalTrials.gov"):
    search_results = []
    
    if source == "ClinicalTrials.gov":
        t = clinical_trials.Trials()
        if query:
            if condition:
                return t.search(query, condition=condition)
            elif intervention:
                return t.search(query, intervention=intervention)
            elif count:
                return t.search(query, count=count)
            elif size:
                return t.search(query, count=size)
            elif recruiting:
                return t.search(query, recruiting=recruiting)
            elif sponsor:
                return t.search(query, sponsor=sponsor)
            elif output_format:
                if output_format.lower() == "xml":
                    return t.search(query, output_format=None)
                else:
                    return t.search(query, output_format=output_format)
            elif state:
                if type(state) is list:
                    if len(state) == 1:
                        return t.search(query, state=state[0])
                    elif len(state) == 2:
                        return t.search(query, state1=state[0], state2=state[1])
                    elif len(state) == 3:
                        return t.search(query, state1=state[0], state2=state[1], state3=state[2])
                    else:
                        print("Currently, this function can only support up to 3 states.")
                else:
                    return t.search(query, state=state)
                
                return t.search(query, state=state)
            elif country:
                if type(country) is list:
                    if len(country) == 1:
                        return t.search(query, country=country[0])
                    elif len(country) == 2:
                        return t.search(query, country1=country[0], country2=country[1])
                    elif len(country) == 3:
                        return t.search(query, country1=country[0], country2=country[1], country3=country[2])
                    else:
                        print("Currently, this function can only support up to 3 countries.")
                else:
                    return t.search(query, country=country)
            else:
                res = t.search(query)
                if "clinical_study" in res["search_results"]:
                    for study in res["search_results"]["clinical_study"]:
                        temp_study = gnomics.objects.clinical_trial.ClinicalTrial(identifier=study["nct_id"], identifier_type="NCT ID", language=None, source="ClinicalTrials.gov", name=study["title"])
                        gnomics.objects.clinical_trial.ClinicalTrial.add_object(temp_study, obj=study, object_type="ClinicalTrials.gov")

                        search_results.append(temp_study)
                
                return search_results
                    
        elif condition:
            return t.search(condition=condition)
        elif intervention:
            return t.search(intervention=intervention)
        else:
            print("No correct parameters were provided. Ending search.")
            return []
    
    elif source == "NCI Clinical Trials":
        print("NOT FUNCTIONAL.")
    
    else:
        print("The source provided does not have a search option.")
        print("Searching using ClinicalTrials.gov instead...")
        return search(query=query, condition=condition, count=count, intervention=intervention, recruiting=recruiting, sponsor=sponsor, output_format=output_format, state=state, country=country, download=download, size=size, from_result=from_result, include=include, exclude=exclude, fulltext=fulltext, org_name_fulltext=org_name_fulltext, trialids=trialids, nci_id=nci_id, nct_id=nct_id, protocol_id=protocol_id, ccr_id=ccr_id, ctep_id=ctep_id, dcp_id=dcp_id, current_trial_status=current_trial_status, phase=phase, study_protocol_type=study_protocol_type, brief_title=brief_title, brief_summary=brief_summary, official_title=official_title, primary_purpose_code=primary_purpose_code, accepts_healthy_volunteers_indicator=accepts_healthy_volunteers_indicator, acronym=acronym, amendment_date=amendment_date, anatomic_sites=anatomic_sites, arm_description=arm_description, arm_name=arm_name, arm_type=arm_type, intervention_code=intervention_code, intervention_description=intervention_description, intervention_type=intervention_type, intervention_synonyms=intervention_synonyms, study_id=study_id, study_id_type=study_id_type, gender=gender, max_age_in_years_lte=max_age_in_years_lte, max_age_in_years_gte=max_age_in_years_gte, min_age_in_years_lte=min_age_in_years_lte, min_age_in_years_gte=min_age_in_years_gte, min_age_unit=min_age_unit, max_age_unit=max_age_unit, max_age_number_lte=max_age_number_lte, max_age_number_gte=max_age_number_gte, min_age_number_lte=min_age_number_lte, min_age_number_gte=min_age_number_gte, current_trial_status_date_lte=current_trial_status_date_lte, current_trial_status_date_gte=current_trial_status_date_gte, record_verification_date_lte=record_verification_date_lte, record_vertification_date_gte=record_vertification_date_gte, org_coordinates_lat=org_coordinates_lat, org_coordinates_lon=org_coordinates_lon, contact_email=contact_email, contact_name=contact_name, contact_phone=contact_phone, generic_contact=generic_contact, org_address_line_1=org_address_line_1, org_address_line_2=org_address_line_2, org_city=org_city, org_postal_code=org_postal_code, org_state_or_province=org_state_or_province, org_country=org_country, org_email=org_email, org_family=org_family, org_fax=org_fax, org_name=org_name, org_phone=org_phone, org_status=org_status, org_status_date=org_status_date, org_to_family_relationship=org_to_family_relationship, org_tty=org_tty, recruitment_status=recruitment_status, recruitment_status_date=recruitment_status_date, source="ClinicalTrials.gov")
            
#   UNIT TESTS
def search_unit_tests(query):
    start = timeit.timeit()
    query_result = search(query=query)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for res in query_result:
        for ident in res.identifiers:
            if ident["identifier_type"] == "NCT ID":
                print("- %s: %s (%s)" % (str(ident["identifier"]), ident["name"], ident["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()