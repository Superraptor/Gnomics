#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get adverse events from a drug.
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
import gnomics.objects.adverse_event
import gnomics.objects.drug

#   Other imports.
import json
import requests

#   MAIN
def main():
    drug_adverse_event_unit_tests("88014", "")

# Get drug adverse events.
def get_adverse_events(drug, user = None, counts = False, exact = True, limit = 100, all_results = True, details = False):
    ae_array = []
    ae_obj_array = []
    ae_count_dict = {}
    rx_array = []
    bad_result = False
    for ident in drug.identifiers:
        if (ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm id" or ident["identifier_type"].lower() == "rxnorm concept unique identifier") and user is not None:
            bad_result = False
            base = "https://api.fda.gov/drug/event.json?"
            ext = "api_key=" + user.fda_api_key + "&limit=" + str(limit) + "&skip=0&search=rxcui:" + ident["identifier"]
            if details == False:
                ext += "&count=patient.reaction.reactionmeddrapt.exact"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                bad_result = True
            else:
                decoded = json.loads(r.text)
                for result in decoded["results"]:
                    if details:
                        for rxn in result["patient"]["reaction"]:
                            meddra_term = rxn["reactionmeddrapt"]
                            meddra_version =  rxn["reactionmeddraversionpt"]
                            if meddra_term not in ae_array:
                                temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                ae_array.append(meddra_term)
                                ae_obj_array.append(temp_ae)
                                ae_count_dict[meddra_term] = 1
                            else:
                                ae_count_dict[meddra_term] += 1
                    else:
                        proc_term = result["term"].lower().capitalize()
                        if proc_term not in ae_array:
                            temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = proc_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                            ae_array.append(proc_term)
                            ae_obj_array.append(temp_ae)
                            ae_count_dict[proc_term] = result["count"]
                        else:
                            ae_count_dict[proc_term] += result["count"]
                if details:
                    total = decoded["meta"]["results"]["total"] - limit
                    skip = 1
                while True and all_results and details:
                    if skip % 10 == 0:
                        print("Page: %s / %s" % (str(skip), str(total)))
                    base = "https://api.fda.gov/drug/event.json?"
                    ext = "api_key=" + user.fda_api_key + "&limit=" + str(limit) + "&skip=" + str(skip) + "&search=rxcui:" + ident["identifier"]
                    if details == False:
                        ext += "&count=patient.reaction.reactionmeddrapt.exact"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    for result in decoded["results"]:
                        if details:
                            for rxn in result["patient"]["reaction"]:
                                meddra_term = rxn["reactionmeddrapt"]
                                meddra_version =  rxn["reactionmeddraversionpt"]
                                if meddra_term not in ae_array:
                                    temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                    ae_array.append(meddra_term)
                                    ae_obj_array.append(temp_ae)
                                    ae_count_dict[meddra_term] = 1
                                else:
                                    ae_count_dict[meddra_term] += 1
                        else:
                            proc_term = result["term"].lower().capitalize()
                            if proc_term not in ae_array:
                                temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = proc_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                ae_array.append(proc_term)
                                ae_obj_array.append(temp_ae)
                                ae_count_dict[proc_term] = result["count"]
                            else:
                                ae_count_dict[proc_term] += result["count"]
                    skip = skip + 1
                    total = total - limit
                    if total <= 0:
                        break
            if bad_result and exact == False:
                # This includes concepts of term types "IN", "MIN", "PIN", "BN", "SBD", "SBDC", "SBDF", "SBDG", "SCD", "SCDC", "SCDF", "SCDG", "DF", "DFG", "BPCK" and "GPCK".
                
                # BN = brand name
                # BPCK = branded pack
                # DF = dose form
                # DFG = dose form group
                # IN = ingredient
                # MIN = multiple ingredients
                # PIN = precise ingredient
                # SBD = branded drug
                # SBDC = branded drug component
                # SBDF = branded dose form
                # SBDG = branded dose form group
                # SCD = clinical drug
                # SCDC = clinical drug component
                # SCDF = clinical dose form
                # SCDG = clinical dose form group
                print("Exact RxCUI mapping provided no results...\n")
                print("Continuing with all related RxCUIs.")
                base = "https://rxnav.nlm.nih.gov/REST/"
                ext = "rxcui/" + ident["identifier"] + "/allrelated.json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                rxcui_array = []
                for x in decoded["allRelatedGroup"]["conceptGroup"]:
                    if "conceptProperties" in x:
                        for obj in x["conceptProperties"]:
                            if obj["rxcui"] not in rxcui_array:
                                rxcui_array.append(obj["rxcui"])
                no_not_found = 0
                for rxcui in rxcui_array:
                    if rxcui not in rx_array:
                        base = "https://api.fda.gov/drug/event.json?"
                        ext = "api_key=" + user.fda_api_key + "&limit=" + str(limit) + "&skip=0&search=rxcui:" + str(rxcui)
                        if details == False:
                            ext += "&count=patient.reaction.reactionmeddrapt.exact"
                        r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                        if not r.ok:
                            no_not_found = no_not_found + 1
                        else:
                            decoded = json.loads(r.text)
                            for result in decoded["results"]:
                                if details:
                                    for rxn in result["patient"]["reaction"]:
                                        if "reactionmeddrapt" in rxn and "reactionmeddraversionpt" in rxn:
                                            meddra_term = rxn["reactionmeddrapt"]
                                            meddra_version =  rxn["reactionmeddraversionpt"]
                                            if meddra_term not in ae_array:
                                                temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                                ae_array.append(meddra_term)
                                                ae_obj_array.append(temp_ae)
                                                ae_count_dict[meddra_term] = 1
                                            else:
                                                ae_count_dict[meddra_term] += 1
                                else:
                                    proc_term = result["term"].lower().capitalize()
                                    if proc_term not in ae_array:
                                        temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = proc_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                        ae_array.append(proc_term)
                                        ae_obj_array.append(temp_ae)
                                        ae_count_dict[proc_term] = result["count"]
                                    else:
                                        ae_count_dict[proc_term] += result["count"]
                            if details:
                                total = decoded["meta"]["results"]["total"] - limit
                                skip = 1
                            while True and details:
                                base = "https://api.fda.gov/drug/event.json?"
                                ext = "api_key=" + user.fda_api_key + "&limit=" + str(limit) + "&skip=" + str(skip) + "&search=rxcui:" + str(rxcui)
                                if details == False:
                                    ext += "&count=patient.reaction.reactionmeddrapt.exact"
                                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                                if not r.ok:
                                    r.raise_for_status()
                                    sys.exit()
                                decoded = json.loads(r.text)
                                for result in decoded["results"]:
                                    if details:
                                        for rxn in result["patient"]["reaction"]:
                                            meddra_term = rxn["reactionmeddrapt"]
                                            meddra_version =  rxn["reactionmeddraversionpt"]
                                            if meddra_term not in ae_array:
                                                temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = meddra_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                                ae_array.append(meddra_term)
                                                ae_obj_array.append(temp_ae)
                                                ae_count_dict[meddra_term] = 1
                                            else:
                                                ae_count_dict[meddra_term] += 1
                                    else:
                                        proc_term = result["term"].lower().capitalize()
                                        if proc_term not in ae_array:
                                            temp_ae = gnomics.objects.adverse_event.AdverseEvent(identifier = proc_term, identifier_type = "MedDRA Term", language = "en", source = "Drugs@FDA")
                                            ae_array.append(proc_term)
                                            ae_obj_array.append(temp_ae)
                                            ae_count_dict[proc_term] = result["count"]
                                        else:
                                            ae_count_dict[proc_term] += result["count"]
                                skip = skip + 1
                                total = total - limit
                                if total <= 0:
                                    break
                        rx_array.append(rxcui)
    if ae_array and counts == False:
        return ae_obj_array
    elif ae_array and counts == True:
        return ae_count_dict
    elif not ae_array and bad_result and counts == False:
        return []
    elif counts == True and not ae_array and bad_result:
        return ae_count_dict
    elif not ae_array and user is None:
        return []
    rxcui_mesh = False
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "mesh unique identifier" or ident["identifier_type"].lower() == "mesh uid":
            gnomics.objects.drug.Drug.rxcui(drug)
            rxcui_mesh = True
            break
    if rxcui_mesh:
        return get_adverse_events(drug)
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "drugbank" or ident["identifier_type"].lower() == "drugbank id" or ident["identifier_type"].lower() == "drugbank identifier" or ident["identifier_type"].lower() == "drugbank accession":
            gnomics.objects.drug.Drug.rxcui(drug)
            return get_adverse_events(drug)
    
# Get drug side effects.
def get_side_effects(drug):
    side_effect_array = []
    return side_effect_array

#   UNIT TESTS
def drug_adverse_event_unit_tests(rxcui, fda_api_key):
    user = User(fda_api_key = fda_api_key)
    rx_com = gnomics.objects.compound.Compound(identifier = str(rxcui), identifier_type = "RxCUI", source = "RxNorm")
    print("Getting adverse events from RxCUI (%s):" % rxcui)
    for ae_name, ae_count in get_adverse_events(rx_com, user = user, exact = False, counts = True, details = False).items():
        print("- %s: %s" % (ae_name, str(ae_count)))
    
#   MAIN
if __name__ == "__main__": main()