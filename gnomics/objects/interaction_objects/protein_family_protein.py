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
import gnomics.objects.protein_family

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_family_protein_unit_tests("PTHR15573")
    
#   Get proteins in a protein family.
def get_proteins(prot_fam):
    prot_id_array = []
    prot_obj_array = []
    for ident in prot_fam.identifiers:
        if ident["identifier_type"].lower() == "panther id" or ident["identifier_type"].lower() == "panther identifier" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl family id" or ident["identifier_type"].lower() == "ensembl family identifier":
            import requests, sys
            server = "https://rest.ensembl.org"
            ext = "/family/id/" + str(ident["identifier"]) + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for x in decoded["MEMBERS"]["UNIPROT_proteins"]:
                if x["protein_stable_id"] not in prot_id_array:
                    temp_prot = gnomics.objects.protein.Protein(identifier = x["protein_stable_id"], identifier_type = "UniProt Accession", source = "Ensembl")
                    prot_id_array.append(x["protein_stable_id"])
                    prot_obj_array.append(temp_prot)
    return prot_obj_array
    
#   UNIT TESTS
def protein_family_protein_unit_tests(ensembl_family_id):
    ensembl_prot_fam = gnomics.objects.protein_family.ProteinFamily(identifier = ensembl_family_id, language = None, identifier_type = "Ensembl Family ID", source = "Ensembl")
    print("Getting proteins from Panther/Ensembl protein family (%s):" % ensembl_family_id)
    for obj in get_proteins(ensembl_prot_fam):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()