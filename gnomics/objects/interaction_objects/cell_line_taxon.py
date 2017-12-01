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

#   MAIN
def main():
    cell_line_taxon_unit_tests("CVCL_0417")

def get_taxon(cell_line):
    taxon_array = []
    for ident in cell_line.identifiers:
        if ident["identifier_type"].lower() == "cellosaurus" or ident["identifier_type"].lower() == "cellosaurus id" or ident["identifier_type"].lower() == "cellosaurus identifier":
            for cello_obj in gnomics.objects.cell_line.CellLine.cellosaurus_obj(cell_line):
                temp_taxon = gnomics.objects.taxon.Taxon(identifier = cello_obj["cell_source_tax_id"], identifier_type = "NCBI Taxonomy ID", source = "ChEMBL")
                taxon_array.append(temp_taxon)
    return taxon_array

#   UNIT TESTS
def cell_line_taxon_unit_tests(cellosaurus_id):
    cello_cell_line = gnomics.objects.cell_line.CellLine(identifier = cellosaurus_id, identifier_type = "Cellosaurus ID", language = None, source = "ChEMBL")
    print("Getting taxon (NCBI Taxonomy ID) from cell line (Cellosaurus ID) (%s):" % cellosaurus_id)
    for taxon in get_taxon(cello_cell_line):
        for iden in taxon.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()