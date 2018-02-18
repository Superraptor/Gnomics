#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get phenotypes from a disease.
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
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.phenotype
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    disease_phenotype_unit_tests("605543", "678")

# Get phenotypes.
def get_phenotypes(dis):
    phen_array = []
    phen_dict = {}
    phen_obj_array = []
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/disease/OMIM:" + str(ident["identifier"]) + "/phenotypes/"
            r = requests.get(server+ext)

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for obj in decoded["associations"]:
                if obj["object"]["id"] not in phen_array:
                
                    # Human Phenotype (HP) Ontology ID, also HPO ID
                    phen_array.append(obj["object"]["id"])

                    new_phen = gnomics.objects.phenotype.Phenotype(identifier = obj["object"]["id"], identifier_type = "HPO ID", language = None, source = "Monarch Initiative", taxon = "Homo sapiens")
                    phen_dict[obj["object"]["id"]] = new_phen
                    phen_obj_array.append(new_phen)
                
        
        elif ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/disease/DOID:" + ident["identifier"] + "/phenotypes/"
            r = requests.get(server+ext)

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()
            for obj in decoded["associations"]:
                if obj["object"]["id"] not in phen_array:
                
                    # Human Phenotype (HP) Ontology ID, also HPO ID
                    phen_array.append(obj["object"]["id"])

                    new_phen = gnomics.objects.phenotype.Phenotype(identifier = obj["object"]["id"], identifier_type = "HPO ID", language = None, source = "Monarch Initiative", taxon = "Homo sapiens")
                    phen_dict[obj["object"]["id"]] = new_phen
                    phen_obj_array.append(new_phen)
                    
    return phen_obj_array
        
#   UNIT TESTS
def disease_phenotype_unit_tests(omim_disease_id, doid):
    omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
    print("\nGetting phenotypes (HPO IDs) from MIM Number (%s):" % omim_disease_id)
    for phen in get_phenotypes(omim_disease):
        print("- " + str(phen))

    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    start = timeit.timeit()
    all_phens = get_phenotypes(doid_dis)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nGetting phenotypes (HPO IDs) from DOID (%s):" % doid)
    for phen in all_phens:
        print("- " + str(phen))
    
#   MAIN
if __name__ == "__main__": main()