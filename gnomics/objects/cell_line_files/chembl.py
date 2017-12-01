#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#

#
#   Get ChEMBL ID.
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
    chembl_unit_tests("CHEMBL3307686", "CVCL_0417")
    
#   Get ChEMBL object.
def get_chembl_obj(cell_line):
    chembl_obj_array = []
    for chembl_obj in cell_line.cell_line_objects:
        if 'object_type' in chembl_obj:
            if chembl_obj['object_type'].lower() == 'chembl object' or chembl_obj['object_type'].lower() == 'chembl':
                chembl_obj_array.append(chembl_obj['object'])
    if chembl_obj_array:
        return chembl_obj_array
    for chembl_id in get_chembl_id(cell_line):
        temp_cell_line = new_client.cell_line
        res = temp_cell_line.filter(chembl_id = chembl_id)
        cell_line.cell_line_objects.append(
            {
                'object': res,
                'object_type': "ChEMBL Object"
            }
        )
        chembl_obj_array.append(res)
    return chembl_obj_array

#   Get ChEMBL ID.
def get_chembl_id(cell_line):
    chembl_array = []
    for ident in cell_line.identifiers:
        if ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            chembl_array.append(ident["identifier"])
    if chembl_array:
        return chembl_array
    for ident in cell_line.identifiers:
        if ident["identifier_type"].lower() == "cellosaurus" or ident["identifier_type"].lower() == "cellosaurus id" or ident["identifier_type"].lower() == "cellosaurus identifier":
            for cello_obj in gnomics.objects.cell_line.CellLine.cellosaurus_obj(cell_line):
                chembl_array.append(cello_obj["cell_chembl_id"])
    return chembl_array

#   UNIT TESTS
def chembl_unit_tests(chembl_id, cellosaurus_id):
    chembl_cell_line = gnomics.objects.cell_line.CellLine(identifier = chembl_id, identifier_type = "ChEMBL ID", language = None, source = "ChEMBL")
    get_chembl_obj(chembl_cell_line)
    cello_cell_line = gnomics.objects.cell_line.CellLine(identifier = str(cellosaurus_id), identifier_type = "Cellosaurus ID", source = "ChEMBL")
    print("Getting ChEMBL ID from Cellosaurus ID (%s):" % cellosaurus_id)
    for cl in get_chembl_id(cello_cell_line):
        print("- %s" % str(cl))

#   MAIN
if __name__ == "__main__": main()