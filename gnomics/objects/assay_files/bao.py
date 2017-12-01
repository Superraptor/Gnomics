#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get BioAssay Ontology (BAO).
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

#   Other imports.
from chembl_webresource_client.new_client import new_client
import json
import requests

#   MAIN
def main():
    bao_unit_tests("29", "BAO_0000219", "", "")
    
#   Get BAO object.
def get_bao_obj(assay, user):
    print("NOT FUNCTIONAL")
    
#   Get BAO ID.
def get_bao_id(assay):
    bao_array = []
    for ident in assay.identifiers:
        if ident["identifier_type"].lower() == "bao id" or ident["identifier_type"].lower() == "bao" or ident["identifier_type"].lower() == "bao identifier":
            bao_array.append(ident["identifier"])
    return bao_array

#   Get list of assays in the given BAO class.
def get_bao_class_assays(assay, user = None, count_only = True):
    
    # dataset
    #   chembl, opddr, opddr-pubchem (or none for all)
    # organism_url
    #   ex: http://identifiers.org/taxonomy/9606
    # target_conf_score
    #   0-9
    # target_rel_type
    #   U, D, H, M, N, S
    # _format
    #   json, tsv, ttl, xml, rdf, rdfjson, html
    # _callback
    #   [string]
    # _metadata
    #   execution, site, formats, views, all
    if count_only:
        assay_count_dict = {}
        for bao in get_bao_id(assay):
            base = " https://beta.openphacts.org/2.1/"
            ext = "assay/members/count?uri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23" + bao + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            assay_count_dict[bao] = decoded["result"]["primaryTopic"]["memberCount"]
        return assay_count_dict
    
    # dataset
    # organism_uri
    # target_conf_score
    # target_rel_type
    # _page
    # _pageSize
    #   default: 10
    # _orderBy
    # _format
    # _callback
    # _metadata
    else:
        assay_count_dict = {}
        for bao in get_bao_id(assay):
            base = " https://beta.openphacts.org/2.1/"
            ext = "assay/members/pages?uri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23" + bao + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            temp_array = []
            for item in decoded["result"]["items"]:
                temp_assay = gnomics.objects.assay.Assay(identifier = item["_about"].split("bioassay#")[1], identifier_type = "OIDD Bioassay ID", source = "OpenPHACTS")
                gnomics.objects.assay.Assay.add_identifier(temp_assay, identifier = item["exactMatch"]["_about"].split("AID")[1], name = item["exactMatch"]["title"], identifier_type = "PubChem AID", source = "OpenPHACTS")
                temp_array.append(temp_assay)
            assay_count_dict[bao] = temp_array
        return assay_count_dict
    
#   UNIT TESTS
def bao_unit_tests(bioassay_id, bao_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    bio_assay = gnomics.objects.assay.Assay(identifier = bioassay_id, identifier_type = "OIDD Bioassay ID", source = "OIDD")
    bao_assay = gnomics.objects.assay.Assay(identifier = bao_id, identifier_type = "BAO ID", source = "OpenPHACTS")
    print("\nGetting assay count from OIDD Bioassay ID (%s):" % bioassay_id)
    for iden, val in get_bao_class_assays(bao_assay, user = user, count_only = True).items():
        print("- %s" % val)
    print("\nGetting assays from OIDD Bioassay ID (%s):" % bioassay_id)
    for iden, val in get_bao_class_assays(bao_assay, user = user, count_only = False).items():
        for x in val:
            for ident in x.identifiers:
                print("- %s (%s)" % (ident["identifier"], ident["identifier_type"]))  

#   MAIN
if __name__ == "__main__": main()