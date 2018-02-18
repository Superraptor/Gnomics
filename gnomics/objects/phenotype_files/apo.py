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
#   Convert to APO (Ascomycete Phenotype Ontology).
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

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    apo_unit_tests()

#   Get APO ID.
def get_apo_id(phen, user=None):
    apo_id_array = []
    
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["apo", "apo id", "apo identifier", "ascomycete phenotype ontology id", "ascomycete phenotype ontology identifier"]:
            if ident["identifier"] not in apo_id_array:
                apo_id_array.append(ident["identifier"])
                
    if apo_id_array:
        return apo_id_array
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["snomedct", "snomed ct", "snomed-ct", "sctid", "sct id", "sct identifier", "snomedct id", "snomedct identifier", "snomed ct id", "snomed ct identifier", "snomed-ct id", "snomed-ct identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "SNOMEDCT/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)
                for result in decoded:
                    for subresult in result["classes"]:
                        if "APO" in subresult["@id"]:
                            apo_id = subresult["@id"].split("/obo/")[1]
                            if apo_id not in apo_id_array:
                                apo_id_array.append(apo_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=apo_id, identifier_type="APO ID", source="NCBO BioPortal", taxon="Ascomycota")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["meddra", "meddra id", "meddra identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "MEDDRA/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)
                for result in decoded:
                    for subresult in result["classes"]:
                        if "APO" in subresult["@id"]:
                            apo_id = subresult["@id"].split("/obo/")[1]
                            if apo_id not in apo_id_array:
                                apo_id_array.append(apo_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=apo_id, identifier_type="APO ID", source="NCBO BioPortal", taxon="Ascomycota")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["mesh uid", "mesh unique id", "mesh unique identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "MESH/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)
                for result in decoded:
                    for subresult in result["classes"]:
                        if "APO" in subresult["@id"]:
                            apo_id = subresult["@id"].split("/obo/")[1]
                            if apo_id not in apo_id_array:
                                apo_id_array.append(apo_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=apo_id, identifier_type="APO ID", source="NCBO BioPortal", taxon="Ascomycota")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["snmi", "snmi id", "snmi identifier", "snomed international", "snomed international id", "snomed international identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "SNMI/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)
                for result in decoded:
                    for subresult in result["classes"]:
                        if "APO" in subresult["@id"]:
                            apo_id = subresult["@id"].split("/obo/")[1]
                            if apo_id not in apo_id_array:
                                apo_id_array.append(apo_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=apo_id, identifier_type="APO ID", source="NCBO BioPortal", taxon="Ascomycota")
                
    return apo_id_array
        
#   UNIT TESTS
def apo_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()