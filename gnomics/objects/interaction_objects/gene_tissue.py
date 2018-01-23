#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get tissues from a gene.
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
import gnomics.objects.tissue

#   Other imports.
import json
import numpy
import requests
import xml.etree.ElementTree as ET

#   MAIN
def main():
    gene_tissue_unit_tests(["ENSG00000210049", "ENSG00000211459", "ENSG00000210077", "ENSG00000210082", "ENSG00000209082", "ENSG00000198888", "ENSG00000210100", "ENSG00000210107", "ENSG00000210112"])

# Get tissue expression.
def get_tissue_expression(gene):
    tiss_array = []
    tiss_dict = {}
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier":
            server = "https://www.proteinatlas.org/"
            ext = ident["identifier"] + ".xml"
            r = requests.get(server+ext)
            if not r.ok:
                continue
            else:   
                tree = ET.ElementTree(ET.fromstring(r.text))
                root = tree.getroot()
                for child in root:
                    for subchild in child:
                        if subchild.tag == "rnaExpression":
                            exp_source = subchild.attrib["source"]
                            exp_tech = subchild.attrib["technology"]
                            for infrachild in subchild:
                                if infrachild.tag == "data":
                                    tissue_name = None
                                    level_type = None
                                    level_tpm = None
                                    level_text = None
                                    for subinfrachild in infrachild:
                                        if subinfrachild.tag == "tissue":
                                            tissue_name = subinfrachild.text
                                        elif subinfrachild.tag == "level":
                                            level_type = subinfrachild.attrib["type"]
                                            level_tpm = subinfrachild.attrib["tpm"]
                                            level_text = subinfrachild.text
                                    if tissue_name is not None:
                                        temp_tissue = gnomics.objects.tissue.Tissue(identifier = tissue_name, identifier_type = "The Human Protein Atlas Accession", language = "en", source = "The Human Protein Atlas")
                                        tiss_dict[tissue_name] = {
                                            'method': "RNA Expression",
                                            'tissue': temp_tissue,
                                            'type': level_type,
                                            'tpm': level_tpm,
                                            'level': level_text,
                                            'source': exp_source,
                                            'technology': exp_tech
                                        }
    return tiss_dict
        
#   UNIT TESTS
def gene_tissue_unit_tests(ensembl_ids):
    for ensembl_gene_id in ensembl_ids:
        ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
        print("Getting tissue gene expression from Ensembl Gene ID (%s):" % ensembl_gene_id)
        for key, val in get_tissue_expression(ensembl_gene).items():
            print("- %s" % key)
            print("  - method: %s" % val["method"])
            print("  - type: %s" % val["type"])
            print("  - tpm: %s" % val["tpm"])
            print("  - level: %s" % val["level"])
            print("  - source: %s" % val["source"])
            print("  - technology: %s" % val["technology"])
    
#   MAIN
if __name__ == "__main__": main()