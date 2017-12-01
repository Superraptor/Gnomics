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
#   Get references from protein.
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
import gnomics.objects.reference

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_reference_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get references.
def get_references(prot):
    ref_id_array = []
    ref_obj_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                references = x["reference"]
                for ref in references:
                    if "PubMed" in ref:
                        pmid = ref["PubMed"]
                        temp_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PubMed ID", name = ref["title"], source = "UniProt")
                        if "DOI" in ref:
                            doi = ref["DOI"]
                            gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = doi, identifier_type = "DOI", source = "UniProt")
                            ref_id_array.append(doi)
                        ref_obj_array.append(temp_ref)
                    elif "title" in ref:
                        title = ref["title"]
                        temp_ref = gnomics.objects.reference.Reference(identifier = title, identifier_type = "Title", name = title, source = "UniProt")
                        ref_obj_array.append(temp_ref)
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            for x in gnomics.objects.protein.Protein.uniprot(prot):
                references = x["reference"]
                for ref in references:
                    if "PubMed" in ref:
                        pmid = ref["PubMed"]
                        temp_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PubMed ID", name = ref["title"], source = "UniProt")
                        if "DOI" in ref:
                            doi = ref["DOI"]
                            gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = doi, identifier_type = "DOI", source = "UniProt")
                            ref_id_array.append(doi)
                        ref_obj_array.append(temp_ref)
                    elif "title" in ref:
                        title = ref["title"]
                        temp_ref = gnomics.objects.reference.Reference(identifier = title, identifier_type = "Title", name = title, source = "UniProt")
                        ref_obj_array.append(temp_ref)
    return ref_obj_array
    
#   UNIT TESTS
def protein_reference_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting references from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_references(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting references from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_references(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()