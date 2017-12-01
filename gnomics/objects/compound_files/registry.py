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
#   Get external registry identifier.
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

#   MAIN
def main():
    registry_unit_tests("6918092", "127378063")

#   Get Registry IDs.
def get_registry_id(com):
    reg_array = []
    for ident in com.identifiers:
            if ident["identifier_type"].lower() == "registry id" or ident["identifier_type"].lower() == "registry identifier" or ident["identifier_type"].lower() == "external registry id" or ident["identifier_type"].lower() == "external registry identifier":
                reg_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem sid" or ident["identifier_type"].lower() == "pubchem substance":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/substance/sid/" + str(ident["identifier"]) + "/xrefs/RegistryID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rindex(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for result in decoded["InformationList"]["Information"]:
                regi = result["RegistryID"]
                for reg in regi:
                    if reg not in reg_array:
                        com.identifiers.append({"identifier" : reg, "identifier_type" : "Registry ID", "source" : "PubChem", "language" : None})
                        reg_array.append(reg)
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(ident["identifier"]) + "/xrefs/RegistryID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rindex(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for result in decoded["InformationList"]["Information"]:
                regi = result["RegistryID"]
                for reg in regi:
                    if reg not in reg_array:
                        com.identifiers.append({"identifier" : reg, "identifier_type" : "Registry ID", "source" : "PubChem", "language" : None})
                        reg_array.append(reg)
    return reg_array
    

#   UNIT TESTS
def registry_unit_tests(pubchem_cid, pubchem_sid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting external registry IDs from PubChem CID (%s):" % pubchem_cid)
    for acc in get_registry_id(pubchem_com):
        print("- %s" % str(acc))
    pubchem_sub = gnomics.objects.compound.Compound(identifier = str(pubchem_sid), identifier_type = "PubChem SID", source = "PubChem")
    print("\nGetting external registry IDs from PubChem SID (%s):" % pubchem_sid)
    for acc in get_registry_id(pubchem_sub):
        print("- %s" % str(acc))
    
#   MAIN
if __name__ == "__main__": main()