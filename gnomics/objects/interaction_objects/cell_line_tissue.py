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
#   Get tissue from cell line.
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
import gnomics.objects.tissue
import gnomics.objects.cell_line

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    cell_line_tissue_unit_tests("LCL-1702")

def get_tissue(cell_line):
    tiss_id_array = []
    tissue_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["cellosaurus", "cellosaurus id", "cellosaurus identifier"]):
        for cello_obj in gnomics.objects.cell_line.CellLine.cellosaurus(cell_line):
            if cello_obj["cell_source_tissue"] not in tiss_id_array:
                temp_tissue = gnomics.objects.tissue.Tissue(identifier = cello_obj["cell_source_tissue"], identifier_type = "ChEMBL Source Tissue", source = "ChEMBL")
                taxon_array.append(temp_tissue)
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["lincs", "lincs id", "lincs identifier", "cell line lincs", "cell line lincs id", "cell line lincs identifier"]):
        for lincs_obj in gnomics.objects.cell_line.CellLine.lincs(cell_line):
            if lincs_obj["cell_source_tissue"] not in tiss_id_array:
                temp_tissue = gnomics.objects.tissue.Tissue(identifier = lincs_obj["cell_source_tissue"], identifier_type = "ChEMBL Source Tissue", source = "ChEMBL")
                tissue_array.append(temp_tissue)
                    
    return tissue_array

#   UNIT TESTS
def cell_line_tissue_unit_tests(lincs_id):
    lincs_cell_line = gnomics.objects.cell_line.CellLine(identifier = lincs_id, identifier_type = "LINCS ID", language = None, source = "ChEMBL")
    
    start = timeit.timeit()
    all_tissue = get_tissue(lincs_cell_line)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    print("Getting tissue from cell line (LINCS ID) (%s):" % lincs_id)
    for tissue in all_tissue:
        for iden in tissue.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()