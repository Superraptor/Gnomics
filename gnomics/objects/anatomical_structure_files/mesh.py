#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Get MeSH.
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
import json
import requests

#   MAIN
def main():
    mesh_unit_tests("21", "50801", "Q199507", "")

# Return MeSH.
def get_mesh(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH ID.
                            if rep["rootSource"] == "MSH":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="MeSH ID", language=None, source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH ID.
                            if rep["rootSource"] == "MSH":
                                anat_array.append(rep["ui"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["ui"], identifier_type="MeSH ID", language=None, source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "wikidata" or iden["identifier_type"].lower() == "wikidata id" or iden["identifier_type"].lower() == "wikidata identifier" or iden["identifier_type"].lower() == "wikidata accession":
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
                    if en_prop_name.lower() == "mesh id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH ID", language = None, source = "Wikidata")
                            return [x["mainsnak"]["datavalue"]["value"]]
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"].lower() == "en":
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
                    if en_prop_name.lower() == "mesh id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH ID", language = None, source = "Wikidata")
                            return [x["mainsnak"]["datavalue"]["value"]]
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
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
                    if en_prop_name.lower() == "mesh id":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH ID", language = None, source = "Wikidata")
                            return [x["mainsnak"]["datavalue"]["value"]]
            
# Get English MeSH term (MSH).
def get_mesh_term_english(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSH":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="en", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSH":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="en", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
            
# Get MeSH tree number.
def get_mesh_tree_number(anat):
    mesh_array = []
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "mesh tree number":
            mesh_array.append(ident["identifier"])
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
                    if en_prop_name.lower() == "mesh code":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")
                            mesh_array.append(x["mainsnak"]["datavalue"]["value"])
    if mesh_array:
        return mesh_array
    for ident in anat.identifiers:
        if (ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia") and ident["language"].lower() == "en":
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
                    if en_prop_name.lower() == "mesh code":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")
                            mesh_array.append(x["mainsnak"]["datavalue"]["value"])
    if mesh_array:        
        return mesh_array
    for ident in anat.identifiers:
        if ident["identifier_type"].lower() == "uberon" or ident["identifier_type"].lower() == "uberon id" or ident["identifier_type"].lower() == "uberon identifier":
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
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
                    if en_prop_name.lower() == "mesh code":
                        for x in prop_dict:
                            gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")
                            mesh_array.append(x["mainsnak"]["datavalue"]["value"])
    return mesh_array
    
# Get Czech MeSH term (MSHCZE).
def get_mesh_term_czech(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHCZE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="cs", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHCZE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="cs", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array

# Get Dutch MeSH term (MSHDUT).
def get_mesh_term_dutch(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHDUT":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="nl", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHDUT":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="nl", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Finnish MeSH term (MSHFIN).
def get_mesh_term_finnish(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHFIN":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="fi", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHFIN":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="fi", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get French MeSH term (MSHFRE).
def get_mesh_term_french(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHFRE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="fr", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHFRE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="fr", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get German MeSH term (MSHGER).
def get_mesh_term_german(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHGER":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="de", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHGER":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="de", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Italian MeSH term (MSHITA).
def get_mesh_term_italian(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHITA":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="it", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHITA":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="it", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Japanese MeSH term (MSHJPN).
def get_mesh_term_japanese(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHJPN":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="ja", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHJPN":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="ja", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Latvian MeSH term (MSHLAV).
def get_mesh_term_latvian(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHLAV":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="lv", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHLAV":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="lv", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Norwegian MeSH term (MSHNOR).
def get_mesh_term_norwegian(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHNOR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="no", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHNOR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="no", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Polish MeSH term (MSHPOL).
def get_mesh_term_polish(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHPOL":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="pl", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHPOL":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="pl", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Portuguese MeSH term (MSHPOR).
def get_mesh_term_portuguese(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHPOR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="pt", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHPOR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="pt", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Russian MeSH term (MSHRUS).
def get_mesh_term_russian(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHRUS":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="ru", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHRUS":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="ru", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Croatian MeSH term (MSHSCR).
def get_mesh_term_croatian(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSCR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="hr", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSCR":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="hr", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Spanish MeSH term (MSHSPA).
def get_mesh_term_spanish(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSPA":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="es", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSPA":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="es", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
# Get Swedish MeSH term (MSHSWE).
def get_mesh_term_swedish(anat, user = None, source = "umls"):
    for iden in anat.identifiers:
        if iden["identifier_type"].lower() == "neu id" or iden["identifier_type"].lower() == "neu identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/NEU/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSWE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="sv", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
        elif iden["identifier_type"].lower() == "uwda id" or iden["identifier_type"].lower() == "uwda identifier":
            if source == "umls":
                anat_array = []
                umls_tgt = User.umls_tgt(user)
                page_num = 0
                base = "https://uts-ws.nlm.nih.gov/rest"
                ext = "/crosswalk/current/source/UWDA/" + iden["identifier"]
                while True:
                    tick = User.umls_st(umls_tgt)
                    page_num += 1
                    query = {"ticket": tick, "pageNumber": page_num}
                    r = requests.get(base+ext, params=query)
                    r.encoding = 'utf-8'
                    items = json.loads(r.text)
                    json_data = items["result"]
                    for rep in json_data:
                        if rep["ui"] not in anat_array and rep["ui"] != "NONE":
                            # MeSH term.
                            if rep["rootSource"] == "MSHSWE":
                                anat_array.append(rep["name"])
                                gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=rep["name"], identifier_type="MeSH Term", language="sv", source="UMLS Metathesaurus")
                    if not json_data:
                        break
                return anat_array
    
#   UNIT TESTS
def mesh_unit_tests(neu_id, uwda_id, wikidata_accession, umls_api_key):
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", source = "Wikidata")
    print("\nGetting MeSH UID from Wikidata Accession (%s):" % wikidata_accession)
    for mesh in get_mesh(wikidata_anat):
        print("- " + str(mesh))
    print("\nGetting MeSH tree number from Wikidata Accession (%s):" % wikidata_accession)
    for mesh in get_mesh_tree_number(wikidata_anat):
        print("- " + str(mesh))
        
    user = User(umls_api_key = umls_api_key)
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
    print("\nGetting MeSH ID from NEU ID (%s):" % neu_id)
    for mesh in get_mesh(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting English MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_english(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Dutch MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_dutch(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Finnish MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_finnish(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting French MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_french(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting German MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_german(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Italian MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_italian(neu_anat, user = user):
        print("- " + str(mesh))
    # print("\nGetting Japanese MeSH term from NEU ID (%s):" % neu_id)
    # for mesh in get_mesh_term_japanese(neu_anat, user = user):
    #    print("- " + str(mesh))
    print("\nGetting Latvian MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_latvian(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Norwegian MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_norwegian(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Polish MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_polish(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Portuguese MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_portuguese(neu_anat, user = user):
        print("- " + str(mesh))
    # print("\nGetting Russian MeSH term from NEU ID (%s):" % neu_id)
    # for mesh in get_mesh_term_russian(neu_anat, user = user):
    #    print("- " + str(mesh))
    print("\nGetting Croatian MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_croatian(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Spanish MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_spanish(neu_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Swedish MeSH term from NEU ID (%s):" % neu_id)
    for mesh in get_mesh_term_swedish(neu_anat, user = user):
        print("- " + str(mesh))
        
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")   
    print("\nGetting MeSH ID from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting English MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_english(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Dutch MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_dutch(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Finnish MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_finnish(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting French MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_french(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting German MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_german(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Italian MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_italian(uwda_anat, user = user):
        print("- " + str(mesh))
    # print("\nGetting Japanese MeSH term from UWDA ID (%s):" % uwda_id)
    # for mesh in get_mesh_term_japanese(uwda_anat, user = user):
    #    print("- " + str(mesh))
    print("\nGetting Latvian MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_latvian(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Norwegian MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_norwegian(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Polish MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_polish(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Portuguese MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_portuguese(uwda_anat, user = user):
        print("- " + str(mesh))
    # print("\nGetting Russian MeSH term from UWDA ID (%s):" % uwda_id)
    # for mesh in get_mesh_term_russian(uwda_anat, user = user):
    #    print("- " + str(mesh))
    print("\nGetting Croatian MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_croatian(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Spanish MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_spanish(uwda_anat, user = user):
        print("- " + str(mesh))
    print("\nGetting Swedish MeSH term from UWDA ID (%s):" % uwda_id)
    for mesh in get_mesh_term_swedish(uwda_anat, user = user):
        print("- " + str(mesh))
    
#   MAIN
if __name__ == "__main__": main()