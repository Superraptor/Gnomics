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
#   Get variations from a phenotype.
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
import gnomics.objects.phenotype
import gnomics.objects.variation

#   Other imports.
import json
import numpy
import requests
import timeit

#   MAIN
def main():
    phenotype_variation_unit_tests("HP:0000501")

# Get variations.
def get_variations(phenotype, user=None):
    var_array = []
    var_id_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(phenotype.identifiers, ["hp code", "hp id", "hp identifier", "hpo code", "hpo id", "hpo identifier", "human phenotype ontology code", "human phenotype ontology id", "human phenotype ontology identifier", "hp", "hpo", "human phenotype ontology"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            proc_id = iden["identifier"]
            if "_" in proc_id:
                proc_id.replace("_", ":")
            
            for hpo_term in gnomics.objects.phenotype.Phenotype.hpo_term(phenotype, user=user):
                server = "https://rest.ensembl.org"
                ext = "/phenotype/term/homo_sapiens/" + str(hpo_term) + "?"
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                for evidence in decoded:
                    if "Variation" in evidence and "mapped_to_accession" in evidence:
                        if evidence["mapped_to_accession"] == proc_id:
                            temp_var = gnomics.objects.variation.Variation(identifier = evidence["Variation"], identifier_type = "RS Number", language = None, source = evidence["source"])
                            
                            if "external_id" in evidence["attributes"]:
                                if "RCV" in evidence["attributes"]["external_id"]:
                                    gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = evidence["attributes"]["external_id"], identifier_type = "ClinVar Accession", language = None, source = evidence["source"])
                                
                            var_array.append(temp_var)
                            var_id_array.append(evidence["Variation"])
                            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(phenotype.identifiers, ["hp label", "hp term", "hpo label", "hpo term", "human phenotype ontology label", "human phenotype ontology term"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
                
            server = "https://rest.ensembl.org"
            ext = "/phenotype/term/homo_sapiens/" + str(iden["identifier"]) + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()

            for evidence in decoded:
                if "Variation" in evidence and "mapped_to_accession" in evidence:
                    if evidence["mapped_to_accession"] == proc_id:
                        temp_var = gnomics.objects.variation.Variation(identifier = evidence["Variation"], identifier_type = "RS Number", language = None, source = evidence["source"])

                        if "external_id" in evidence["attributes"]:
                            if "RCV" in evidence["attributes"]["external_id"]:
                                gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = evidence["attributes"]["external_id"], identifier_type = "ClinVar Accession", language = None, source = evidence["source"])

                        var_array.append(temp_var)
                        var_id_array.append(evidence["Variation"])
                
    return var_array
            
#   UNIT TESTS
def phenotype_variation_unit_tests(hpo_id):
    hpo_phen = gnomics.objects.phenotype.Phenotype(identifier = hpo_id, identifier_type = "HPO ID", source = "UMLS")
    print("\nGetting variations from HPO ID (%s):" % hpo_id)
    for var in get_variations(hpo_phen):
        for iden in var.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()