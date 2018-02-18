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
#   Get protein families from protein.
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
import gnomics.objects.protein_family

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_protein_family_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get protein family identifiers for a protein.
def get_protein_families(prot):
    
    prot_fam_id_array = []
    prot_fam_obj_array = []
            
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
    
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "Pfam":
                        prot_fam_id_array.append(xref["identifier"])
                        temp_prot_fam = gnomics.objects.protein_family.ProteinFamily(identifier = xref["identifier"], identifier_type = "Pfam ID", source = "UniProt")
                        prot_fam_obj_array.append(temp_prot_fam)
                    elif xref["id_type"] == "TIGRFAM":
                        prot_fam_id_array.append(xref["identifier"])
                        temp_prot_fam = gnomics.objects.protein_family.ProteinFamily(identifier = xref["identifier"], identifier_type = "TIGRFAM ID", source = "UniProt")
                        prot_fam_obj_array.append(temp_prot_fam)
            
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                xrefs = x["db_reference"]
                for xref in xrefs:
                    if xref["id_type"] == "Pfam":
                        prot_fam_id_array.append(xref["identifier"])
                        temp_prot_fam = gnomics.objects.protein_family.ProteinFamily(identifier = xref["identifier"], identifier_type = "Pfam ID", source = "UniProt")
                        prot_fam_obj_array.append(temp_prot_fam)
                    elif xref["id_type"] == "TIGRFAM":
                        prot_fam_id_array.append(xref["identifier"])
                        temp_prot_fam = gnomics.objects.protein_family.ProteinFamily(identifier = xref["identifier"], identifier_type = "TIGRFAM ID", source = "UniProt")
                        prot_fam_obj_array.append(temp_prot_fam)
            
    return prot_fam_obj_array
    
#   UNIT TESTS
def protein_protein_family_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    print("NOT FUNCTIONAL.")
    
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    
    print("Getting protein families from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_protein_families(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    
    print("\nGetting protein families from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_protein_families(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()