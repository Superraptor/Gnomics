#
#
#
#
#

#   IMPORT SOURCES:
#       INTERMINE
#           https://pypi.python.org/pypi/intermine
#

#
#   Get Intermine data.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

#   Other imports.
from intermine.webservice import Service
import itertools
import re
import requests, sys

#   Import modules.
import gnomics.objects.gene

#   MAIN
def main():
    intermine_unit_tests("ENSG00000113916", "20674")
    
#   FLYMINE
def flymine(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl gene id":
            s = Service("www.flymine.org/query")
            Gene = s.model.Gene
            q = s.query(Gene).select("*").where("Gene", "LOOKUP", ident["identifier"])
            for row in q.rows():
                primary_identifier = row["primaryIdentifier"]
                brief_description = row["briefDescription"]
                cyto_location = row["cytoLocation"]
                description = row["description"]
                identifier = row["id"]
                length_of_gene = row["length"]
                name_of_gene = row["name"]
                score = row["score"]
                score_type = row["scoreType"]
                secondary_identifier = row["secondaryIdentifier"]
                gene_symbol = row["symbol"]
                gene_object = {
                    'id': identifier,
                    'primary_id': primary_identifier,
                    'secondary_id': secondary_identifier,
                    'symbol': gene_symbol,
                    'name': name_of_gene,
                    'cyto_location': cyto_location,
                    'brief_description': brief_description,
                    'description': description,
                    'length': length_of_gene,
                    'score': score,
                    'score_type': score_type
                }
                return gene_object

#   Flymine Gene ID
def get_flymine_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl gene id":
            gene_obj = flymine(gene)
            return gene_obj["id"]

#   Flymine Primary Gene ID
def get_flymine_primary_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl gene id":
            gene_obj = flymine(gene)
            return gene_obj["primary_id"]
        
#   Flymine Secondary Gene ID
def get_flymine_secondary_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ensembl" or ident["identifier_type"].lower() == "ensembl id" or ident["identifier_type"].lower() == "ensembl identifier" or ident["identifier_type"].lower() == "ensembl gene id":
            gene_obj = flymine(gene)
            return gene_obj["secondary_id"]
    
#   HUMANMINE
def humanmine():
    s = Service("www.humanmine.org/query")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "ENSG00000113916")
    for row in q.rows():
        print(row)
    
