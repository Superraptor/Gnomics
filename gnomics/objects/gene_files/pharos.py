#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       MYGENE
#           https://pypi.python.org/pypi/mygene
#

#
#   Get Pharos (Tchem) gene.
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
import gnomics.objects.gene

#   Other imports.
import mygene

#   MAIN
def main():
    pharos_unit_tests("hsa:5315")

# Returns Pharos (Tchem) identifier.
def get_pharos_gene_id(gene):
    pharos_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["pharos gene", "pharos gene id", "pharos gene identifier", "pharos"]:
            pharos_array.append(ident["identifier"])
            
    if pharos_array:
        return pharos_array
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["kegg", "kegg id", "kegg identifier", "kegg gene id"]:
            for kegg_obj in gnomics.objects.gene.Gene.kegg_gene(gene):
                if kegg_obj["DBLINKS"]["Pharos"].split("(")[0] not in pharos_array:
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier=kegg_obj["DBLINKS"]["Pharos"].split("(")[0], identifier_type="Pharos Gene ID", taxon=ident["taxon"], source="KEGG", language=None)
                    pharos_array.append(kegg_obj["DBLINKS"]["Pharos"].split("(")[0])
        
    return pharos_array
        
#   UNIT TESTS
def pharos_unit_tests(kegg_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, taxon = "Homo sapiens", source = "KEGG")
    print("Getting Pharos (Tchem) IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    print("- %s" % get_pharos_gene_id(kegg_gene))

#   MAIN
if __name__ == "__main__": main()