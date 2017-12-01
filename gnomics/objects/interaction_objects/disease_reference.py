#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get references associated with a disease.
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
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
import re
import requests

#   MAIN
def main():
    reference_unit_tests("H00286")

# Return references.
def get_references(disease, user = None):
    ref_array = []
    for ident in disease.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg disease id":
            sorted_output = []
            for ref in gnomics.objects.disease.Disease.kegg_disease(disease)["REFERENCE"]:
                journal = ref["JOURNAL"]
                authors = ref["AUTHORS"]
                title = ref["TITLE"]
                unprocessed_ref = ref["REFERENCE"]
                processed_pmid = re.findall('\d+', unprocessed_ref)[0]
                if str(processed_pmid) not in ref_array:
                    ref_array.append(str(processed_pmid))
    return ref_array
    
#   UNIT TESTS
def reference_unit_tests(kegg_disease_id):
    kegg_disease = gnomics.objects.disease.Disease(identifier = str(kegg_disease_id), identifier_type = "KEGG DISEASE ID", source = "KEGG")
    print("\nGetting references (PMIDs) from KEGG DISEASE ID (%s):" % kegg_disease_id)
    for ref in get_references(kegg_disease):
        print("- %s" % str(ref))

#   MAIN
if __name__ == "__main__": main()