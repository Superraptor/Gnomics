#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get FDA identifier.
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
import gnomics.objects.drug

#   Other imports
import json
import requests

#   MAIN
def main():
    fda_unit_tests("731536")

#   Get FDA drug object.
def get_fda_obj(drug):
    for drug_obj in drug.drug_objects:
        if 'object_type' in drug_obj:
            if drug_obj['object_type'].lower() == 'fda drug' or drug_obj['object_type'].lower() == 'fda':
                return drug_obj['object']
    for rxcui in gnomics.objects.drug.Drug.rxcui(drug):
        base = "https://api.fda.gov/drug/"
        ext = "label.json?search=openfda.rxcui:" + rxcui + "&limit=1"
        r = requests.get(base+ext, headers = {"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.ext()
        decoded = r.json()
        fda_obj_temp = decoded["results"][0]
        drug.drug_objects.append({
            'object': fda_obj_temp,
            'object_type': "ChemSpider compound"
        })
        return fda_obj_temp   
    
#   Get FDA ID.
def get_fda_id(drug):
    fda_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "fda" or ident["identifier_type"].lower() == "fda id" or ident["identifier_type"].lower() == "fda identifier" or ident["identifier_type"].lower() == "fda name":
            fda_array.append(ident["identifier"])
    return fda_array

#   UNIT TESTS
def fda_unit_tests(rxcui):
    rx_drug = gnomics.objects.drug.Drug(identifier = rxcui, identifier_type = "RxCUI", source = "Drugs@FDA", language = None)
    print(get_fda_obj(rx_drug))
    
#   MAIN
if __name__ == "__main__": main()