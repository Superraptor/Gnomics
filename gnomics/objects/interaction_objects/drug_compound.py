#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get compounds from drug.
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
import gnomics.objects.drug

#   Other imports.
import json
import pubchempy as pubchem
import requests
import timeit

#   MAIN
def main():
    drug_compound_unit_tests("DB00398", "", "")
     
#   Get compounds.
def get_compounds(drug, user=None):
    com_array = []
    
    for ident in drug.identifiers:
        if (ident["identifier_type"].lower() in ["drugbank accession", "drugbank", "drugbank id", "drugbank identifier"]) and user is not None:
            
            base = "https://beta.openphacts.org/2.1/"
            ext = "compound?uri=http%3A%2F%2Fbio2rdf.org%2Fdrugbank%3A" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            for subitem in decoded["result"]["primaryTopic"]["exactMatch"]:
                if "_about" in subitem:
                    if "http://www.conceptwiki.org" in subitem["_about"]:
                        temp_com = gnomics.objects.compound.Compound(identifier = subitem["_about"].split("/concept/")[1], identifier_type = "ConceptWiki ID", source = "OpenPHACTS")
                        com_array.append(temp_com)
                    elif "http://rdf.chemspider.com" in subitem["_about"]:
                        temp_com = gnomics.objects.compound.Compound(identifier = subitem["_about"].split("http://rdf.chemspider.com/")[1], identifier_type = "ChemSpider ID", source = "OpenPHACTS")
                        com_array.append(temp_com)
                    elif "http://rdf.ebi.ac.uk/resource/chembl" in subitem["_about"]:
                        temp_com = gnomics.objects.compound.Compound(identifier = subitem["_about"].split("http://rdf.ebi.ac.uk/resource/chembl/molecule/")[1], identifier_type = "ChEMBL ID", source = "OpenPHACTS")
                        com_array.append(temp_com)
                    elif "http://rdf.ebi.ac.uk/resource/surechembl" in subitem["_about"]:
                        temp_com = gnomics.objects.compound.Compound(identifier = subitem["_about"].split("http://rdf.ebi.ac.uk/resource/surechembl/molecule/")[1], identifier_type = "SCHEMBL ID", source = "OpenPHACTS")
                        com_array.append(temp_com)
            
            return com_array
       
    return com_array
    
#   UNIT TESTS
def drug_compound_unit_tests(drugbank_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    
    drugbank_drug = gnomics.objects.drug.Drug(identifier = drugbank_id, identifier_type = "DrugBank ID", source = "OpenPHACTS")
    start = timeit.timeit()
    all_coms = get_compounds(drugbank_drug, user = user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nGetting compound identifiers from DrugBank ID (%s):" % drugbank_id)
    for com in all_coms:
        for iden in com.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()