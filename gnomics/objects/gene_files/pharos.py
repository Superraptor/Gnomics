#
#
#
#
#

#
#   Get Pharos (Tchem) gene.
#

#
#   IMPORT SOURCES:
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

#   MAIN
def main():
    pharos_unit_tests("hsa:5315")

# Returns Pharos (Tchem) identifier.
def get_pharos_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "pharos gene" or ident["identifier_type"].lower() == "pharos gene id" or ident["identifier_type"].lower() == "pharos gene identifier" or ident["identifier_type"].lower() == "pharos":
            return ident["identifier"]
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg gene id":
            gene.identifiers.append(
                {
                    'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Pharos"],
                    'language': None,
                    'identifier_type': "Pharos gene identifier",
                    'taxon': "Homo sapiens",
                    'source': "Pharos"
                }
            )
            return gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["Pharos"].split("(")[0]

#   UNIT TESTS
def pharos_unit_tests(kegg_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, taxon = "Homo sapiens", source = "KEGG")
    print("Getting Pharos (Tchem) IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    print("- %s" % get_pharos_gene_id(kegg_gene))

#   MAIN
if __name__ == "__main__": main()