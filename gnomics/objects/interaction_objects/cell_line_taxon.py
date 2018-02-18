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
#   Get taxon from cell line.
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
import gnomics.objects.taxon
import gnomics.objects.cell_line

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    cell_line_taxon_unit_tests("CVCL_0417")

def get_taxon(cell_line):
    tax_id_array = []
    taxon_array = []
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["cellosaurus", "cellosaurus id", "cellosaurus identifier"]):
        for cello_obj in gnomics.objects.cell_line.CellLine.cellosaurus(cell_line):
            if cello_obj["cell_source_tax_id"] not in tax_id_array:
                temp_taxon = gnomics.objects.taxon.Taxon(identifier = cello_obj["cell_source_tax_id"], identifier_type = "NCBI Taxonomy ID", source = "ChEMBL")
                taxon_array.append(temp_taxon)
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(cell_line.identifiers, ["lincs", "lincs id", "lincs identifier", "cell line lincs", "cell line lincs id", "cell line lincs identifier"]):
        
        for lincs_obj in gnomics.objects.cell_line.CellLine.lincs(cell_line):
            if lincs_obj["cell_source_tax_id"] not in tax_id_array:
                temp_taxon = gnomics.objects.taxon.Taxon(identifier = lincs_obj["cell_source_tax_id"], identifier_type = "NCBI Taxonomy ID", source = "ChEMBL", name = lincs_obj["cell_source_organism"])
                taxon_array.append(temp_taxon)
                    
    return taxon_array

#   UNIT TESTS
def cell_line_taxon_unit_tests(cellosaurus_id):
    cello_cell_line = gnomics.objects.cell_line.CellLine(identifier = cellosaurus_id, identifier_type = "Cellosaurus ID", language = None, source = "ChEMBL")
    
    start = timeit.timeit()
    all_taxon = get_taxon(cello_cell_line)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    print("Getting taxon (NCBI Taxonomy ID) from cell line (Cellosaurus ID) (%s):" % cellosaurus_id)
    for taxon in all_taxon:
        for iden in taxon.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()