#   MOUSEMINE
def mousemine(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez id":
            s = Service("http://www.mousemine.org/mousemine")
            Gene = s.model.Gene
            q = s.query(Gene).select("*").where("Gene", "LOOKUP", ident["identifier"])
            gene_object = {}
            for row in q.rows():
                process = row.__str__()
                for x in re.findall(r"(\w+)=('[0-9A-Za-z:()\- \[\]<>\.,]{1,}'|None|[0-9]{1,})", process):
                    temp_str = x[1]
                    if temp_str[0] == "'" and temp_str[-1] == "'":
                        temp_str = temp_str[1:-1]
                    if x[0] == "briefDescription":
                        if temp_str.strip() == "None":
                            gene_object["brief_description"] = None
                        else:
                            gene_object["brief_description"] = temp_str.strip()
                    elif x[0] == "description":
                        gene_object["description"] = temp_str.strip()
                        for y in re.findall(r"(FUNCTION:[0-9A-Za-z\-\(\) ,.\[]+]|PHENOTYPE:[0-9A-Za-z\-\(\) ,.\[]+])", temp_str):
                            y_split = y.split(":")
                            if y_split[0].strip() == "FUNCTION":
                                gene_object["function"] = y_split[1].strip()
                            elif y_split[0].strip() == "PHENOTYPE":
                                gene_object["phenotype"] = y_split[1].strip()
                    elif x[0] == "id":
                        gene_object["id"] = temp_str.strip()
                    elif x[0] == "length":
                        gene_object["length"] = temp_str.strip()
                    elif x[0] == "mgiType":
                        gene_object["mgi_type"] = temp_str.strip()
                    elif x[0] == "name":
                        gene_object["name"] = temp_str.strip()
                    elif x[0] == "ncbiGeneNumber":
                        gene_object["ncbi_gene_id"] = temp_str.strip()
                    elif x[0] == "primaryIdentifier":
                        gene_object["primary_id"] = temp_str.strip()
                    elif x[0] == "score":
                        if temp_str.strip() == "None":
                            gene_object["score"] = None
                        else:
                            gene_object["score"] = temp_str.strip()
                    elif x[0] == "scoreType":
                        if temp_str.strip() == "None":
                            gene_object["score_type"] = None
                        else:
                            gene_object["score_type"] = temp_str.strip()
                    elif x[0] == "secondaryIdentifier":
                        if temp_str.strip() == "None":
                            gene_object["secondary_id"] = None
                        else:
                            gene_object["secondary_id"] = temp_str.strip()
                    elif x[0] == "specificity":
                        if temp_str.strip() == "None":
                            gene_object["specificity"] = None
                        else:
                            gene_object["specificity"] = temp_str.strip()
                    elif x[0] == "symbol":
                        gene_object["symbol"] = temp_str.strip()
            return gene_object
                
#   Mousemine Gene ID
def get_mousemine_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez id":
            gene_obj = mousemine(gene)
            return gene_obj["id"]

#   Mousemine Primary Gene ID
def get_mousemine_primary_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez id":
            gene_obj = mousemine(gene)
            return gene_obj["primary_id"]
        
#   Mousemine Secondary Gene ID
def get_mousemine_secondary_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "ncbi" or ident["identifier_type"].lower() == "ncbi id" or ident["identifier_type"].lower() == "ncbi gene identifier" or ident["identifier_type"].lower() == "ncbi gene id" or ident["identifier_type"].lower() == "entrez gene id" or ident["identifier_type"].lower() == "entrez id":
            gene_obj = mousemine(gene)
            return gene_obj["secondary_id"]
            
#   RATMINE
def ratmine():
    s = Service("www.ratmine.org/query")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "ENSG00000113916")
    gene_object = {}
    for row in q.rows():
        print(row)
    
#   SYNBIOMINE
def synbiomine():
    s = Service("http://synbiomine.org/query")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "ENSG00000113916")
    for row in q.rows():
        print(row)
    
#   YEASTMINE
def yeastmine():
    s = Service("www.yeastmine.org/query/service")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "ENSG00000113916")
    for row in q.rows():
        print(row)
    
#   ZEBRAFISHMINE
def zebrafishmine():
    s = Service("www.zebrafishmine.org/query")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "ENSG00000113916")
    for row in q.rows():
        print(row)
    
#   UNIT TESTS
def intermine_unit_tests(ensembl_gene_id, ncbi_gene_id):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("Getting FlyMine gene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_flymine_gene_id(ensembl_gene))
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting FlyMine primary gene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_flymine_primary_gene_id(ensembl_gene))
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting FlyMine secondary gene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_flymine_secondary_gene_id(ensembl_gene))
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("\nGetting MGI gene IDs from NCBI Gene ID (%s):" % ncbi_gene_id)
    print("- %s" % get_mousemine_gene_id(ncbi_gene))
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("\nGetting MGI primary gene IDs from NCBI Gene ID (%s):" % ncbi_gene_id)
    print("- %s" % get_mousemine_primary_gene_id(ncbi_gene))
    ncbi_gene = gnomics.objects.gene.Gene(identifier = ncbi_gene_id, identifier_type = "NCBI Gene ID", language = None, taxon = "Homo sapiens", source = "NCBI")
    print("\nGetting MGI secondary gene IDs from NCBI Gene ID (%s):" % ncbi_gene_id)
    print("- %s" % get_mousemine_secondary_gene_id(ncbi_gene))

#   MAIN
if __name__ == "__main__": main()