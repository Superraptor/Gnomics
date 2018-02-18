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
#   Get DrugBank identifier.
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

#   MAIN
def main():
    drugbank_unit_tests("5640")

#   Get DrugBank ID.
def get_drugbank_id(drug):
    drugbank_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["drugbank accession", "drugbank", "drugbank id", "drugbank identifier"]:
            if ident["identifier"] not in drugbank_array:
                drugbank_array.append(ident["identifier"])
                
    if drugbank_array:
        return drugbank_array
                
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() in ["rxcui", "rxnorm id", "rxnorm identifier"]:
            gnomics.objects.drug.Drug.rxnorm_obj(drug)
            if "drugbank" in gnomics.objects.drug.Drug.rxnorm_obj(drug):
                drugbank_ids = gnomics.objects.drug.Drug.rxnorm_obj(drug)["drugbank"]
                drugbank_array.extend(drugbank_ids)
                for iden in drugbank_ids:
                    gnomics.objects.drug.Drug.add_identifier(drug, identifier=iden, identifier_type="DrugBank ID", source="RxNorm")
            
    return drugbank_array

#   UNIT TESTS
def drugbank_unit_tests(rxcui):
    rx_drug = gnomics.objects.drug.Drug(identifier=str(rxcui), identifier_type="RxCUI", source="RxNorm")
    print("\nGetting DrugBank IDs from RxCUI (%s):" % rxcui)
    for drugbank in get_drugbank_id(rx_drug):
        print("- " + str(drugbank))
    
#   MAIN
if __name__ == "__main__": main()