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
#   Get KEGG pathways.
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
import gnomics.objects.pathway

#   Other imports.
from bioservices import *

#   MAIN
def main():
    kegg_unit_tests("K15406", "ko00073", "map01100")

#   Get KEGG PATHWAY (map).
def get_kegg_map_pathway(path):
    kegg_map_pathway_obj_array = []
    kegg_map_pathway_array = []
    for path_obj in path.pathway_objects:
        if 'object_type' in path_obj:
            if path_obj['object_type'].lower() in ["kegg map", "kegg map pathway", "kegg map pathway id", "kegg map pathway identifier", "map pathway"]:
                kegg_map_pathway_obj_array.append(path_obj['object'])
                kegg_map_pathway_array.append(path_obj['identifier'])
    for iden in get_kegg_map_pathway_id(path):
        if iden not in kegg_map_pathway_array:
            s = KEGG()
            res = s.get(iden)
            map_pathway = s.parse(res)
            path.pathway_objects.append({
                'object': map_pathway,
                'object_type': "KEGG map pathway",
                'identifier': iden
            })
            kegg_map_pathway_obj_array.append(map_pathway)
            kegg_map_pathway_array.append(iden)
    return kegg_map_pathway_obj_array
    
#   Get KEGG PATHWAY ID (map).
def get_kegg_map_pathway_id(path):
    kegg_map_pathway_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(path.identifiers, ["kegg map", "kegg map pathway", "kegg map pathway id", "kegg map pathway identifier", "map pathway"]):
        if iden["identifier"] not in kegg_map_pathway_array:
            kegg_map_pathway_array.append(iden["identifier"])
    
    return kegg_map_pathway_array
    
#   Get KEGG PATHWAY (ko).
def get_kegg_ko_pathway(path):
    kegg_ko_pathway_obj_array = []
    kegg_ko_pathway_array = []
    for path_obj in path.pathway_objects:
        if 'object_type' in path_obj:
            if path_obj['object_type'].lower() in ["kegg ko", "kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier", "ko pathway"]:
                kegg_ko_pathway_obj_array.append(path_obj['object'])
                kegg_ko_pathway_array.append(path_obj['identifier'])
    for iden in get_kegg_ko_pathway_id(path):
        if iden not in kegg_ko_pathway_array:
            s = KEGG()
            res = s.get(iden)
            ko_pathway = s.parse(res)
            path.pathway_objects.append({
                'object': ko_pathway,
                'object_type': "KEGG ko pathway",
                'identifier': iden
            })
            kegg_ko_pathway_obj_array.append(ko_pathway)
            kegg_ko_pathway_array.append(iden)
    return kegg_ko_pathway_obj_array
            
#   Get KEGG PATHWAY ID (ko).
def get_kegg_ko_pathway_id(path):
    kegg_ko_pathway_array = []
    for ident in path.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko", "kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier", "ko pathway"]:
                if ident["identifier"] not in kegg_ko_pathway_array:
                    kegg_ko_pathway_array.append(ident["identifier"])
    for ident in path.identifiers:    
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg map", "kegg map pathway", "kegg map pathway id", "kegg map pathway identifier", "map pathway"]:
                for ko in get_kegg_map_pathway(path):
                    if ko["KO_PATHWAY"] not in kegg_ko_pathway_array:
                        path.identifiers.append({
                            'identifier': ko["KO_PATHWAY"],
                            'language': None,
                            'identifier_type': "KEGG KO PATHWAY ID",
                            'source': "KEGG"
                        })
                        kegg_ko_pathway_array.append(ko["KO_PATHWAY"])
                        
    for related_obj in path.related_objects:
        if 'object_type' in related_obj:
            if related_obj['object_type'].lower() == 'kegg orthology':
                for ko_ortho in gnomics.objects.pathway.Pathway.kegg_orthology_object(path):
                    for key, value in ko_ortho["object"]["PATHWAY"].items():
                        if key not in kegg_ko_pathway_array:
                            kegg_ko_pathway_array.append(key)
                            path.identifiers.append({
                                'identifier': key,
                                'language': None,
                                'identifier_type': "KEGG KO PATHWAY ID",
                                'source': "KEGG"
                            })
    return kegg_ko_pathway_array

#   UNIT TESTS
def kegg_unit_tests(kegg_orthology_id, kegg_ko_pathway_id, kegg_map_pathway_id):
    kegg_orthology_com = gnomics.objects.pathway.Pathway()
    kegg_orthology_com.related_objects.append({
        'identifier': kegg_orthology_id, 
        'object_type': "KEGG ORTHOLOGY"
    })
    print("Getting KEGG PATHWAY ID (ko) from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for kegg_ko in get_kegg_ko_pathway_id(kegg_orthology_com):
        print("- %s" % str(kegg_ko))

#   MAIN
if __name__ == "__main__": main()