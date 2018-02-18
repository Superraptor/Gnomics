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
#   Get MMDB (Molecular Modeling Database) ID.
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

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    mmdb_unit_tests("36462")
    
# Get MMDB IDs.
def get_mmdb(com, user=None):
    mmdb_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["mmdb", "mmdb id", "mmdb identifier", "mmdbid"]):
        if iden["identifier"] not in mmdb_array:
            mmdb_array.append(iden["identifier"])
            
    if mmdb_array:
        return mmdb_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(iden["identifier"]) + "/xrefs/MMDBID/JSONP"
            
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("An unknown error was encountered while trying to reach the PubChem PUG REST server.")
            else:
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.index(")")
                    res = str_r[l_index:r_index]
                    decoded = json.loads(res)
                    for result in decoded["InformationList"]["Information"]:
                        mms = result["MMDBID"]
                        for mm in mms:
                            if mm not in mmdb_array: 
                                gnomics.objects.compound.Compound.add_identifier(com, identifier=mm, identifier_type="MMDB ID", language=None, source="PubChem")
                                mmdb_array.append(mm)
                    
                except ValueError:
                    print("Input is not in a JSONP format.")

    return mmdb_array

#   UNIT TESTS
def mmdb_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting MMDB IDs from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    mmdb_array = get_mmdb(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in mmdb_array:
        print("\t- %s" % str(com))
    
#   MAIN
if __name__ == "__main__": main()