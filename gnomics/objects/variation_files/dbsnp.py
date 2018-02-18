#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       MYVARIANT
#           http://myvariant-py.readthedocs.io/en/latest/
#

#
#   Get information from dbSNP.
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
import gnomics.objects.variation

#   Other imports.
import myvariant
import requests

#   MAIN
def main():
    dbsnp_unit_tests("rs58991260")
    
# Return dbSNP object.
def get_dbsnp_obj(variant):
    obj_array = []
    
    for obj in variant.variation_objects:
        if obj["object_type"] in ["reference snp id", "reference snp identifier", "reference snp object", "rs", "rs id", "rs identifier", "rs object", "rs number", "rsid"]:
            obj_array.append(obj["object"])
            
    if obj_array:
        return obj_array
    
    for rs_id in get_rs_number(variant):
        mv = myvariant.MyVariantInfo()
        query_string = "dbsnp.rsid:" + rs_id
        result = mv.query(query_string, fields='dbsnp')
        gnomics.objects.variation.Variation.add_object(variant, obj = result, object_type = "dbSNP")
        obj_array.append(result)
        
    return obj_array

# Returns RS Number.
def get_rs_number(variant):
    rs_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variant.identifiers, ["reference snp id", "reference snp identifier", "rs", "rs id", "rs identifier", "rs number", "rsid"]):
        if iden["identifier"] not in rs_array:
            rs_array.append(iden["identifier"])
    return rs_array
        
#   UNIT TESTS
def dbsnp_unit_tests(rsid):
    variant = gnomics.objects.variation.Variation(identifier = rsid, identifier_type = "RS Number", language = None, source = None)

#   MAIN
if __name__ == "__main__": main()