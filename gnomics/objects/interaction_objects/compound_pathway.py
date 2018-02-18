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
#   Get diseases from a compound.
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
import gnomics.objects.reference

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    pathway_unit_tests("C01576", "33419-42-0", "36462", "33510", "CHEBI:4911", "83931753-9e3f-4e90-b104-e3bcd0b4d833", "", "", chemspider_security_token="")
    
# Get pathways from compound.
def get_pathways(com, source=None, pathway_assoc=None, user=None):
    path_array = []
    path_id_array = []
    
    for related_obj in com.related_objects:
        if 'object_type' in related_obj:
            if related_obj['object_type'].lower() in ["disease"]:
                any_in = 0
                for iden in related_obj['object'].identifiers:
                    if iden not in path_id_array:
                        path_id_array.append(iden)
                        path_array.append(related_obj["object"])
                    else:
                        any_in = any_in + 1
                if any_in == 0:
                    path_array.append(related_obj["object"])
    
    id_id_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["kegg compound", "kegg compound id", "kegg compound accession"]:
            if source is None:
                kegg_com_db_entry = gnomics.objects.compound.Compound.kegg_compound_db_entry(com)
                for map_id, path_name in kegg_com_db_entry["PATHWAY"].items():
                    if map_id not in path_id_array:
                        temp_pathway = gnomics.objects.pathway.Pathway(identifier = map_id, identifier_type = "KEGG map identifier", source = "KEGG")
                        com.related_objects.append({
                            "object": temp_pathway,
                            "object_type": "Pathway",
                            "identifier": map_id,
                            "source": "KEGG"
                        })
                        path_array.append(temp_pathway)
                        path_id_array.append(map_id)
            elif source.lower() in ["kegg"]:
                kegg_com_db_entry = gnomics.objects.compound.Compound.kegg_compound_db_entry(com)
                for map_id, path_name in kegg_com_db_entry["PATHWAY"].items():
                    if map_id not in path_id_array:
                        temp_pathway = gnomics.objects.pathway.Pathway(identifier = map_id, identifier_type = "KEGG map identifier", source = "KEGG")
                        com.related_objects.append({
                            "object": temp_pathway,
                            "object_type": "Pathway",
                            "identifier": map_id,
                            "source": "KEGG"
                        })
                        path_array.append(temp_pathway)
                        path_id_array.append(map_id)
        elif ident["identifier_type"].lower() in ["conceptwiki", "conceptwiki id", "conceptwiki identifier"]:
        
            base = "https://beta.openphacts.org/2.1/"
            ext = "pathways/byCompound?uri=http%3A%2F%2Fwww.conceptwiki.org%2Fconcept%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            path_array = []
            for item in decoded["result"]["items"]:
                if "wikipathways" in item["identifier"]:
                    temp_name = item["title"]
                    temp_iden = item["identifier"].split("/wikipathways/")[1]
                    temp_taxon = item["pathway_organism"]["label"]
                    
                    temp_obj = gnomics.objects.pathway.Pathway(identifier = temp_iden, identifier_type = "WikiPathways ID", source = "OpenPHACTS", name = temp_name, taxon = temp_taxon)
                    gnomics.objects.pathway.Pathway.add_identifier(temp_obj, identifier = temp_name, identifier_type = "Name", source = "OpenPHACTS")

                    path_array.append(temp_obj)
                    
            return path_array
        
        elif ident["identifier_type"].lower() in ["cas registry number", "cas", "cas rn"]:
            report_type = ""
            
            # "inferred" and "curated" do not work currently, due
            # to restrictions of the CTDBase data sources.
            if report_type == "enriched":
                report_type = "enriched"
            elif report_type == "inferred":
                report_type = "inferred"
            elif report_type == "curated":
                report_type = "curated"
            else:
                print("Because 'pathway_assoc' is set to neither 'enriched', 'inferred', or 'curated', all three will be performed.")
                report_type = None
            
            server = "http://ctdbase.org/tools/batchQuery.go"
            if source is None:
                cas_rn_array = gnomics.objects.compound.Compound.cas(com, user = user)
                for cas_rn in cas_rn_array:
                    if cas_rn not in id_id_array:
                        id_id_array.append(cas_rn)

                        extensions = []
                        if report_type is None:
                            ext_1 = "?inputType=chem&inputTerms=" + str(cas_rn) + "&report=pathways_enriched&format=JSON"
                            extensions.append(ext_1)
                        else:
                            ext = "?inputType=chem&inputTerms=" + str(cas_rn) + "&report=pathways_" + report_type + "&format=JSON"
                            extensions.append(ext)

                        for ext in extensions:

                            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()

                            for dec in decoded:
                                if "PathwayID" in dec:
                                    temp_identifier = ""
                                    
                                    if "REACT:" in dec["PathwayID"]:
                                        temp_identifier = dec["PathwayID"].split(":")[1]
                                        if temp_identifier not in path_id_array:
                                            temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "REACT", language = None, source = "CTDBase")

                                            if "PathwayName" in dec:
                                                gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")

                                            background_match_qty = None
                                            if "BackgroundMatchQty" in dec:
                                                background_match_qty = dec["BackgroundMatchQty"]
                                            cas_rn_result = None
                                            if "CasRN" in dec:
                                                 cas_rn_result = dec["CasRN"]
                                            corr_p_val = None
                                            if "CorrectedPValue" in dec:
                                                 corr_p_val = dec["CorrectedPValue"]
                                            p_val = None
                                            if "PValue" in dec:
                                                 p_val = dec["PValue"]
                                            target_match_quan = None
                                            if "TargetMatchQty" in dec:
                                                 target_match_quan = dec["TargetMatchQty"]
                                            target_total_quan = None
                                            if "TargetTotalQty" in dec:
                                                 target_total_quan = dec["TargetTotalQty"]
                                            
                                            pathway_dict = {
                                                "pathway_object": temp_pathway_obj,
                                                "background_match_quantity": background_match_qty,
                                                "cas_rn": cas_rn_result,
                                                "mesh_id": dec["ChemicalID"],
                                                "corrected_p_value": corr_p_val,
                                                "p_value": p_val,
                                                "target_match_quantity": target_match_quan,
                                                "target_total_quantity": target_total_quan
                                            }

                                            path_array.append(temp_pathway_obj)
                                            path_id_array.append(temp_identifier)

                                    elif "KEGG:" in dec["PathwayID"]:
                                        temp_identifier = dec["PathwayID"].split(":")[1]
                                        if temp_identifier not in path_id_array:
                                            temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "KEGG hsa pathway", language = None, source = "CTDBase")

                                            if "PathwayName" in dec:
                                                gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")
                                                
                                            background_match_qty = None
                                            if "BackgroundMatchQty" in dec:
                                                background_match_qty = dec["BackgroundMatchQty"]
                                            cas_rn_result = None
                                            if "CasRN" in dec:
                                                 cas_rn_result = dec["CasRN"]
                                            corr_p_val = None
                                            if "CorrectedPValue" in dec:
                                                 corr_p_val = dec["CorrectedPValue"]
                                            p_val = None
                                            if "PValue" in dec:
                                                 p_val = dec["PValue"]
                                            target_match_quan = None
                                            if "TargetMatchQty" in dec:
                                                 target_match_quan = dec["TargetMatchQty"]
                                            target_total_quan = None
                                            if "TargetTotalQty" in dec:
                                                 target_total_quan = dec["TargetTotalQty"]

                                            pathway_dict = {
                                                "object": temp_pathway_obj,
                                                "background_match_quantity": background_match_qty,
                                                "cas_rn": cas_rn_result,
                                                "mesh_id": dec["ChemicalID"],
                                                "corrected_p_value": corr_p_val,
                                                "p_value": p_val,
                                                "target_match_quantity": target_match_quan,
                                                "target_total_quantity": target_total_quan
                                            }

                                            path_array.append(temp_pathway_obj)
                                            path_id_array.append(temp_identifier)

                                        else:
                                            print("The input '%s' produced no results. The object was not found." % (dec["Input"]))


            elif source.lower() in ["ctdbase", "ctd"]:
                cas_rn_array = gnomics.objects.compound.Compound.cas(com, user = user)
                for cas_rn in cas_rn_array:
                    if cas_rn not in id_id_array:
                        id_id_array.append(cas_rn)

                        extensions = []
                        if report_type is None:
                            ext_1 = "?inputType=chem&inputTerms=" + str(cas_rn) + "&report=pathways_enriched&format=JSON"
                            extensions.append(ext_1)
                        else:
                            ext = "?inputType=chem&inputTerms=" + str(cas_rn) + "&report=pathways_" + report_type + "&format=JSON"
                            extensions.append(ext)

                        for ext in extensions:

                            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                            if not r.ok:
                                r.raise_for_status()
                                sys.exit()

                            decoded = r.json()
                            
                            for dec in decoded:
                                if "PathwayID" in dec:
                                    temp_identifier = ""
                                    
                                    if "REACT:" in dec["PathwayID"]:
                                        temp_identifier = dec["PathwayID"].split(":")[1]
                                        if temp_identifier not in path_id_array:
                                            temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "REACT", language = None, source = "CTDBase")

                                            if "PathwayName" in dec:
                                                gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")

                                            background_match_qty = None
                                            if "BackgroundMatchQty" in dec:
                                                background_match_qty = dec["BackgroundMatchQty"]
                                            cas_rn_result = None
                                            if "CasRN" in dec:
                                                 cas_rn_result = dec["CasRN"]
                                            corr_p_val = None
                                            if "CorrectedPValue" in dec:
                                                 corr_p_val = dec["CorrectedPValue"]
                                            p_val = None
                                            if "PValue" in dec:
                                                 p_val = dec["PValue"]
                                            target_match_quan = None
                                            if "TargetMatchQty" in dec:
                                                 target_match_quan = dec["TargetMatchQty"]
                                            target_total_quan = None
                                            if "TargetTotalQty" in dec:
                                                 target_total_quan = dec["TargetTotalQty"]
                                            
                                            pathway_dict = {
                                                "pathway_object": temp_pathway_obj,
                                                "background_match_quantity": background_match_qty,
                                                "cas_rn": cas_rn_result,
                                                "mesh_id": dec["ChemicalID"],
                                                "corrected_p_value": corr_p_val,
                                                "p_value": p_val,
                                                "target_match_quantity": target_match_quan,
                                                "target_total_quantity": target_total_quan
                                            }

                                            path_array.append(temp_pathway_obj)
                                            path_id_array.append(temp_identifier)

                                    elif "KEGG:" in dec["PathwayID"]:
                                        temp_identifier = dec["PathwayID"].split(":")[1]
                                        if temp_identifier not in path_id_array:
                                            temp_pathway_obj = gnomics.objects.pathway.Pathway(identifier = temp_identifier, identifier_type = "KEGG hsa pathway", language = None, source = "CTDBase")

                                            if "PathwayName" in dec:
                                                gnomics.objects.pathway.Pathway.add_identifier(temp_pathway_obj, identifier = dec["PathwayName"], identifier_type = "Name", language = "en", source = "CTDBase")
                                                
                                            background_match_qty = None
                                            if "BackgroundMatchQty" in dec:
                                                background_match_qty = dec["BackgroundMatchQty"]
                                            cas_rn_result = None
                                            if "CasRN" in dec:
                                                 cas_rn_result = dec["CasRN"]
                                            corr_p_val = None
                                            if "CorrectedPValue" in dec:
                                                 corr_p_val = dec["CorrectedPValue"]
                                            p_val = None
                                            if "PValue" in dec:
                                                 p_val = dec["PValue"]
                                            target_match_quan = None
                                            if "TargetMatchQty" in dec:
                                                 target_match_quan = dec["TargetMatchQty"]
                                            target_total_quan = None
                                            if "TargetTotalQty" in dec:
                                                 target_total_quan = dec["TargetTotalQty"]

                                            pathway_dict = {
                                                "object": temp_pathway_obj,
                                                "background_match_quantity": background_match_qty,
                                                "cas_rn": cas_rn_result,
                                                "mesh_id": dec["ChemicalID"],
                                                "corrected_p_value": corr_p_val,
                                                "p_value": p_val,
                                                "target_match_quantity": target_match_quan,
                                                "target_total_quantity": target_total_quan
                                            }

                                            path_array.append(temp_pathway_obj)
                                            path_id_array.append(temp_identifier)

                                        else:
                                            print("The input '%s' produced no results. The object was not found." % (dec["Input"]))
    if path_array:
        return path_array
    
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["chebi", "chebi id", "chebi identifier"]:
            gnomics.objects.compound.Compound.cas(com)
            return get_pathways(com, source = source, pathway_assoc = pathway_assoc)
        elif ident["identifier_type"].lower() in ["pubchem cid", "cid"]:
            gnomics.objects.compound.Compound.cas(com)
            return get_pathways(com, source = source, pathway_assoc = pathway_assoc)
        elif (ident["identifier_type"].lower() in ["chemspider", "chemspider id", "chemspider identifier"]) and user is not None:
            gnomics.objects.compound.Compound.cas(com, user=user)
            return get_pathways(com, source=source, pathway_assoc=pathway_assoc, user=user)
        
    return path_array
    

