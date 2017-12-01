#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get ConceptWiki.
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
import json
import requests

#   MAIN
def main():
    conceptwiki_unit_tests("38932552-111f-4a4e-a46a-4ed1d7bdf9d5", "187440", "CHEMBL1336", "SCHEMBL8218", "", "")

#   Get ConceptWiki object.
#
#   _format
#   _callback
#   _metadata
def get_conceptwiki_obj(com, user = None):
    for com_obj in com.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'conceptwiki object' or com_obj['object_type'].lower() == 'conceptwiki':
                return com_obj['object']
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "csid" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier":
            com_obj_array = []
            for csid in [gnomics.objects.compound.Compound.chemspider_id(com)]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.chemspider.com%2F" + csid + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                com.compound_objects.append(
                    {
                        'object': decoded["result"],
                        'object_type': "ConceptWiki Object"
                    }
                )
                com_obj_array.append(decoded["result"])
            return com_obj_array
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            com_obj_array = []
            for chembl_id in [gnomics.objects.compound.Compound.chembl_id(com)]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fchembl%2Fmolecule%2F" + chembl_id + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                com.compound_objects.append(
                    {
                        'object': decoded["result"],
                        'object_type': "ConceptWiki Object"
                    }
                )
                com_obj_array.append(decoded["result"])
            return com_obj_array
        elif ident["identifier_type"].lower() == "schembl" or ident["identifier_type"].lower() == "schembl id" or ident["identifier_type"].lower() == "schembl identifier":
            com_obj_array = []
            for schembl_id in [gnomics.objects.compound.Compound.schembl_id(com)]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Frdf.ebi.ac.uk%2Fresource%2Fsurechembl%2Fmolecule%2F" + schembl_id + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                com.compound_objects.append(
                    {
                        'object': decoded["result"],
                        'object_type': "ConceptWiki Object"
                    }
                )
                com_obj_array.append(decoded["result"])
            return com_obj_array
        elif ident["identifier_type"].lower() == "conceptwiki id" or ident["identifier_type"].lower() == "conceptwiki":
            com_obj_array = []
            for conceptwiki_id in [get_conceptwiki_id(com)]:
                base = "https://beta.openphacts.org/2.1/"
                ext = "compound?uri=http%3A%2F%2Fwww.conceptwiki.org%2Fconcept%2F" + conceptwiki_id + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                com.compound_objects.append(
                    {
                        'object': decoded["result"],
                        'object_type': "ConceptWiki Object"
                    }
                )
                com_obj_array.append(decoded["result"])
            return com_obj_array
    
#   Get ConceptWiki ID.
def get_conceptwiki_id(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "conceptwiki id" or ident["identifier_type"].lower() == "conceptwiki":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "csid" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier":
            cs_uri = "http://rdf.chemspider.com/" + ident["identifier"]
            concept_array = []
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"]:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1])
                            concept_array.append(subitem["_about"].split("/concept/")[1])
            return concept_array
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            chembl_uri = "ttp://rdf.ebi.ac.uk/resource/chembl/molecule/" + ident["identifier"]
            concept_array = []
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"]:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1])
                            concept_array.append(subitem["_about"].split("/concept/")[1])
            return concept_array
        elif ident["identifier_type"].lower() == "schembl" or ident["identifier_type"].lower() == "schembl id" or ident["identifier_type"].lower() == "schembl identifier":
            schembl_uri = "http://rdf.ebi.ac.uk/resource/surechembl/molecule/" + ident["identifier"]
            concept_array = []
            for item in get_conceptwiki_obj(com, user = user):
                for subitem in item["primaryTopic"]["exactMatch"]:
                    if "_about" in subitem:
                        if "http://www.conceptwiki.org" in subitem["_about"]:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = subitem["_about"].split("/concept/")[1], identifier_type = "ConceptWiki ID", source = "OpenPHACTS")
                            concept_array.append(subitem["_about"].split("/concept/")[1])
            return concept_array

#   UNIT TESTS
def conceptwiki_unit_tests(conceptwiki_id, chemspider_id, chembl_id, schembl_id, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    conceptwiki_com = gnomics.objects.compound.Compound(identifier = conceptwiki_id, identifier_type = "ConceptWiki ID", source = "OpenPHACTS")
    chemspider_com = gnomics.objects.compound.Compound(identifier = chemspider_id, identifier_type = "ChemSpider ID", source = "OpenPHACTS")
    print("Getting ConceptWiki IDs from ChemSpider ID (%s):" % chemspider_id)
    for com in get_conceptwiki_id(chemspider_com, user = user):
        print("- " + str(com))
    chembl_com = gnomics.objects.compound.Compound(identifier = chembl_id, identifier_type = "ChEMBL ID", source = "OpenPHACTS")
    print("\nGetting ConceptWiki IDs from ChEMBL ID (%s):" % chembl_id)
    for com in get_conceptwiki_id(chembl_com, user = user):
        print("- " + str(com))
    schembl_com = gnomics.objects.compound.Compound(identifier = schembl_id, identifier_type = "SCHEMBL ID", source = "OpenPHACTS")
    print("\nGetting ConceptWiki IDs from SCHEMBL ID (%s):" % schembl_id)
    for com in get_conceptwiki_id(schembl_com, user = user):
        print("- " + str(com))

#   MAIN
if __name__ == "__main__": main()