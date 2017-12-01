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
#   Get Vega gene.
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
import gnomics.objects.gene

#   MAIN
def main():
    vega_unit_tests()

# Returns Vega gene identifier.
def get_vega_gene_id(gene, taxon = "Homo sapiens"):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "vega gene" or ident["identifier_type"].lower() == "vega gene id" or ident["identifier_type"].lower() == "vega gene identifier" or ident["identifier_type"].lower() == "vega":
            return ident["identifier"]
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier":
            gnomics.objects.gene.Gene.add_identifier(identifier = gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Vega"], language = None, identifier_type = "Vega gene identifier", taxon = taxon, source = "Vega")
            return gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Vega"]
    
#   UNIT TESTS
def vega_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()