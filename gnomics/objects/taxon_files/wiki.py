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
#   Get Wikipedia, Wikidata.
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
from wikidata.client import Client
import json
import pytaxize
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    wiki_unit_tests("Homo sapiens")
    
#   Get Wikidata accession.
def get_wikidata_accession(taxon):
    wiki_array = []
    
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"] and ident["identifier"] not in wiki_array:
            wiki_array.append(ident["identifier"])
        
    if wiki_array:
        return wiki_array
        
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia", "wikipedia article"]:
            if ident["language"] == "en":
        
                base = "https://en.wikipedia.org/w/api.php"
                ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]

                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)      
                wikidata_id = decoded["query"]["pages"]["pageprops"]["wikibase_item"]
                
                if wikidata_id not in wiki_array:
                    gnomics.objects.taxon.Taxon.add_identifier(identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")

                    wiki_array.append(wikidata_id)
        
        elif ident["identifier_type"].lower() in ["scientific name", "binomial name", "binomial nomenclature", "binomen", "latin name"]:
            
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            wikidata_id = next(iter(decoded["query"]["pages"].values()))["pageprops"]["wikibase_item"]
            
            instance_of_taxon = False
            
            client = Client()
            entity = client.get(wikidata_id, load=True)
            
            for stuff in [entity.attributes]:
                for prop_id, prop_dict in stuff["claims"].items():

                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    
                    if en_prop_name.lower() == "instance of":
                        for x in prop_dict:
                            if x["mainsnak"]["datavalue"]["value"]["id"] == "Q16521":
                                instance_of_taxon = True
             
            if instance_of_taxon == True and wikidata_id not in wiki_array:
                gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                
                wiki_array.append(wikidata_id)
    
    return wiki_array
            
#   Get Wikidata object.
def get_wikidata_object(taxon):
    wikidata_obj_array = []
    for tax_obj in taxon.taxon_objects:
        if 'object_type' in tax_obj:
            if tax_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(tax_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in [get_wikidata_accession(taxon)]:
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.taxon.Taxon.add_object(taxon, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   UNIT TESTS
def wiki_unit_tests(sci_name):
    sci_taxon = gnomics.objects.taxon.Taxon(identifier=sci_name, identifier_type="Scientific Name", language="Latin", source=None)
    print("Getting Wikidata Accession from Scientific Name (%s):" % sci_name)
    for wikidata in [get_wikidata_accession(sci_taxon)]:
        print("- %s" % wikidata)
        
#   MAIN
if __name__ == "__main__": main()