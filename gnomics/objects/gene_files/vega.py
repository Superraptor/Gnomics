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

#   Other imports.
from bioservices import *

#   MAIN
def main():
    vega_unit_tests()

# Returns Vega gene identifier.
def get_vega_gene_id(gene):
    vega_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["vega gene", "vega gene id", "vega gene identifier", "vega"]:
            vega_array.append(ident["identifier"])
            
    if vega_array:
        return vega_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["kegg", "kegg id", "kegg identifier", "kegg gene", "kegg gene id", "kegg gene identifier"]:
            for obj in gnomics.objects.gene.Gene.kegg_gene(gene):
                if "DBLINKS" in obj:
                    if "Vega" in obj["DBLINKS"]:
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = obj["DBLINKS"]["Vega"], language = None, identifier_type = "Vega gene identifier", source = "Vega")
                        vega_array.append(obj["DBLINKS"]["Vega"])

    return vega_array
    
#   UNIT TESTS
def vega_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()