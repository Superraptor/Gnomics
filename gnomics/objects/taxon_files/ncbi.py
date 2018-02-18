#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYTAXIZE
#           http://pytaxize.readthedocs.io/en/latest/
#

#
#   Get NCBI Taxonomy.
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
import gnomics.objects.taxon

#   Other imports.
import json
import pytaxize
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    ncbi_unit_tests("1045608", "Q15978631")
    
#   Get NCBI Taxonomy identifiers.
def get_ncbi_taxonomy_id(taxon):
    ncbi_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["ncbi", "ncbi taxid", "ncbi taxon", "ncbi taxon id", "ncbi taxon identifier", "ncbi taxonomy", "ncbi taxonomy id", "ncbi taxonomy identifier", "ncbitaxon", "ncbitaxon id", "ncbitaxon identifier"]:
            ncbi_array.append(ident["identifier"])
            
    if ncbi_array:
        return ncbi_array
    
    ids_completed = []
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["eol", "eol id", "eol identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            for tax_obj in gnomics.objects.taxon.Taxon.eol_page(taxon):
                for iden2 in tax_obj["taxonConcepts"]:
                    if iden2["sourceIdentifier"].isdigit() and iden2["nameAccordingTo"] == "NCBI Taxonomy":
                        if iden2["sourceIdentifier"] not in ncbi_array:
                            gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier=iden2["sourceIdentifier"], identifier_type="NCBI Taxonomy ID", language=None, source="EOL")
                            ncbi_array.append(iden2["sourceIdentifier"])
                        
        elif ident["identifier_type"].lower() in ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"] and ident["identifier"] not in ids_completed:
            ids_completed.append(ident["identifier"])
            
            for stuff in gnomics.objects.taxon.Taxon.wikidata(taxon):
                
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]

                    if en_prop_name.lower() == "ncbi taxonomy id":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"] not in ncbi_array:
                                gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NCBI Taxonomy ID", language = None, source = "Wikidata")
                                ncbi_array.append(x["mainsnak"]["datavalue"]["value"])
    return ncbi_array

#   UNIT TESTS
def ncbi_unit_tests(eol_id, wikidata_accession):
    eol_taxon = gnomics.objects.taxon.Taxon(identifier=eol_id, identifier_type="EOL ID", language=None, source="EOL")
    print("Getting NCBI Taxonomy IDs from EOL ID (%s):" % eol_id)
    for ncbi_id in get_ncbi_taxonomy_id(eol_taxon):
        print("- %s" % ncbi_id)
        
    wikidata_taxon = gnomics.objects.taxon.Taxon(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
    print("\nGetting NCBI Taxonomy IDs from Wikidata Accession (%s):" % wikidata_accession)
    for ncbi_id in get_ncbi_taxonomy_id(wikidata_taxon):
        print("- " + str(ncbi_id))
        
#   MAIN
if __name__ == "__main__": main()