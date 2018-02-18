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
#   Perform wiki-based operations.
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

#   Other imports.
import json
import requests

#   MAIN
def main():
    wiki_unit_tests()

#   Perform crosswalking operation.
def wikidata_property_check(wikidata_object, wikidata_property_name, wikidata_property_language = "en"):
    
    found_array = []
    
    for prop_id, prop_dict in wikidata_object["claims"].items():
        base = "https://www.wikidata.org/w/api.php"
        ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = json.loads(r.text)
            en_prop_name = decoded["entities"][prop_id]["labels"][wikidata_property_language]["value"]
            if en_prop_name.lower() == wikidata_property_name.lower():
                for x in prop_dict:
                    found_array.append(x["mainsnak"]["datavalue"]["value"])
            
    return found_array
    
#   UNIT TESTS
def wiki_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()