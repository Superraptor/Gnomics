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
#   Get UniProt.
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
import gnomics.objects.compound

#   Other imports.
import json
import pubchempy as pubchem
import requests
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

#   MAIN
def main():
    uniprot_unit_tests("", "P13368", "INSR_HUMAN")

#   Get UniProt object.
def get_uniprot_obj(prot):
    prot_obj_array = []
    
    for prot_obj in prot.protein_objects:
        if 'object_type' in prot_obj:
            if prot_obj['object_type'].lower() in ['uniprot object', 'uniprot']:
                prot_obj_array.append(prot_obj['object'])
    
    if prot_obj_array:
        return prot_obj_array
    
    for uniprot_id in get_uniprot_kb_ac(prot):
        
        # Download XML
        base = "http://www.uniprot.org/uniprot/"
        ext = uniprot_id + ".xml"

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        
        tree = ET.ElementTree(ET.fromstring(r.text))
        
        # Parse XML into dictionary
        xml_result_obj = {}
        
        root = tree.getroot()
        
        for child in root:
            for subchild in child:
                if subchild.tag == "{http://uniprot.org/uniprot}sequence":
                    xml_result_obj["sequence"] = subchild.text.replace("\n", "")
                    xml_result_obj["sequence_length"] = subchild.attrib["length"]
                    xml_result_obj["sequence_mass"] = subchild.attrib["mass"]
                    xml_result_obj["sequence_checksum"] = subchild.attrib["checksum"]
                    xml_result_obj["sequence_modified"] = subchild.attrib["modified"]
                    xml_result_obj["sequence_version"] = subchild.attrib["version"]
                elif subchild.tag == "{http://uniprot.org/uniprot}keyword":
                    if "keyword" in xml_result_obj:
                        xml_result_obj["keyword"].append({
                            subchild.attrib["id"]: subchild.text
                        })
                    else:
                        xml_result_obj["keyword"] = [{
                            subchild.attrib["id"]: subchild.text
                        }]
                elif subchild.tag == "{http://uniprot.org/uniprot}accession":
                    if "accession" in xml_result_obj:
                        xml_result_obj["accession"].append(subchild.text)
                    else:
                        xml_result_obj["accession"] = [subchild.text]
                elif subchild.tag == "{http://uniprot.org/uniprot}name":
                    if "name" in xml_result_obj:
                        xml_result_obj["name"].append(subchild.text)
                    else:
                        xml_result_obj["name"] = [subchild.text]
                elif subchild.tag == "{http://uniprot.org/uniprot}dbReference" and (not subchild):
                    if "db_reference" in xml_result_obj:
                            xml_result_obj["db_reference"].append({
                                'id_type': subchild.attrib["type"],
                                'identifier': subchild.attrib["id"]
                            })
                    else:
                        xml_result_obj["db_reference"] = [{
                            'id_type': subchild.attrib["type"],
                            'identifier': subchild.attrib["id"]
                        }]
                elif subchild.tag == "{http://uniprot.org/uniprot}evidence" and (not subchild):
                    if "evidence" in xml_result_obj:
                            xml_result_obj["evidence"].append({
                                'key': subchild.attrib["key"],
                                'type': subchild.attrib["type"]
                            })
                    else:
                        xml_result_obj["evidence"] = [{
                            'key': subchild.attrib["key"],
                            'type': subchild.attrib["type"]
                        }]
                elif subchild.tag == "{http://uniprot.org/uniprot}feature":
                    feat_dict = {}
                    feat_dict["feature_type"] = subchild.attrib["type"]
                    if "description" in subchild.attrib:
                        feat_dict["feature_description"] = subchild.attrib["description"]
                    if "evidence" in subchild.attrib:
                        feat_dict["feature_evidence"] = subchild.attrib["evidence"]
                    elif "id" in subchild.attrib:
                        feat_dict["feature_id"] = subchild.attrib["id"]
                    for infrachild in subchild:
                        if infrachild.tag == "original":
                            feat_dict["original"] = infrachild.text
                        elif infrachild.tag == "variation":
                            feat_dict["variation"] = infrachild.text
                        for subinfrachild in infrachild:
                            if infrachild.tag == "location" and subinfrachild.tag == "position":
                                if "position" in subinfrachild.attrib:
                                    feat_dict["position"] = subinfrachild.attrib["position"]
                                elif "begin" in subinfrachild.attrib:
                                    feat_dict["begin"] = subinfrachild.attrib["begin"]
                                elif "end" in subinfrachild.attrib:
                                    feat_dict["end"] = subinfrachild.attrib["end"]
                    if "feature" in xml_result_obj:
                        xml_result_obj["feature"].append(feat_dict)
                    else:
                        xml_result_obj["feature"] = [feat_dict]
                elif subchild.tag == "{http://uniprot.org/uniprot}reference":
                    ref_dict = {}
                    ref_dict["key"] = subchild.attrib["key"]
                    ref_dict["author_list"] = []
                    ref_dict["scope"] = []
                    for infrachild in subchild:
                        if infrachild.tag == "{http://uniprot.org/uniprot}citation":
                            if "type" in infrachild.attrib:
                                ref_dict["type"] = infrachild.attrib["type"]
                            if "date" in infrachild.attrib:
                                ref_dict["date"] = infrachild.attrib["date"]
                            if "name" in infrachild.attrib:
                                ref_dict["name"] = infrachild.attrib["name"]
                            if "volume" in infrachild.attrib:
                                ref_dict["volume"] = infrachild.attrib["volume"]
                            if "first" in infrachild.attrib:
                                ref_dict["first"] = infrachild.attrib["first"]
                            if "last" in infrachild.attrib:
                                ref_dict["last"] = infrachild.attrib["last"]
                        for subinfrachild in infrachild:
                            if subinfrachild.tag == "{http://uniprot.org/uniprot}title":
                                ref_dict["title"] = subinfrachild.text
                            elif subinfrachild.tag == "{http://uniprot.org/uniprot}authorList":
                                for infrasubinfrachild in subinfrachild:
                                    if "name" in infrasubinfrachild.attrib:
                                        ref_dict["author_list"].append(infrasubinfrachild.attrib["name"])
                            if subinfrachild.tag == "{http://uniprot.org/uniprot}dbReference":
                                ref_dict[subinfrachild.attrib["type"]] = subinfrachild.attrib["id"]
                        if infrachild.tag == "{http://uniprot.org/uniprot}scope":
                            ref_dict["scope"].append(infrachild.text)
                        elif infrachild.tag == "{http://uniprot.org/uniprot}source":
                            for subinfrachild in infrachild:
                                if subinfrachild.tag == "{http://uniprot.org/uniprot}strain":
                                    ref_dict["strain"] = subinfrachild.text
                    if "reference" in xml_result_obj:
                        xml_result_obj["reference"].append(ref_dict)
                    else:
                        xml_result_obj["reference"] = [ref_dict]
                elif subchild.tag == "{http://uniprot.org/uniprot}comment":
                    comment_dict = {}
                    comment_dict["type"] = subchild.attrib["type"]
                    if "evidence" in subchild.attrib:
                        comment_dict["evidence"] = subchild.attrib["evidence"]
                    
                    for infrachild in subchild:
                        if infrachild.tag == "{http://uniprot.org/uniprot}text":
                            if "evidence" in infrachild.attrib:
                                comment_dict["evidence"] = infrachild.attrib["evidence"]
                            comment_dict["text"] = infrachild.text
                        elif infrachild.tag == "{http://uniprot.org/uniprot}conflict":
                            if "type" in infrachild.attrib:
                                comment_dict["conflict_type"] = infrachild.attrib["type"]
                                for subinfrachild in infrachild:
                                    if subinfrachild.tag == "{http://uniprot.org/uniprot}sequence":
                                        if "resource" in subinfrachild.attrib:
                                            comment_dict["sequence_resource"] = subinfrachild.attrib["resource"]
                                        if "id" in subinfrachild.attrib:
                                            comment_dict["sequence_id"] = subinfrachild.attrib["id"]
                                        if "version" in subinfrachild.attrib:
                                            comment_dict["sequence_version"] = subinfrachild.attrib["version"]
                        elif infrachild.tag == "{http://uniprot.org/uniprot}subcellularLocation":
                            comment_dict["subcellular_location"] = True
                            for subinfrachild in infrachild:
                                if subinfrachild.tag == "{http://uniprot.org/uniprot}location":
                                    if "evidence" in subinfrachild.attrib:
                                        comment_dict["location_evidence"] = subinfrachild.attrib["evidence"]
                                    comment_dict["location"] = subinfrachild.text
                                elif subinfrachild.tag == "{http://uniprot.org/uniprot}topology":
                                    if "evidence" in subinfrachild.attrib:
                                        comment_dict["topology_evidence"] = subinfrachild.attrib["evidence"]
                                    comment_dict["topology"] = subinfrachild.text
                    
                    if "comment" in xml_result_obj:
                        xml_result_obj["comment"].append(comment_dict)
                    else:
                        xml_result_obj["comment"] = [comment_dict]
                        
                    
                for infrachild in subchild:
                    if subchild.tag == "{http://uniprot.org/uniprot}dbReference":
                        if "db_reference" in xml_result_obj:
                            if "type" in infrachild.attrib:
                                xml_result_obj["db_reference"].append({
                                    'id_type': subchild.attrib["type"],
                                    'identifier': subchild.attrib["id"],
                                    'property_type': infrachild.attrib["type"],
                                    'property_value': infrachild.attrib["value"]
                                })
                            else:
                                xml_result_obj["db_reference"].append({
                                    'id_type': subchild.attrib["type"],
                                    'identifier': subchild.attrib["id"]
                                })
                        else:
                            xml_result_obj["db_reference"] = [{
                                'id_type': subchild.attrib["type"],
                                'identifier': subchild.attrib["id"],
                                'property_type': infrachild.attrib["type"],
                                'property_value': infrachild.attrib["value"]
                            }]
                    elif subchild.tag == "{http://uniprot.org/uniprot}organism":
                        if infrachild.tag == "{http://uniprot.org/uniprot}name" and infrachild.attrib["type"] == "scientific":
                            xml_result_obj["organism_scientific_name"] = infrachild.text
                        elif infrachild.tag == "{http://uniprot.org/uniprot}name" and infrachild.attrib["type"] == "common":
                            xml_result_obj["organism_common_name"] = infrachild.text
                        elif infrachild.tag == "{http://uniprot.org/uniprot}dbReference" and infrachild.attrib["type"] == "NCBI Taxonomy":
                            xml_result_obj["ncbi_taxonomy_id"] = infrachild.attrib["id"]
                    elif subchild.tag == "{http://uniprot.org/uniprot}gene":
                        if infrachild.tag == "{http://uniprot.org/uniprot}name":
                            if infrachild.attrib["type"] == "primary":
                                xml_result_obj["primary_gene_name"] = infrachild.text
                            elif infrachild.attrib["type"] == "synonym":
                                xml_result_obj["gene_synonym"] = infrachild.text
                            elif infrachild.attrib["type"] == "ORF":
                                xml_result_obj["gene_orf"] = infrachild.text


                    for subinfrachild in infrachild:
                        if infrachild.tag == "{http://uniprot.org/uniprot}lineage" and subinfrachild.tag == "{http://uniprot.org/uniprot}taxon":
                            if "lineage" in xml_result_obj:
                                xml_result_obj["lineage"].append(subinfrachild.text)
                            else:
                                xml_result_obj["lineage"] = [subinfrachild.text]
                        elif infrachild.tag == "{http://uniprot.org/uniprot}recommendedName":
                            if subinfrachild.tag == "{http://uniprot.org/uniprot}fullName":
                                if "recommended_name" in xml_result_obj:
                                    xml_result_obj["recommended_name"].append(subinfrachild.text)
                                else:
                                    xml_result_obj["recommended_name"] = [subinfrachild.text]
                            elif subinfrachild.tag == "{http://uniprot.org/uniprot}ecNumber":
                                if "ec_number" in xml_result_obj:
                                    xml_result_obj["ec_number"].append(subinfrachild.text)
                                else:
                                    xml_result_obj["ec_number"] = [subinfrachild.text]
                        elif subchild.tag == "{http://uniprot.org/uniprot}evidence" and infrachild.tag == "{http://uniprot.org/uniprot}source" and subinfrachild.tag == "{http://uniprot.org/uniprot}dbReference":
                            if "evidence" in xml_result_obj:
                                    xml_result_obj["evidence"].append({
                                        'key': subchild.attrib["key"],
                                        'type': subchild.attrib["type"],
                                        'db_ref_type': subinfrachild.attrib["type"],
                                        'id': subinfrachild.attrib["id"]
                                    })
                            else:
                                xml_result_obj["evidence"] = [{
                                    'key': subchild.attrib["key"],
                                    'type': subchild.attrib["type"],
                                    'db_ref_type': subinfrachild.attrib["type"],
                                    'id': subinfrachild.attrib["id"]
                                }]

        prot.protein_objects.append({
            'object': xml_result_obj,
            'object_type': "UniProt"
        })
        prot_obj_array.append(xml_result_obj)
    
    return prot_obj_array
    
