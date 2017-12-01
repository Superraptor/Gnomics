#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Search for assays.
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
import gnomics.objects.assay
import gnomics.objects.compound

#   Other imports.
from chembl_webresource_client.new_client import new_client
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    search_unit_tests("fold change")
    
# Returns ChEMBL assay.
def search(query, source="chembl", assay_type_description=None, tissue_chembl_id=None, src_id=None, assay_organism=None, relationship_type=None, description=None, assay_chembl_id=None, assay_type=None, confidence_description=None, confidence_score=None, assay_tissue=None, target_chembl_id=None, relationship_description=None, assay_strain=None, src_assay_id=None, assay_tax_id=None, assay_cell_type=None, document_chembl_id=None, assay_category=None, assay_subcellular_fraction=None, cell_chembl_id=None, score=None, assay_test_type=None, bao_format=None):
    result_array = []
    assay_id_array = []
    if source == "chembl" or source == "all":
        assay = new_client.assay
        res = assay.search(query)
        for res_assay in res:
            temp_assay = gnomics.objects.assay.Assay(identifier=res_assay["assay_chembl_id"], identifier_type="ChEMBL ID", language=None, source="ChEMBL", taxon=res_assay["assay_organism"], name=res_assay["description"])
            if "bao_format" in res_assay:
                gnomics.objects.assay.Assay.add_identifier(temp_assay, identifier=res_assay["bao_format"], identifier_type="BAO ID", language=None, source="ChEMBL", taxon=res_assay["assay_organism"], name=res_assay["description"])
                assay_id_array.append(res_assay["bao_format"])
            result_array.append(temp_assay)
            assay_id_array.append(res_assay["assay_chembl_id"])
        return result_array
    if source == "ebi" or source == "all":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        # See here:
        # https://www.ebi.ac.uk/ols/ontologies
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
                # Taxon agnostic.
                if "BAO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in assay_id_array:
                        assay_temp = gnomics.objects.assay.Assay(identifier = new_id, identifier_type = "BAO ID", source = "Ontology Lookup Service", name = doc["label"])
                        result_array.append(assay_temp)
                        assay_id_array.append(new_id)
    return result_array

#   UNIT TESTS
def search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for assay in basic_search_results:
        for iden in assay.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()