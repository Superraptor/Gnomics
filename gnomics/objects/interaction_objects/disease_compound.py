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
#   Get compounds from diseases.
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
import gnomics.objects.compound
import gnomics.objects.disease

#   Other imports.
import requests
import timeit

#   MAIN
def main():
    disease_compound_unit_tests("2394", "D000544")

#   Get compounds.
def get_compounds(dis):
    com_array = []
    com_obj_dict = {}
    com_obj_array = []
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            server = "https://api.monarchinitiative.org/api"
            ext = "/bioentity/disease/DOID:" + ident["identifier"] + "/substance/"
            r = requests.get(server+ext)
            
            if not r.ok:
                continue
            else:    
                decoded = r.json()
                for chem_id in decoded:
                    if chem_id not in com_array:
                        chebi_com = gnomics.objects.compound.Compound(identifier = str(chem_id), identifier_type = "ChEBI ID", source = "ChEBI")
                        com_array.append(chem_id)
                        com_obj_dict[chem_id] = chebi_com
                        com_obj_array.append(chebi_com)
        
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh uid"]:
            server = "http://ctdbase.org/tools/batchQuery.go"
            ext = "?inputType=disease&inputTerms=" + str(ident["identifier"]) + "&report=chems&format=JSON"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.json()
            
            for interaction in decoded:
                if "CasRN" in interaction and "ChemicalID" in interaction:
                    if interaction["CasRN"] not in com_array and interaction["ChemicalID"] not in com_array:
                        cas_com = gnomics.objects.compound.Compound(identifier = str(interaction["CasRN"]), identifier_type = "CAS Registry Number", source = "CTDBase")
                        com_array.append(interaction["CasRN"])
                        com_array.append(interaction["ChemicalID"])
                        com_obj_dict[interaction["CasRN"]] = cas_com
                        com_obj_array.append(cas_com)
                
                elif "ChemicalID" in interaction:
                    if interaction["ChemicalID"] not in com_array:
                    
                        mesh_com = gnomics.objects.compound.Compound(identifier = str(interaction["ChemicalID"]), identifier_type = "MeSH UID", source = "CTDBase")
                        com_array.append(interaction["ChemicalID"])
                        com_obj_dict[interaction["ChemicalID"]] = mesh_com
                        com_obj_array.append(mesh_com)
                    
                elif "CasRN" in interaction:
                    if interaction["CasRN"] not in com_array:
                        
                        cas_com = gnomics.objects.compound.Compound(identifier = str(interaction["CasRN"]), identifier_type = "CAS Registry Number", source = "CTDBase")
                        com_array.append(interaction["CasRN"])
                        com_obj_dict[interaction["CasRN"]] = cas_com
                        com_obj_array.append(cas_com)
                    
                else:
                    print("This record contained no MeSH UID or CAS RN and will not be added to the list's records for that reason.")
                    print("The rest of the record's contents are as follows:")
                    print(interaction)

    return com_obj_array
    

#   UNIT TESTS
def disease_compound_unit_tests(doid, mesh_uid):
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
        
    print("\nGetting compounds (ChEBI IDs) from DOID (%s):" % doid)
    for com_key in get_compounds(doid_dis):
        for iden in com_key.identifiers:
                print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    mesh_dis = gnomics.objects.disease.Disease(identifier = str(mesh_uid), identifier_type = "MeSH UID", source = "MeSH")
        
    start = timeit.timeit()
    all_coms = get_compounds(mesh_dis)
    end = timeit.timeit()
        
    print("\nGetting compounds (ChEBI IDs) from MeSH disease UID (%s):" % mesh_uid)
    for com_key in all_coms:
        for iden in com_key.identifiers:
                print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    print("TIME ELAPSED: %s seconds." % str(end - start))

#   MAIN
if __name__ == "__main__": main()