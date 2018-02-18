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
#   Get Cellosaurus ID.
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
    cellosaurus_unit_tests("CVCL_0417")
    
#   Get Cellosaurus object.
def get_cellosaurus_obj(cell_line):
    cello_obj_array = []
    for cello_obj in cell_line.cell_line_objects:
        if 'object_type' in cello_obj:
            if cello_obj['object_type'].lower() in ['cellosaurus object', 'cellosaurus']:
                cello_obj_array.append(cello_obj['object'])
    
    if cello_obj_array:
        return cello_obj_array
    
    for cello_id in get_cellosaurus_id(cell_line):
        temp_cell_line = new_client.cell_line
        res = temp_cell_line.filter(cellosaurus_id=cello_id)
        for sub_res in res:
            gnomics.objects.cell_line.CellLine.add_object(cell_line, obj=sub_res, object_type="Cellosaurus Objct")
            cello_obj_array.append(sub_res)
        
    return cello_obj_array

#   Get Cellosaurus ID.
def get_cellosaurus_id(cell_line):
    cello_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["cellosaurus", "cellosaurus id", "cellosaurus identifier"]):
        if iden["identifier"] not in cello_array:
            cello_array.append(iden["identifier"])
    return cello_array

#   UNIT TESTS
def cellosaurus_unit_tests(cellosaurus_id):
    cello_cell_line = gnomics.objects.cell_line.CellLine(identifier = cellosaurus_id, identifier_type = "Cellosaurus ID", language = None, source = "ChEMBL")
    get_cellosaurus_obj(cello_cell_line)

#   MAIN
if __name__ == "__main__": main()