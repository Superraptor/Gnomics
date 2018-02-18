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
#   Get cell lines from a gene.
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
import gnomics.objects.cell_line

#   Other imports.
import json
import numpy
import requests
import timeit
import xml.etree.ElementTree as ET

#   MAIN
def main():
    gene_cell_line_unit_tests("ENSG00000134057")

# Get cell line expression.
def get_cell_line_expression(gene):
    cell_array = []
    cell_dict = {}
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]:
            server = "https://www.proteinatlas.org/"
            ext = ident["identifier"] + ".xml"
            r = requests.get(server+ext)
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            tree = ET.ElementTree(ET.fromstring(r.text))
            root = tree.getroot()
            for child in root:
                for subchild in child:
                    if subchild.tag == "rnaExpression":
                        exp_source = subchild.attrib["source"]
                        exp_tech = subchild.attrib["technology"]
                        for infrachild in subchild:
                            if infrachild.tag == "data":
                                cell_name = None
                                level_type = None
                                level_tpm = None
                                level_text = None
                                for subinfrachild in infrachild:
                                    if subinfrachild.tag == "cellLine":
                                        cell_name = subinfrachild.text
                                    elif subinfrachild.tag == "level":
                                        level_type = subinfrachild.attrib["type"]
                                        level_tpm = subinfrachild.attrib["tpm"]
                                        level_text = subinfrachild.text
                                if cell_name is not None:
                                    temp_cell_line = gnomics.objects.cell_line.CellLine(identifier = cell_name, identifier_type = "The Human Protein Atlas Accession", source = "The Human Protein Atlas")
                                    cell_dict[cell_name] = {
                                        'method': "RNA Expression",
                                        'cell_line': temp_cell_line,
                                        'type': level_type,
                                        'tpm': level_tpm,
                                        'level': level_text,
                                        'source': exp_source,
                                        'technology': exp_tech
                                    }
            
    return cell_dict
        
#   UNIT TESTS
def gene_cell_line_unit_tests(ensembl_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("Getting cell line gene expression from Ensembl Gene ID (%s):" % ensembl_gene_id)
    
    start = timeit.timeit()
    all_genes = get_cell_line_expression(ensembl_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for key, val in all_genes.items():
        print("- %s" % key)
        print("  - method: %s" % val["method"])
        print("  - type: %s" % val["type"])
        print("  - tpm: %s" % val["tpm"])
        print("  - level: %s" % val["level"])
        print("  - source: %s" % val["source"])
        print("  - technology: %s" % val["technology"])
    
#   MAIN
if __name__ == "__main__": main()