#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get tissues from taxon.
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
import gnomics.objects.taxon
import gnomics.objects.tissue

#   Other imports.
import json
import requests

#   MAIN
def main():
    taxon_tissue_unit_tests("Homo sapiens")
     
#   Get tissues.
def get_tissues(taxon):
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "scientific name" or ident["identifier_type"].lower() == "binomial name":
            server = "https://rest.ensembl.org"
            ext = "/eqtl/tissue/" + ident["identifier"].lower().replace(" ", "_") + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            tiss_array = []
            for key, val in decoded.items():
                temp_tiss = gnomics.objects.tissue.Tissue(identifier = key, identifier_type = "Ensembl Accession", source = "Ensembl", language = "en")
                tiss_array.append(temp_tiss)
            return tiss_array
    
#   UNIT TESTS
def taxon_tissue_unit_tests(sci_name):
    sci_taxon = gnomics.objects.taxon.Taxon(identifier = sci_name, identifier_type = "Scientific Name", language = "la", source = "Ensembl")
    print("\nGetting tissue identifiers from taxon scientific name (%s):" % sci_name)
    for tiss in get_tissues(sci_taxon):
        for iden in tiss.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()