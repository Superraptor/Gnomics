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
#   Get taxon from protein.
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
import gnomics.objects.protein
import gnomics.objects.taxon

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_taxon_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get taxon.
def get_taxon(prot):
    taxon_id_array = []
    taxon_obj_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                sci_name = x["organism_scientific_name"]
                com_name = x["organism_common_name"]
                temp_tax = gnomics.objects.taxon.Taxon(identifier = sci_name, name = com_name, identifier_type = "scientific name", language = "la", source = "UniProt")
                gnomics.objects.taxon.Taxon.add_identifier(temp_tax, identifier = x["ncbi_taxonomy_id"], identifier_type = "NCBI TaxID", source = "UniProt", name = com_name)
                taxon_id_array.append(x["ncbi_taxonomy_id"])
                taxon_obj_array.append(temp_tax)
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                sci_name = x["organism_scientific_name"]
                com_name = x["organism_common_name"]
                temp_tax = gnomics.objects.taxon.Taxon(identifier = sci_name, name = com_name, identifier_type = "scientific name", language = "la", source = "UniProt")
                gnomics.objects.taxon.Taxon.add_identifier(temp_tax, identifier = x["ncbi_taxonomy_id"], identifier_type = "NCBI TaxID", source = "UniProt", name = com_name)
                taxon_id_array.append(x["ncbi_taxonomy_id"])
                taxon_obj_array.append(temp_tax)
    return taxon_obj_array
    
#   UNIT TESTS
def protein_taxon_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting taxon from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_taxon(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting taxon from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_taxon(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()