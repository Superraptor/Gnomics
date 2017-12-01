#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get diseases from a gene.
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
import gnomics.objects.compound
import gnomics.objects.gene

#   Other imports.
import json
import requests

#   MAIN
def main():
    gene_compound_unit_tests("675", "ENSG00000113916")

# Get drug interactions.
# http://dgidb.genome.wustl.edu/api
#
# Interaction sources can be TTD, DrugBank, etc.
# But should be an array if possible.
def get_compounds(gene, source = "dgidb", interaction_sources = None, interaction_types = None, drug_types = None, source_trust_levels = None):
    chem_id_array = []
    chem_obj_array = []
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez gene identifier" or ident["identifier_type"].lower() == "entrez gene" or ident["identifier_type"].lower() == "ncbi entrez gene identifier" or ident["identifier_type"].lower() == "ncbi entrez gene" or ident["identifier_type"].lower() == "ncbi gene id":
            if source == "dgidb":
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v2/interactions.json?genes=" + ident["identifier"]
                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if drug_types is not None:
                    ext = ext + (",".join(drug_types)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                for iden in decoded["ambiguousTerms"]:
                    for iden_sec in iden["interactions"]:
                        if iden_sec["drugChemblId"] not in chem_id_array:
                            chem_id_array.append(iden_sec["drugChemblId"])
                            temp_com = gnomics.objects.compound.Compound(identifier = iden_sec["drugChemblId"], identifier_type = "ChEMBL ID", source = "DGIdb")
                            chem_obj_array.append(temp_com)
        elif ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier" or ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl":
            if source == "dgidb":
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v2/interactions.json?genes=" + ident["identifier"]
                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if drug_types is not None:
                    ext = ext + (",".join(drug_types)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                for iden in decoded["matchedTerms"]:
                    for iden_sec in iden["interactions"]:
                        if iden_sec["drugChemblId"] not in chem_id_array:
                            chem_id_array.append(iden_sec["drugChemblId"])
                            temp_com = gnomics.objects.compound.Compound(identifier = iden_sec["drugChemblId"], identifier_type = "ChEMBL ID", source = "DGIdb")
                            chem_obj_array.append(temp_com)
    return chem_obj_array
    
#   UNIT TESTS
def gene_compound_unit_tests(entrez_gene_id, ensembl_gene_id):
    entrez_gene = gnomics.objects.gene.Gene(identifier = entrez_gene_id, identifier_type = "Entrez Gene ID", language = None, species = "Homo sapiens", source = "NCBI")
    print("Getting diseases from NCBI Entrez gene ID (%s):" % entrez_gene_id)
    for dis in get_compounds(entrez_gene):
        print("- %s" % dis)
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, species = "Homo sapiens", source = "Ensembl")
    print("\nGetting diseases from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for dis in get_compounds(ensembl_gene):
        print("- %s" % dis)
    
#   MAIN
if __name__ == "__main__": main()