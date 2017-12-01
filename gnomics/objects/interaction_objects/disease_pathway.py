#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get pathways associated with a disease.
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
import gnomics.objects.disease
import gnomics.objects.pathway

#   Other imports.
from decimal import *
import requests

#   MAIN
def main():
    pathway_unit_tests("219700", "H00286")

# Return pathways.
#
# Note that only inferred pathways will be returned.
def get_pathways(disease, user = None):
    pathway_array = []
    pathway_obj_array = []
    for ident in disease.identifiers:
        if ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id" or ident["identifier_type"].lower() == "omim identifier" or ident["identifier_type"].lower() == "omim disease id" or ident["identifier_type"].lower() == "mim number" or ident["identifier_type"].lower() == "mim":
            server = "http://ctdbase.org/tools/batchQuery.go"
            ext = "?inputType=disease&inputTerms=OMIM:" + str(ident["identifier"]) + "&report=pathways_inferred&format=JSON"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            sorted_output = []
            for dec in decoded:
                if "PathwayID" in dec:
                    temp_identifier = ""
                    if "REACT:" in dec["PathwayID"]:
                        temp_identifier = dec["PathwayID"].split(":")[1]
                        temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "REACT", language = None, source = "CTDBase")
                        if "PathwayName" in dec:
                            gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")
                        pathway_dict = {
                            "pathway_object": temp_pathway_obj,
                            "inference_gene_symbol": dec["InferenceGeneSymbol"],
                            "mim_number": dec["DiseaseID"],
                            "disease_name": dec["DiseaseName"],
                            "disease_categories": dec["DiseaseCategories"].split("|")
                        }
                        sorted_output.append(pathway_dict)
                        pathway_obj_array.append(temp_pathway_obj)
                    elif "KEGG:" in dec["PathwayID"]:
                        temp_identifier = dec["PathwayID"].split(":")[1]
                        temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "KEGG hsa pathway", language = None, source = "CTDBase")
                        if "PathwayName" in dec:
                            gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")
                        pathway_dict = {
                            "pathway_object": temp_pathway_obj,
                            "inference_gene_symbol": dec["InferenceGeneSymbol"],
                            "mim_number": dec["DiseaseID"],
                            "disease_name": dec["DiseaseName"],
                            "disease_categories": dec["DiseaseCategories"].split("|")
                        }
                        sorted_output.append(pathway_dict)
                        pathway_obj_array.append(temp_pathway_obj)
                    else:
                        print("The input '%s' produced no results. The object was not found." % (dec["Input"]))
            return pathway_obj_array
        elif ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg disease id":
            sorted_output = []
            for key, val in gnomics.objects.disease.Disease.kegg_disease(disease)["PATHWAY"].items():
                if key not in pathway_array:
                    pathway_array.append(key)
                    new_path = gnomics.objects.pathway.Pathway(identifier = key, identifier_type = "KEGG hsa PATHWAY ID", language = None, source = "KEGG")
                    gnomics.objects.pathway.Pathway.add_identifier(new_path, identifier = val, identifier_type = "KEGG Pathway Name", language = "en", source = "KEGG")
                    pathway_dict = {
                        "pathway_object": new_path,
                        "identifier": key
                    }
                    sorted_output.append(pathway_dict)
                    pathway_obj_array.append(temp_pathway_obj)
            return pathway_obj_array
    return pathway_obj_array
    
#   UNIT TESTS
def pathway_unit_tests(omim_disease_id, kegg_disease_id):
    omim_disease = gnomics.objects.disease.Disease(identifier = str(omim_disease_id), identifier_type = "MIM Number", source = "OMIM")
    print("Getting pathway names from MIM Number (%s):" % omim_disease_id)
    for path in get_pathways(omim_disease):
        for iden in path["pathway_object"].identifiers:
            if iden["identifier_type"].lower() == "name":
                print("- " + str(iden["identifier"]))
    kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG DISEASE ID", source = "KEGG")
    print("\nGetting pathways (KEGG PATHWAY names) from KEGG DISEASE ID (%s):" % kegg_disease_id)
    for path in get_pathways(kegg_disease):
        for iden in path["pathway_object"].identifiers:
            if iden["identifier_type"].lower() == "kegg pathway name":
                print("- " + str(iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()