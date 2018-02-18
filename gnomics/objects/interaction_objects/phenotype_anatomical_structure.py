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
#   Get anatomical structures from phenotype.
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
import gnomics.objects.anatomical_structure
import gnomics.objects.phenotype

#   Other imports.
import json
import re
import requests
import timeit

#   MAIN
def main():
    phenotype_anatomical_structure_unit_tests("HP_0000527")
     
#   Get anatomical structures from phenotype.
def get_anatomical_structures(phenotype):
    anat_array = []
    
    for ident in phenotype.identifiers:
        if ident["identifier_type"].lower() in ["hp id", "hpo identifier", "hpo id", "hp identifier"]:

            base = "https://raw.githubusercontent.com/obophenotype/"
            ext = "human-phenotype-ontology/master/scratch/hp-equivalence-axioms.obo"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.text.split("\n")
            
            proc_ident = ident["identifier"]
            if "_" in proc_ident:
                proc_ident = proc_ident.replace("_", ":")
            found = False
            for line in decoded:
                if proc_ident in line:
                    found = True
                if found == True and "[Term]" in line:
                    break
                if found == True and "UBERON:":
                    match = re.findall('UBERON:\d+', line)
                    if match:
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = match[0], identifier_type = "UBERON ID", source = "Human Phenotype Ontology")
                        anat_array.append(temp_anat)
                   
    return anat_array
    
#   UNIT TESTS
def phenotype_anatomical_structure_unit_tests(hp_id):
    hp_phen = gnomics.objects.phenotype.Phenotype(identifier = hp_id, identifier_type = "HPO ID", source = "Ontobee")
    print("\nGetting anatomical structure identifiers from phenotype (%s):" % hp_id)
    for anat in get_anatomical_structures(hp_phen):
        for iden in anat.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()