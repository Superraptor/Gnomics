#!/usr/bin/env python

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
#   Get NCT ID.
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
import json
import requests
import timeit
import xml.etree.ElementTree as ET

#   MAIN
def main():
    nct_unit_tests("NCT03270111")
    
#   Get NCT object.
def get_nct_obj(clinical_trial):
    
    ct_obj_array = []
    for ct_obj in clinical_trial.clinical_trial_objects:
        if 'object_type' in ct_obj:
            if ct_obj['object_type'].lower() == 'clinicaltrials.gov object' or ct_obj['object_type'].lower() == 'nct object':
                ct_obj_array.append(ct_obj['object'])
    
    if ct_obj_array:
        return ct_obj_array
    
    for nct_id in get_nct_id(clinical_trial):
        
        # Download XML
        base = "https://clinicaltrials.gov/"
        ext = "ct2/show/" + nct_id + "/?displayxml=TRUE"

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        
        tree = ET.ElementTree(ET.fromstring(r.text))
        
        # Parse XML into dictionary
        xml_result_obj = {}
        
        root = tree.getroot()
        
        for child in root:
            
            # Study first posted
            if child.tag == "study_first_posted":
                if "study_first_posted" in xml_result_obj:
                    xml_result_obj["study_first_posted"].append(child.text)
                else:
                    xml_result_obj["study_first_posted"] = [child.text]
                    
            # Study first mitted
            elif child.tag == "study_first_mitted":
                if "study_first_mitted" in xml_result_obj:
                    xml_result_obj["study_first_mitted"].append(child.text)
                else:
                    xml_result_obj["study_first_mitted"] = [child.text]
                    
            # Study first mitted QC
            elif child.tag == "study_first_mitted_qc":
                if "study_first_mitted_qc" in xml_result_obj:
                    xml_result_obj["study_first_mitted_qc"].append(child.text)
                else:
                    xml_result_obj["study_first_mitted_qc"] = [child.text]
                    
            # Last update mitted.
            elif child.tag == "last_update_mitted":
                if "last_update_mitted" in xml_result_obj:
                    xml_result_obj["last_update_mitted"].append(child.text)
                else:
                    xml_result_obj["last_update_mitted"] = [child.text]
                    
            # Last updated mitted QC.
            elif child.tag == "last_update_mitted_qc":
                if "last_update_mitted_qc" in xml_result_obj:
                    xml_result_obj["last_update_mitted_qc"].append(child.text)
                else:
                    xml_result_obj["last_update_mitted_qc"] = [child.text]
                    
            # Last update posted.
            elif child.tag == "last_update_posted":
                if "last_update_posted" in xml_result_obj:
                    xml_result_obj["last_update_posted"].append(child.text)
                else:
                    xml_result_obj["last_update_posted"] = [child.text]
                    
            # First received date.
            elif child.tag == "firstreceived_date":
                if "firstreceived_date" in xml_result_obj:
                    xml_result_obj["firstreceived_date"].append(child.text)
                else:
                    xml_result_obj["firstreceived_date"] = [child.text]
                    
            # Last changed date.
            elif child.tag == "lastchanged_date":
                if "lastchanged_date" in xml_result_obj:
                    xml_result_obj["lastchanged_date"].append(child.text)
                else:
                    xml_result_obj["lastchanged_date"] = [child.text]
             
            # Verification date.
            elif child.tag == "verification_date":
                if "verification_date" in xml_result_obj:
                    xml_result_obj["verification_date"].append(child.text)
                else:
                    xml_result_obj["verification_date"] = [child.text]
                    
            # Brief title.
            elif child.tag == "brief_title":
                if "brief_title" in xml_result_obj:
                    xml_result_obj["brief_title"].append(child.text)
                else:
                    xml_result_obj["brief_title"] = [child.text]
            
            # Official title.
            elif child.tag == "official_title":
                if "official_title" in xml_result_obj:
                    xml_result_obj["official_title"].append(child.text)
                else:
                    xml_result_obj["official_title"] = [child.text]
                    
            # Overall status.
            elif child.tag == "overall_status":
                if "overall_status" in xml_result_obj:
                    xml_result_obj["overall_status"].append(child.text)
                else:
                    xml_result_obj["overall_status"] = [child.text]
                    
            # Start date.
            elif child.tag == "start_date":
                if "start_date" in xml_result_obj:
                    xml_result_obj["start_date"].append(child.text)
                else:
                    xml_result_obj["start_date"] = [child.text]
                    
            # Completion date.
            elif child.tag == "completion_date":
                if "completion_date" in xml_result_obj:
                    xml_result_obj["completion_date"].append(child.text)
                else:
                    xml_result_obj["completion_date"] = [child.text]
                    
            # Primary completion date.
            elif child.tag == "primary_completion_date":
                if "primary_completion_date" in xml_result_obj:
                    xml_result_obj["primary_completion_date"].append(child.text)
                else:
                    xml_result_obj["primary_completion_date"] = [child.text]
            
            # Phase.
            elif child.tag == "phase":
                if "phase" in xml_result_obj:
                    xml_result_obj["phase"].append(child.text)
                else:
                    xml_result_obj["phase"] = [child.text]
            
            # Study type.
            elif child.tag == "study_type":
                if "study_type" in xml_result_obj:
                    xml_result_obj["study_type"].append(child.text)
                else:
                    xml_result_obj["study_type"] = [child.text]
           
            # Keywords.
            elif child.tag == "keyword":
                if "keyword" in xml_result_obj:
                    xml_result_obj["keyword"].append(child.text)
                else:
                    xml_result_obj["keyword"] = [child.text]
            
            for subchild in child:
                if subchild.tag == "mesh_term":
                    if "mesh_term" in xml_result_obj:
                        xml_result_obj["mesh_term"].append(subchild.text)
                    else:
                        xml_result_obj["mesh_term"] = [subchild.text]
                        
                elif subchild.tag == "investigator_full_name":
                    if "investigator_full_name" in xml_result_obj:
                        xml_result_obj["investigator_full_name"].append(subchild.text)
                        
                    else:
                        xml_result_obj["investigator_full_name"] = [subchild.text]
                        
                elif subchild.tag == "country":
                    if "country" in xml_result_obj:
                        xml_result_obj["country"].append(subchild.text)
                        
                    else:
                        xml_result_obj["country"] = [subchild.text]
                        
                elif subchild.tag == "status":
                    if "status" in xml_result_obj:
                        xml_result_obj["status"].append(subchild.text)
                        
                    else:
                        xml_result_obj["status"] = [subchild.text]
                        
                elif subchild.tag == "url":
                    if "url" in xml_result_obj:
                        xml_result_obj["url"].append(subchild.text)
                        
                    else:
                        xml_result_obj["url"] = [subchild.text]
                        
                elif subchild.tag == "org_study_id":
                    if "org_study_id" in xml_result_obj:
                        xml_result_obj["org_study_id"].append(subchild.text)
                        
                    else:
                        xml_result_obj["org_study_id"] = [subchild.text]
                        
                elif subchild.tag == "nct_id":
                    if "nct_id" in xml_result_obj:
                        xml_result_obj["nct_id"].append(subchild.text)
                        
                    else:
                        xml_result_obj["nct_id"] = [subchild.text]
                        
                elif subchild.tag == "textblock" and child.tag == "brief_summary":
                    if "brief_summary" in xml_result_obj:
                        xml_result_obj["brief_summary"].append(subchild.text.strip().replace("\n","").replace("      ", " "))
                        
                    else:
                        
                        xml_result_obj["brief_summary"] = [subchild.text.strip().replace("\n","").replace("      ", " ")]
                        
                elif subchild.tag == "textblock" and child.tag == "detailed_description":
                    if "detailed_description" in xml_result_obj:
                        xml_result_obj["detailed_description"].append(subchild.text.strip().replace("\n","").replace("      ", " "))
                        
                    else:
                        xml_result_obj["detailed_description"] = [subchild.text.strip().replace("\n","").replace("      ", " ")]
                        
                elif subchild.tag == "gender":
                    if "gender" in xml_result_obj:
                        xml_result_obj["gender"].append(subchild.text)
                        
                    else:
                        xml_result_obj["gender"] = [subchild.text]
                        
                elif subchild.tag == "gender_based":
                    if "gender_based" in xml_result_obj:
                        xml_result_obj["gender_based"].append(subchild.text)
                        
                    else:
                        xml_result_obj["gender_based"] = [subchild.text]
                        
                elif subchild.tag == "minimum_age":
                    if "minimum_age" in xml_result_obj:
                        xml_result_obj["minimum_age"].append(subchild.text)
                        
                    else:
                        xml_result_obj["minimum_age"] = [subchild.text]
                        
                elif subchild.tag == "maximum_age":
                    if "maximum_age" in xml_result_obj:
                        xml_result_obj["maximum_age"].append(subchild.text)
                        
                    else:
                        xml_result_obj["maximum_age"] = [subchild.text]
         
        gnomics.objects.clinical_trial.ClinicalTrial.add_object(clinical_trial, obj = xml_result_obj, object_type = "ClinicalTrials.gov Object")
        
        ct_obj_array.append(xml_result_obj)
        
    return ct_obj_array

#   Get NCT ID.
def get_nct_id(clinical_trial):
    nct_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(clinical_trial.identifiers, ["nct", "nct id", "nct identifier"]):
        if iden["identifier"] not in nct_array:
            nct_array.append(iden["identifier"])
    return nct_array

#   UNIT TESTS
def nct_unit_tests(nct_id):
    nct_ct = gnomics.objects.clinical_trial.ClinicalTrial(identifier = nct_id, identifier_type = "NCT ID", language = None, source = "ClinicalTrials.gov")
    get_nct_obj(nct_ct)

#   MAIN
if __name__ == "__main__": main()