#   UNIT TESTS
def pathway_unit_tests(kegg_compound_id, cas_rn, pubchem_cid, chemspider_id, chebi_id, conceptwiki_id, openphacts_app_id, openphacts_app_key, chemspider_security_token=None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token, openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
        print("User created successfully.\n")
        
        conceptwiki_com = gnomics.objects.compound.Compound(identifier = str(conceptwiki_id), identifier_type = "ConceptWiki ID", source = "OpenPHACTS")
        print("Getting pathways from ConceptWiki ID (%s):" % conceptwiki_id)
        for path in get_pathways(conceptwiki_com, user = user):
            for iden in path.identifiers:
                if iden["identifier_type"] == "Name":
                    print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("\nGetting pathways from ChemSpider ID (%s):" % chemspider_id)
        for path in get_pathways(chemspider_com, user = user):
            for iden in path.identifiers:
                if iden["identifier_type"] == "Name":
                    print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
                    
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting pathways from ChEBI ID (%s):" % chebi_id)
        for path in get_pathways(chebi_com):
            for iden in path.identifiers:
                if iden["identifier_type"] == "Name":
                    print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    
        kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting pathways from KEGG COMPOUND ID (%s):" % kegg_compound_id)
        for path in get_pathways(kegg_com):
            for iden in path.identifiers:
                print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))

        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("\nGetting pathways from CAS Registry Number (%s):" % cas_rn)
        for path in get_pathways(cas_com):
            for iden in path.identifiers:
                if iden["identifier_type"] == "Name":
                    print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))

        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting pathways from PubChem CID (%s):" % pubchem_cid)
        
        start = timeit.timeit()
        all_pathways = get_pathways(pubchem_com)
        end = timeit.timeit()

        for path in all_pathways:
            for iden in path.identifiers:
                if iden["identifier_type"] == "Name":
                    print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
                    
        print("TIME ELAPSED: %s seconds." % str(end - start))
    
#   MAIN
if __name__ == "__main__": main()