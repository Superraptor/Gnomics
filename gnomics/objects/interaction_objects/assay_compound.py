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
#   Get compounds from assay.
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
import gnomics.objects.assay
import gnomics.objects.compound

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    aids_unit_tests("1000")

#   Get compounds.
#
#   Parameters:
#   - compound_type: This is the type of compound, which
#                    can be either active, inactive, or
#                    both (both is represented by 'all').
def get_compounds(assay, user=None, compound_type="all"):
    
    com_array = []
    ids_completed = []
    sids_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(assay.identifiers, ["pubchem aid", "pubchem", "pubchem assay id", "pubchem assay identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            if compound_type == "all":
                
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/assay/aid/" + str(iden["identifier"]) + "/sids/JSON?"
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:

                    decoded = r.json()
                    
                    for info in decoded["InformationList"]["Information"]:
                        for sid in info["SID"]:
                            if str(sid) not in sids_array:
                                sids_array.append(str(sid))
                                temp_com = gnomics.objects.compound.Compound(identifier=str(sid), identifier_type="PubChem SID", language=None, source="Pubchem")
                                com_array.append(temp_com)
                
            elif compound_type == "inactive":
                
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/assay/aid/" + str(iden["identifier"]) + "/sids/JSON?sids_type=inactive"
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:

                    decoded = r.json()
                    
                    for info in decoded["InformationList"]["Information"]:
                        for sid in info["SID"]:
                            if str(sid) not in sids_array:
                                sids_array.append(str(sid))
                                temp_com = gnomics.objects.compound.Compound(identifier=str(sid), identifier_type="PubChem SID", language=None, source="Pubchem")
                                com_array.append(temp_com)
                
            elif compound_type == "active":
                
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/assay/aid/" + str(iden["identifier"]) + "/sids/JSON?sids_type=active"
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:

                    decoded = r.json()
                    
                    for info in decoded["InformationList"]["Information"]:
                        for sid in info["SID"]:
                            if str(sid) not in sids_array:
                                sids_array.append(str(sid))
                                temp_com = gnomics.objects.compound.Compound(identifier=str(sid), identifier_type="PubChem SID", language=None, source="Pubchem")
                                com_array.append(temp_com)

    return com_array

#   UNIT TESTS
def aids_unit_tests(pubchem_aid):
    pubchem_assay = gnomics.objects.assay.Assay(identifier = str(pubchem_aid), identifier_type = "PubChem AID", source = "PubChem")
    
    print("Getting all compounds from PubChem AID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    all_compounds = get_compounds(pubchem_assay)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for res_com in all_compounds:
        for iden in res_com.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
                
    print("\nGetting active compounds from PubChem AID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    all_compounds = get_compounds(pubchem_assay, compound_type="active")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for res_com in all_compounds:
        for iden in res_com.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
                
    print("\nGetting inactive compounds from PubChem AID (%s)..." % pubchem_aid)
    start = timeit.timeit()
    all_compounds = get_compounds(pubchem_assay, compound_type="inactive")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for res_com in all_compounds:
        for iden in res_com.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()