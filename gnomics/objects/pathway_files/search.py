#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#

#
#   Search for pathway.
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
import gnomics.objects.pathway

#   Other imports.
from bioservices.kegg import KEGG
import json
import requests
import xml.etree.ElementTree as ET

#   MAIN
def main():
    basic_search_unit_tests("breast cancer", "Homo sapiens")
    
# Return search.
#
# Various parameters available here:
# http://www.wikipathways.org/index.php/Help:WikiPathways_Webservice/API
# http://webservice.wikipathways.org/findPathwaysByText?query=apoptosis
#
# RESULT PARAMS
#
#
# QUERY PARAMS
# - query
# - species
#
def search(query, source = "wikipathways", result_format = "xml", species = None, genes = None):
    if source == "wikipathways" and species is None:
        url = "http://webservice.wikipathways.org/"
        ext = "/findPathwaysByText?query=" + str(query)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        tree = ET.ElementTree(ET.fromstring(r.text))
        root = tree.getroot()
        path_array = []
        for child in root:
            temp_path_dict = {}
            for subchild in child:
                if subchild.tag == "{http://www.wikipathways.org/webservice}id":
                    temp_path_dict["identifier"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}score":
                    temp_path_dict["score"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}url":
                    temp_path_dict["url"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}name":
                    temp_path_dict["name"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}species":
                    temp_path_dict["species"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}revision":
                    temp_path_dict["revision"] = subchild.text
            temp_path = gnomics.objects.pathway.Pathway(identifier = temp_path_dict["identifier"], identifier_type = "WikiPathways ID", name = temp_path_dict["name"], taxon = temp_path_dict["species"], source = "WikiPathways")
            path_array.append(temp_path)
        return path_array
    elif source == "wikipathways" and species is not None:
        url = "http://webservice.wikipathways.org/"
        ext = "/findPathwaysByText?query=" + str(query) + "&species=" + str(species)
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        tree = ET.ElementTree(ET.fromstring(r.text))
        root = tree.getroot()
        path_array = []
        for child in root:
            temp_path_dict = {}
            for subchild in child:
                if subchild.tag == "{http://www.wikipathways.org/webservice}id":
                    temp_path_dict["identifier"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}score":
                    temp_path_dict["score"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}url":
                    temp_path_dict["url"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}name":
                    temp_path_dict["name"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}species":
                    temp_path_dict["species"] = subchild.text
                elif subchild.tag == "{http://www.wikipathways.org/webservice}revision":
                    temp_path_dict["revision"] = subchild.text
            temp_path = gnomics.objects.pathway.Pathway(identifier = temp_path_dict["identifier"], identifier_type = "WikiPathways ID", name = temp_path_dict["name"], taxon = temp_path_dict["species"], source = "WikiPathways")
            path_array.append(temp_path)
        return path_array
    elif source == "kegg" and genes is not None:
        k = KEGG()
    elif source == "kegg" and genes is None:
        k = KEGG()
        list_of_pathways = k.find("pathway", query)
        temp_path_list = list_of_pathways.split("\n")
        super_path_list = []
        for thing in temp_path_list:
            temp_split = thing.split("\t")
            if len(temp_split) != 1:
                path_id = temp_split[0].strip().split(":")[1]
                path_name = temp_split[1].strip()
                if "map" in path_id:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = path_id, identifier_type = "KEGG MAP PATHWAY ID", source = "KEGG")
                    super_path_list.append(temp_path)
                elif "ko" in path_id:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = path_id, identifier_type = "KEGG KO PATHWAY ID", source = "KEGG")
                    super_path_list.append(temp_path)
                elif "ec" in path_id:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = path_id, identifier_type = "KEGG EC PATHWAY ID", source = "KEGG")
                    super_path_list.append(temp_path)
                elif "rn" in path_id:
                    temp_path = gnomics.objects.pathway.Pathway(identifier = path_id, identifier_type = "KEGG RN PATHWAY ID", source = "KEGG")
                    super_path_list.append(temp_path)
                else:
                    print("NOT FUNCTIONAL.")
        return super_path_list
    else:
        print("The source provided is not currently available for searching.")
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query, species):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following pathway IDs:" % str(len(basic_search_results)))
    for path in basic_search_results:
        for iden in path.identifiers:
            print("- %s: %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"], iden["taxon"]))
    print("\nBeginning basic search for '%s' for the species '%s'..." % (basic_query, species))
    basic_search_results = search(basic_query, species = species)
    print("\nSearch returned %s result(s) with the following pathway IDs:" % str(len(basic_search_results)))
    for path in basic_search_results:
        for iden in path.identifiers:
            print("- %s: %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"], iden["taxon"]))
    print("\nBeginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query, source = "kegg")
    print("\nSearch returned %s result(s) with the following pathway IDs:" % str(len(basic_search_results)))
    for path in basic_search_results:
        for iden in path.identifiers:
            print("- %s: %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"], iden["taxon"]))
    
#   MAIN
if __name__ == "__main__": main()