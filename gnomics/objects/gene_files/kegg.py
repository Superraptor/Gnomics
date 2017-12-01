#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#


#
#   Get KEGG GENE.
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
import re

#   MAIN
def main():
    kegg_unit_tests()

# Get KEGG gene object.
# If no species is specified, Homo sapiens (HSA) is assumed.
def get_kegg_gene(gen, species = "Homo sapiens"):
    for gene_obj in gen.gene_objects:
        if 'object_type' in gene_obj:
            if (gene_obj['object_type'].lower() == 'kegg') and (gene_obj['species'].lower() == species):
                return gene_obj['object']
    s = KEGG()
    gene_array = []
    # Only supports a single gene for now.
    for temp_gen in gnomics.objects.gene.Gene.kegg_gene_id(gen):
        if ":" in temp_gen:
            gene_array = temp_gen.split(":")
            break
        else:
            gene_array = re.findall(r"[^\W\d_]+|\d+", temp_gen)
            break
    final_gene_from_array = gene_array[0] + ":" + gene_array[1]
    res = s.get(final_gene_from_array)
    gene = s.parse(res)
    gen.gene_objects.append({
        'object': gene,
        'object_type': "KEGG gene",
        'species': species
    })
    return gene

# Returns KEGG gene identifier.
def get_kegg_gene_id(gene):
    kegg_gene_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier"  or ident["identifier_type"].lower() == "kegg gene id" or ident["identifier_type"].lower() == "kegg gene identifier" or ident["identifier_type"].lower() == "kegg gene":
            kegg_gene_array.append(ident["identifier"])
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "uniprot" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            u = UniProt(verbose = False)
            u_dict = u.mapping(fr="ACC+ID", to="KEGG_ID", query=ident["identifier"])
            u_gene = u_dict[ident["identifier"]]
            for gen in u_gene:
                prefix = (''.join([i for i in gen if not i.isdigit()])).replace(":", "")
                sp = species.Species(identifier = prefix, identifier_type = "KEGG")
                gene.identifiers.append({
                    'identifier': gen,
                    'language': None,
                    'identifier_type': "UniProt identifier",
                    'species': sp.scientific_name,
                    'source': "UniProt"
                })
                kegg_gene_array.append(gen.replace(":", ""))
    return kegg_gene_array
    
#   UNIT TESTS
def kegg_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()