#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get tissues from protein.
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
import gnomics.objects.protein
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

#   MAIN
def main():
    protein_tissue_unit_tests("P55795", "", "")
     
#   Get tissues.
#
#   Parameters:
#   - evidence
#   - quality
#   - _page
#   - _pageSize
#   - _orderBy
#   - _format
#   - _callback
#   - _metadata
def get_tissues(protein, user = None):
    for ident in protein.identifiers:
        if ident["identifier_type"].lower() == "uniprot acc" or ident["identifier_type"].lower() == "uniprot accession" or ident["identifier_type"].lower() == "uniprot uri":
            base = "https://beta.openphacts.org/2.1/"
            ext = "tissue/byProtein?uri=http%3A%2F%2Fpurl.uniprot.org%2Funiprot%2F" + ident["identifier"] + "&app_id=" + user.openphacts_app_id + "&app_key=" + user.openphacts_app_key + "&_format=json"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            tiss_array = []
            for item in decoded["result"]["items"]:
                temp_tiss = gnomics.objects.tissue.Tissue(identifier = item["tissue"]["_about"].split("caloha.obo#")[1], identifier_type = "CALOHA ID", source = "OpenPHACTS", name = item["tissue"]["label"])
                tiss_array.append(temp_tiss)
            return tiss_array
        
#   Get tissue expression.
def get_tissue_expression(protein):
    tiss_array = []
    tiss_dict = {}
    for ident in protein.identifiers:
        if ident["identifier_type"].lower() == "uniprot acc" or ident["identifier_type"].lower() == "uniprot accession" or ident["identifier_type"].lower() == "uniprot uri":
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "ENSEMBL_ID",
                "format": "tab",
                "query": ident["identifier"],
            }
            data = urllib.parse.urlencode(params)
            data = data.encode("utf-8")
            request = urllib.request.Request(url, data)
            contact = ""
            request.add_header("User-Agent", "Python %s" % contact)
            response = urllib.request.urlopen(request)
            page = response.read(200000).decode("utf-8")
            newline_sp = page.split("\n")
            id_from = newline_sp[0].split("\t")[0].strip()
            id_to = newline_sp[0].split("\t")[1].strip()
            orig_id = newline_sp[1].split("\t")[0].strip()
            new_id = newline_sp[1].split("\t")[1].strip()
            server = "https://www.proteinatlas.org/"
            ext = new_id + ".xml"
            r = requests.get(server+ext)
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            tree = ET.ElementTree(ET.fromstring(r.text))
            root = tree.getroot()
            for child in root:
                for subchild in child:
                    if subchild.tag == "tissueExpression":
                        exp_source = subchild.attrib["source"]
                        exp_tech = subchild.attrib["technology"]
                        exp_assay_type = subchild.attrib["assayType"]
                        for infrachild in subchild:
                            if infrachild.tag == "data":
                                tissue_name = None
                                level_type = None
                                level_text = None
                                tissue_cells = []
                                for subinfrachild in infrachild:
                                    if subinfrachild.tag == "tissue":
                                        tissue_name = subinfrachild.text
                                    elif subinfrachild.tag == "level":
                                        level_type = subinfrachild.attrib["type"]
                                        level_text = subinfrachild.text
                                    elif subinfrachild.tag == "tissueCell":
                                        cell_type_name = None
                                        cell_type_level_type = None
                                        cell_type_level_text = None
                                        for infrainfrachild in subinfrachild:
                                            if infrainfrachild.tag == "cellType":
                                                cell_type_name = infrainfrachild.text
                                            elif infrainfrachild.tag == "level":
                                                cell_type_level_type = infrainfrachild.attrib["type"]
                                                cell_type_level_text = infrainfrachild.text
                                        if cell_type_name is not None:
                                            tissue_cells.append({
                                                'cell_type': cell_type_name,
                                                'type': cell_type_level_type,
                                                'level': cell_type_level_text
                                            })
                                if tissue_name is not None:
                                    temp_tissue = gnomics.objects.tissue.Tissue(identifier = tissue_name, identifier_type = "The Human Protein Atlas Accession", source = "The Human Protein Atlas")
                                    tiss_dict[tissue_name] = {
                                        'method': "Tissue Expression",
                                        'tissue': temp_tissue,
                                        'type': level_type,
                                        'level': level_text,
                                        'source': exp_source,
                                        'technology': exp_tech,
                                        'assay_type': exp_assay_type,
                                        'cells': tissue_cells
                                    }
    return tiss_dict
    
#   UNIT TESTS
def protein_tissue_unit_tests(uniprot_acc, openphacts_app_id, openphacts_app_key):
    user = User(openphacts_app_id = openphacts_app_id, openphacts_app_key = openphacts_app_key)
    uniprot_prot = gnomics.objects.protein.Protein(identifier = uniprot_acc, identifier_type = "UniProt Accession", source = "OpenPHACTS")
    print("\nGetting tissue identifiers from UniProt Accession (%s):" % uniprot_acc)
    for tiss in get_tissues(uniprot_prot, user = user):
        for iden in tiss.identifiers:
            print("- %s (%s) [%s]" % (iden["name"], str(iden["identifier"]), iden["identifier_type"]))
    print("\nGetting tissue expression from UniProt Accession (%s):" % uniprot_acc)
    for key, val in get_tissue_expression(uniprot_prot).items():
        print("- %s" % key)
        print("  - method: %s" % val["method"])
        print("  - type: %s" % val["type"])
        print("  - level: %s" % val["level"])
        print("  - source: %s" % val["source"])
        print("  - technology: %s" % val["technology"])
        print("  - assay type: %s" % val["assay_type"])

#   MAIN
if __name__ == "__main__": main()