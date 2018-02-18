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
#   Get HGVS information.
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
    hgvs_unit_tests("chr9:g.107620835G>A")
    
# Return HGVS object.
def get_hgvs_obj(variant):
    obj_array = []

    for obj in variant.variation_objects:
        if obj["object_type"] in ["hgvs", "hgvs id", "hgvs identifier", "hgvs object"]:
            obj_array.append(obj["object"])
            
    if obj_array:
        return obj_array
    
    for hgvs in get_hgvs_id(variant):
        mv = myvariant.MyVariantInfo()
        result = mv.getvariant(hgvs)
        gnomics.objects.variation.Variation.add_object(variant, obj = result, object_type = "HGVS")
        obj_array.append(result)
        
    return obj_array

# Returns HGVS-based variant ID.
def get_hgvs_id(variant):
    hgvs_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variant.identifiers, ["coding hgvs", "coding hgvs id", "coding hgvs identifier", "genomic hgvs", "genomic hgvs id", "genomic hgvs identifier", "hgvs", "hgvs id", "hgvs identifier"]):
        if iden["identifier"] not in hgvs_array:
            hgvs_array.append(iden["identifier"])
            
    if hgvs_array:
        return hgvs_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variant.identifiers, ["reference snp id", "reference snp identifier", "rs", "rs id", "rs identifier", "rs number", "rsid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for obj in gnomics.objects.variation.Variation.dbsnp(variant):
                for hit in obj["hits"]:
                    hgvs_id = hit["_id"]
                    if hgvs_id not in hgvs_array:
                        gnomics.objects.variation.Variation.add_identifier(variant, identifier=hgvs_id, identifier_type="HGVS ID", language=None, source="MyVariant")
                        hgvs_array.append(hgvs_id)
    
    return hgvs_array

# Returns coding HGVS-based variant ID.
def get_coding_hgvs_id(variant):
    hgvs_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variant.identifiers, ["coding hgvs", "coding hgvs id", "coding hgvs identifier"]):
        if iden["identifier"] not in hgvs_array:
            hgvs_array.append(iden["identifier"])
    return hgvs_array

# Returns genomic HGVS-based variant ID.
def get_genomic_hgvs_id(variant):
    hgvs_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variant.identifiers, ["genomic hgvs", "genomic hgvs id", "genomic hgvs identifier"]):
        if iden["identifier"] not in hgvs_array:
            hgvs_array.append(iden["identifier"])
    return hgvs_array
        
#   UNIT TESTS
def hgvs_unit_tests(hgvsid):
    variant = gnomics.objects.variation.Variation(identifier = hgvsid, identifier_type = "HGVS ID", language = None, source = None)

#   MAIN
if __name__ == "__main__": main()