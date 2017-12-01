#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get UBERON identifiers.
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
import gnomics.objects.anatomical_structure

#   Other imports.
from urllib.parse import urlencode, quote_plus
import json
import requests

#   MAIN
def main():
    uberon_unit_tests("UBERON:0001424", "Q199507")

# Return UBERON object.
def get_uberon_obj(anat, user = None):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "uberon id" or iden["identifier_type"].lower() == "uberon identifier" or iden["identifier_type"].lower() == "uberon":
            if ":" in iden["identifier"]:
                temp_iden = iden["identifier"].replace(':', '_')
                norm_url = "http://purl.obolibrary.org/obo/" + temp_iden
                payload = {'term': norm_url}
                result_url = urlencode(payload)
                encode_payload = {'term': result_url}
                encode_result_url = urlencode(encode_payload)
                print(encode_result_url.split("%3D"))
                url = "http://www.ebi.ac.uk/ols/api/"
                ext = "ontologies/uberon/terms/" + encode_result_url.split("%3D")[1]
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj=decoded, object_type="UBERON")
                return decoded
            elif "_" in iden["identifier"]:
                print("NOT FUNCTIONAL.")
                norm_url = "http://purl.obolibrary.org/obo/" + iden["identifier"]
                payload = {'term': norm_url}
                result_url = urlencode(payload)
                encode_payload = {'term': result_url}
                encode_result_url = urlencode(encode_payload)
                url = "http://www.ebi.ac.uk/ols/api/"
                ext = "ontologies/uberon/terms/" + encode_result_url.split("%3D")[1]
                r = requests.get(url+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                gnomics.objects.anatomical_structure.AnatomicalStructure.add_object(anat, obj=decoded, object_type="UBERON")
                return decoded
            else:
                print("UBERON identifier is not in the correct format to allow for double URL encoding in the OLS.")
            
#   Get UBERON ID.
def get_uberon_id(anat):
    uberon_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier"  or ident["identifier_type"].lower() == "uberon":
            uberon_array.append(ident["identifier"])
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "uberon id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "UBERON ID", language = None, source = "Wikidata")
                            uberon_array.append(x["mainsnak"]["datavalue"]["value"])
    return uberon_array
    
    
#   UNIT TESTS
def uberon_unit_tests(uberon_id, wikidata_accession):
    uberon_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uberon_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", source = "Wikidata")
    print("\nGetting UBERON ID from Wikidata Accession (%s):" % wikidata_accession)
    for uberon in get_uberon_id(wikidata_anat):
        print("- %s" % uberon)
    
#   MAIN
if __name__ == "__main__": main()