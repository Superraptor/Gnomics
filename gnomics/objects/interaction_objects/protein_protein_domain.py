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
#   Get protein domains from protein.
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
import gnomics.objects.protein_domain

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_protein_domain_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get protein domain identifiers for a protein.
def get_protein_domains(prot):
    prot_dom_id_array = []
    prot_dom_obj_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "CDD":
                        prot_dom_id_array.append(xref["identifier"])
                        temp_prot_dom = gnomics.objects.protein_domain.ProteinDomain(identifier = xref["identifier"], identifier_type = "CDD ID", source = "UniProt")
                        prot_dom_obj_array.append(temp_prot_dom)
                    elif xref["id_type"] == "SMART":
                        prot_domm_id_array.append(xref["identifier"])
                        temp_prot_dom = gnomics.objects.protein_domain.ProteinDomain(identifier = xref["identifier"], identifier_type = "SMART ID", source = "UniProt")
                        prot_dom_obj_array.append(temp_prot_dom)
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "CDD":
                        prot_dom_id_array.append(xref["identifier"])
                        temp_prot_dom = gnomics.objects.protein_domain.ProteinDomain(identifier = xref["identifier"], identifier_type = "CDD ID", source = "UniProt")
                        prot_dom_obj_array.append(temp_prot_dom)
                    elif xref["id_type"] == "SMART":
                        prot_domm_id_array.append(xref["identifier"])
                        temp_prot_dom = gnomics.objects.protein_domain.ProteinDomain(identifier = xref["identifier"], identifier_type = "SMART ID", source = "UniProt")
                        prot_dom_obj_array.append(temp_prot_dom)
    return prot_dom_obj_array
    
#   UNIT TESTS
def protein_protein_domain_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting protein domains from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_protein_domains(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting protein domains from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_protein_domains(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()