#   Get UniProtKB AC/ID (accession/identifier).
def get_uniprot_kb_ac_id(prot):
    print("NOT FUNCTIONAL.")

#   Get UniProtKB AC (accession).
def get_uniprot_kb_ac(prot):
    uniprot_array = []
    
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["acc", "uniprot ac", "uniprot acc", "uniprot accession", "uniprotkb ac", "uniprotkb acc", "uniprotkb accession"]:
            uniprot_array.append(ident["identifier"])
            
    if uniprot_array:
        return uniprot_array
            
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() in ["uniprotkb ac+id", "uniprotkb ac+identifier", "uniprotkb ac/id", "uniprotkb ac/identifier", "uniprotkb acc+id", "uniprotkb acc+identifier", "uniprotkb acc/id", "uniprotkb acc/identifier", "uniprotkb accession+id", "uniprotkb accession+identifier", "uniprotkb accession/id", "uniprotkb accession/identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC+ID",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["uniprotkb id", "uniprotkb identifier", "uniprot id", "uniprot identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "ACC",
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
            id_from = newline_sp[0].split("\t")[3].strip()
            id_to = newline_sp[0].split("\t")[2].strip()
            orig_id = newline_sp[1].split("\t")[3].strip()
            new_id = newline_sp[1].split("\t")[2].strip()
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["uniparc", "uniparc id", "uniparc identifier", "uparc", "uparc id", "uparc identifier", "upi"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "UPARC",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
                
        elif ident["identifier_type"].lower() in ["nf50", "nf50 id", "nf50 identifier", "uniref50", "uniref50 id", "uniref50 identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "NF50",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["nf90", "nf90 id", "nf90 identifier", "uniref90", "uniref90 id", "uniref90 identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "NF90",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["nf100", "nf100 id", "nf100 identifier", "uniref100", "uniref100 id", "uniref100 identifier"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "NF100",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() in ["crc64", "crc64 checksum", "crc64 checksum value"]:
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "CRC64",
                "to": "ACC",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
    return uniprot_array
    
#   Get UniProtKB ID (identifier).
def get_uniprot_kb_id(prot):
    uniprot_array = []
    
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "acc":
            uniprot_array.append(ident["identifier"])
            
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb ac+id":
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC+ID",
                "to": "ID",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
    
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "ID",
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
            if new_id not in uniprot_array:
                uniprot_array.append(new_id)
            
    return uniprot_array

#   UNIT TESTS
def uniprot_unit_tests(uniprot_kb_ac_id, uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting UniProtKB ID from UniProtKB accession (%s):" % uniprot_kb_ac)
    for iden in get_uniprot_kb_id(uniprot_kb_ac_prot):
        print("- " + str(iden))
    
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting UniProtKB accession from UniProtKB identifier (%s):" % uniprot_kb_id)
    for iden in get_uniprot_kb_ac(uniprot_kb_id_prot):
        print("- " + str(iden))
        
#   MAIN
if __name__ == "__main__": main()