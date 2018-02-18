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
#   Get transcript from a variation.
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
import gnomics.objects.transcript
import gnomics.objects.variation

#   Other imports.
import json
import myvariant
import requests
import timeit

#   MAIN
def main():
    variation_transcript_unit_tests("chr7:g.140453134T>C", "RS121913364")

# Get transcript.
def get_transcript(variation):
    trans_array = []
    trans_id_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variation.identifiers, ["coding hgvs", "coding hgvs id", "coding hgvs identifier", "genomic hgvs", "genomic hgvs id", "genomic hgvs identifier", "hgvs", "hgvs id", "hgvs identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for obj in gnomics.objects.variation.Variation.hgvs(variation):
                if "dbnsfp" in obj:
                    ensembl_id = obj["dbnsfp"]["ensembl"]["transcriptid"]
                    if ensembl_id not in trans_id_array:
                        temp_trans = gnomics.objects.transcript.Transcript(identifier=ensembl_id, identifier_type="Ensembl Transcript ID", language=None, source="MyVariant")
                        trans_array.append(temp_trans)
                        trans_id_array.append(ensembl_id)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(variation.identifiers, ["reference snp id", "reference snp identifier", "rs", "rs id", "rs identifier", "rs number", "rsid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for obj in gnomics.objects.variation.Variation.hgvs(variation):
                if "dbnsfp" in obj:
                    ensembl_id = obj["dbnsfp"]["ensembl"]["transcriptid"]
                    if ensembl_id not in trans_id_array:
                        temp_trans = gnomics.objects.transcript.Transcript(identifier=ensembl_id, identifier_type="Ensembl Transcript ID", language=None, source="MyVariant")
                        trans_array.append(temp_trans)
                        trans_id_array.append(ensembl_id)
            
    return trans_array
            
#   UNIT TESTS
def variation_transcript_unit_tests(hgvs_id, rsid):
    hgvs_var = gnomics.objects.variation.Variation(identifier = hgvs_id, identifier_type = "HGVS ID", language = None, source = None)
    print("\nGetting transcript identifiers from HGVS ID (%s):" % hgvs_id)
    for trans in get_transcript(hgvs_var):
        for iden in trans.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
    dbsnp_var = gnomics.objects.variation.Variation(identifier = rsid, identifier_type = "RS Number", language = None, source = None)
    print("\nGetting transcript identifiers from RSID (%s):" % rsid)
    for trans in get_transcript(dbsnp_var):
        for iden in trans.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()