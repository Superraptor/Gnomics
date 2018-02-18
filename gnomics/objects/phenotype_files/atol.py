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
#   Convert to Animal Trait Ontology for Livestock (ATOL).
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
    atol_unit_tests()

#   Get ATOL ID.
def get_atol_id(phen, user=None):
    atol_id_array = []
    
    for ident in phen.identifiers:
        if ident["identifier_type"].lower() in ["atol", "atol id", "atol identifier", "animal trait ontology for livestock id", "animal trait ontology for livestock identifier", "animal trait ontology for livestock"]:
            if ident["identifier"] not in atol_id_array:
                atol_id_array.append(ident["identifier"])
           
    if atol_id_array:
        return atol_id_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["fbcv", "fbcv id", "fbcv identifier", "fb-cv", "fb-cv id", "fb-cv identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "FB-CV/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for result in decoded:
                    for subresult in result["classes"]:
                        if "ATOL" in subresult["@id"]:
                            atol_id = subresult["@id"].split("/obo/")[1]
                            if atol_id not in atol_id_array:
                                atol_id_array.append(atol_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=atol_id, identifier_type="ATOL ID", source="NCBO BioPortal")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["fypo", "fypo id", "fypo identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "FYPO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for result in decoded:
                    for subresult in result["classes"]:
                        if "ATOL" in subresult["@id"]:
                            atol_id = subresult["@id"].split("/obo/")[1]
                            if atol_id not in atol_id_array:
                                atol_id_array.append(atol_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=atol_id, identifier_type="ATOL ID", source="NCBO BioPortal")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["mesh", "mesh unique id", "mesh unique identifier"]):
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
                        if "ATOL" in subresult["@id"]:
                            atol_id = subresult["@id"].split("/obo/")[1]
                            if atol_id not in atol_id_array:
                                atol_id_array.append(atol_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=atol_id, identifier_type="ATOL ID", source="NCBO BioPortal")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["oba", "oba id", "oba identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "OBA/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for result in decoded:
                    for subresult in result["classes"]:
                        if "ATOL" in subresult["@id"]:
                            atol_id = subresult["@id"].split("/obo/")[1]
                            if atol_id not in atol_id_array:
                                atol_id_array.append(atol_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=atol_id, identifier_type="ATOL ID", source="NCBO BioPortal")
                                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(tissue.identifiers, ["vt", "vt id", "vt identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            if user.ncbo_api_key is not None:
                ids_completed.append(iden["identifier"])

                temp_ident = iden["identifier"]
                if "_" not in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")
                elif ":" in temp_ident:
                    temp_ident = temp_ident.replace(":", "_")

                base = "http://data.bioontology.org/ontologies/"
                ext = "VT/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F" + temp_ident + "/mappings/?apikey=" + user.ncbo_api_key
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                for result in decoded:
                    for subresult in result["classes"]:
                        if "ATOL" in subresult["@id"]:
                            atol_id = subresult["@id"].split("/obo/")[1]
                            if atol_id not in atol_id_array:
                                atol_id_array.append(atol_id)
                                gnomics.objects.phenotype.Phenotype.add_identifier(phen, identifier=atol_id, identifier_type="ATOL ID", source="NCBO BioPortal")
    
    return atol_id_array
        
#   UNIT TESTS
def atol_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()