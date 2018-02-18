#!/usr/bin/env python

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
#   Get BSID.
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
import gnomics.objects.pathway

#   Other imports.

#   MAIN
def main():
    bsid_unit_tests()
    
#   Get BSID.
def get_bsid(pathway):
    bsid_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(pathway.identifiers, ["bsid"]):
        if iden["identifier"] not in bsid_array:
            bsid_array.append(iden["identifier"])
    
    if bsid_array:
        return bsid_array
    
    for ident in pathway.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg ko pathway", "kegg ko pathway id", "kegg ko pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_ko_pathway(pathway):
                    if "DBLINKS" in temp:
                        if "BSID" in temp["DBLINKS"]:
                            for temp_bsid in temp["DBLINKS"]["BSID"].split(" "):
                                if temp_bsid not in bsid_array:
                                    gnomics.objects.pathway.Pathway.add_identifier(path, identifier=temp_bsid, identifier_type="BSID", source="KEGG", language=None)
                                    bsid_array.append(temp_bsid)

            elif ident["identifier_type"].lower() in ["kegg map pathway", "kegg map pathway id", "kegg map pathway identifier"]:
                for temp in gnomics.objects.pathway.Pathway.kegg_map_pathway(pathway):
                    if "DBLINKS" in temp:
                        if "BSID" in temp["DBLINKS"]:
                            for temp_bsid in temp["DBLINKS"]["BSID"].split(" "):
                                if temp_bsid not in bsid_array:
                                    gnomics.objects.pathway.Pathway.add_identifier(path, identifier=temp_bsid, identifier_type="BSID", source="KEGG", language=None)
                                    bsid_array.append(temp_bsid)
    
    return bsid_array

#   UNIT TESTS
def bsid_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()