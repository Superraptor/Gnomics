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
#   Get LINCS ID.
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
import gnomics.objects.cell_line

#   Other imports.
from chembl_webresource_client.new_client import new_client
import json
import requests

#   MAIN
def main():
    lincs_unit_tests("LCL-1702")
    
#   Get LINCS object.
def get_lincs_obj(cell_line):
    lincs_obj_array = []
    for lincs_obj in cell_line.cell_line_objects:
        if 'object_type' in lincs_obj:
            if lincs_obj['object_type'].lower() in ['lincs object', 'lincs']:
                lincs_obj_array.append(lincs_obj['object'])
    
    if lincs_obj_array:
        return lincs_obj_array
    
    for lincs_id in get_lincs_id(cell_line):
        temp_cell_line = new_client.cell_line
        res = temp_cell_line.filter(cl_lincs_id = lincs_id)
        for sub_res in res:
            gnomics.objects.cell_line.CellLine.add_object(cell_line, obj=sub_res, object_type="LINCS Object")
            lincs_obj_array.append(sub_res)
        
    return lincs_obj_array

#   Get LINCS ID.
def get_lincs_id(cell_line):
    lincs_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["lincs", "lincs id", "lincs identifier", "cell line lincs", "cell line lincs id", "cell line lincs identifier"]):
        if iden["identifier"] not in lincs_array:
            lincs_array.append(iden["identifier"])
    return lincs_array

#   UNIT TESTS
def lincs_unit_tests(lincs_id):
    lincs_cell_line = gnomics.objects.cell_line.CellLine(identifier = lincs_id, identifier_type = "LINCS ID", language = None, source = "LINCS")
    get_lincs_obj(lincs_cell_line)

#   MAIN
if __name__ == "__main__": main()