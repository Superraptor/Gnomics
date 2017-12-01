#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYTAXIZE
#           http://pytaxize.readthedocs.io/en/latest/
#       WIKIDATA
#           https://pypi.python.org/pypi/Wikidata
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
import gnomics.objects.taxon

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   Other imports.
from wikidata.client import Client
import pytaxize

#   MAIN
def main():
    wiki_unit_tests("Homo sapiens")
    
#   Get Wikidata accession.
def get_wikidata_accession(taxon):
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "wikidata accession" or ident["identifier_type"].lower() == "wikidata":
            return ident["identifier"]
    for ident in taxon.identifiers:
        if ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia":
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)      
            wikidata_id = decoded["query"]["pages"]["pageprops"]["wikibase_item"]
            gnomics.objects.taxon.Taxon.add_identifier(identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
            return wikidata_id
        elif ident["identifier_type"].lower() == "scientific name" or ident["identifier_type"].lower() == "binomial name" or ident["identifier_type"].lower() == "binomial nomenclature" or ident["identifier_type"].lower() == "binomen" or ident["identifier_type"].lower() == "latin name":
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
                            # This is the ID for taxon in Wikidata, see: https://www.wikidata.org/wiki/Q16521
                            if x["mainsnak"]["datavalue"]["value"]["id"] == "Q16521":
                                instance_of_taxon = True
            if instance_of_taxon == True:
                gnomics.objects.taxon.Taxon.add_identifier(taxon, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                return wikidata_id
            
#   Get Wikidata object.
def get_wikidata_object(taxon):
    wikidata_obj_array = []
    for tax_obj in taxon.taxon_objects:
        if 'object_type' in tax_obj:
            if tax_obj['object_type'].lower() == 'wikidata object' or tax_obj['object_type'].lower() == 'wikidata':
                wikidata_obj_array.append(assay_obj['object'])
    if wikidata_obj_array:
        return wikidata_obj_array
    for wikidata_id in [get_wikidata_accession(taxon)]:
        client = Client()
        entity = client.get(wikidata_id, load=True)
        taxon.taxon_objects.append({
            'object': entity.attributes,
            'object_type': "Wikidata Object"
        })
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