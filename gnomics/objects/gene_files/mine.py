#!/usr/bin/env python

#
#
#
#
#

#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       EUTILS
#           https://github.com/biocommons/eutils
#       INTERMINE
#           https://pypi.python.org/pypi/intermine
#

#
#   Get Intermine data.
#

#
#   Note that only particular identifiers work on InterMine:
#   http://intermine.readthedocs.io/en/latest/database/data-sources/id-resolvers/
#
#   These include Entrez Gene IDs, 
#   FlyBase IDs (D. melanogaster only), 
#   WormBase IDs (C. elegans only),
#   Zebrafish (Zfin) IDs, Mouse (Mgi) IDs, Rat (Rgd) IDs, 
#   HGNC Human Gene IDs, Ensembl gene IDs, and Human IDs.
#   
#   See also: 
#   - http://intermine.readthedocs.io/en/latest/web-services/how-do-i/
#   - http://intermine.readthedocs.io/en/latest/web-services/tutorial/
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
from bioservices import *
from bioservices.uniprot import UniProt
from intermine.webservice import Service
import eutils.client
import intermine
import itertools
import re
import requests

#   Import modules.
import gnomics.objects.gene

#   MAIN
def main():
    intermine_unit_tests("ENSG00000113916", "20674", "RGD:3001", "WBGene00000001")
    
#   FLYMINE
def flymine(gene):
    obj_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id"]:
            s = Service("www.flymine.org/query")
            Gene = s.model.Gene
            q = s.query(Gene).select("*").where("Gene", "LOOKUP", ident["identifier"])
            try:
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
                    obj_array.append(gene_object)
            except intermine.errors.WebserviceError:
                print("A webservice error occurred. Please contact Intermine support.")
            else:
                print("Something else went wrong.")
    return obj_array

#   Flymine Gene ID
def get_flymine_gene_id(gene):
    flymine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["flymine id", "flymine identifier, flymine gene id", "flymine gene identifier"]):
        if iden["identifier"] not in flymine_array:
            flymine_array.append(iden["identifier"])

    if flymine_array:
        return flymine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = flymine(gene)
            for obj in gene_obj:
                flymine_array.append(obj["id"])
    
    return flymine_array

#   Flymine Primary Gene ID
def get_flymine_primary_gene_id(gene):
    flymine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["flymine primary id", "flymine primary identifier, flymine primary gene id", "flymine primary gene identifier"]):
        if iden["identifier"] not in flymine_array:
            flymine_array.append(iden["identifier"])

    if flymine_array:
        return flymine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = flymine(gene)
            for obj in gene_obj:
                flymine_array.append(obj["primary_id"])
    
    return flymine_array
        
#   Flymine Secondary Gene ID
def get_flymine_secondary_gene_id(gene):
    flymine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["flymine secondary id", "flymine secondary identifier, flymine secondary gene id", "flymine secondary gene identifier"]):
        if iden["identifier"] not in flymine_array:
            flymine_array.append(iden["identifier"])

    if flymine_array:
        return flymine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = flymine(gene)
            for obj in gene_obj:
                flymine_array.append(obj["secondary_id"])
    
    return flymine_array
    
#   HUMANMINE
def humanmine():
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["humanmine primary id", "humanmine primary identifier", "humanmine primary gene id", "humanmine primary gene identifier"]):
    
        s = Service("www.humanmine.org/humanmine")
        Gene = s.model.Gene
        q = s.query(Gene).select("*").where("Gene", "LOOKUP", iden["identifier"])
        gene_object = {}  
        for row in q.rows():
            process = row.__str__()
            for x in re.findall(r"(\w+)=('[0-9A-Za-z:()\- \[\]<>\.,]{1,}'|None|[0-9]{1,})", process):

                temp_str = x[1]
                if temp_str[0] == "'" and temp_str[-1] == "'":
                    temp_str = temp_str[1:-1]
                    
                if x[0] == "description":
                    gene_object["description"] = temp_str.strip()
                elif x[0] == "cytoLocation":
                    gene_object["cytogenetic_location"] = temp_str.strip()
                elif x[0] == "id":
                    gene_object["id"] = temp_str.strip()
                elif x[0] == "length":
                    gene_object["length"] = temp_str.strip()
                elif x[0] == "primaryIdentifier":
                    gene_object["primary_id"] = temp_str.strip()
                elif x[0] == "score":
                    gene_object["score"] = temp_str.strip()
                elif x[0] == "scoreType":
                    gene_object["score_type"] = temp_str.strip()
                elif x[0] == "secondaryIdentifier":
                    gene_object["secondary_id"] = temp_str.strip()
                elif x[0] == "symbol":
                    gene_object["symbol"] = temp_str.strip()
                        
        return gene_object
    
#   Humanmine Gene ID
def get_humanmine_gene_id(gene):
    humanmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["humanmine id", "humanmine identifier", "humanmine gene id", "humanmine gene identifier"]):
        if iden["identifier"] not in humanmine_array:
            humanmine_array.append(iden["identifier"])
    return humanmine_array

#   Humanmine Primary Gene ID
def get_humanmine_primary_gene_id(gene):
    humanmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["humanmine primary id", "humanmine primary identifier", "humanmine primary gene id", "humanmine primary gene identifier"]):
        if iden["identifier"] not in humanmine_array:
            humanmine_array.append(iden["identifier"])
    return humanmine_array

#   Humanmine Secondary Gene ID
def get_humanmine_secondary_gene_id(gene):
    humanmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["humanmine secondary id", "humanmine secondary identifier", "humanmine secondary gene id", "humanmine secondary gene identifier"]):
        if iden["identifier"] not in humanmine_array:
            humanmine_array.append(iden["identifier"])
    return humanmine_array
    
#   MOUSEMINE
def mousemine(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ncbi", "ncbi id", "ncbi gene identifier", "ncbi gene id", "entrez gene id", "entrez id"]:
            s = Service("www.mousemine.org/mousemine")
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
    mousemine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["mousemine id", "mousemine identifier, mousemine gene id", "mousemine gene identifier"]):
        if iden["identifier"] not in mousemine_array:
            mousemine_array.append(iden["identifier"])

    if mousemine_array:
        return mousemine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "entrez id", "entrez identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi id", "ncbi identifier", "ncbi-geneid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = mousemine(gene)
            mousemine_array.append(gene_obj["id"])
    
    return mousemine_array

#   Mousemine Primary Gene ID
def get_mousemine_primary_gene_id(gene):
    mousemine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["mousemine primary id", "mousemine primary identifier, mousemine primary gene id", "mousemine primary gene identifier"]):
        if iden["identifier"] not in mousemine_array:
            mousemine_array.append(iden["identifier"])

    if mousemine_array:
        return mousemine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "entrez id", "entrez identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi id", "ncbi identifier", "ncbi-geneid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = mousemine(gene)
            mousemine_array.append(gene_obj["primary_id"])
    
    return mousemine_array
        
#   Mousemine Secondary Gene ID
def get_mousemine_secondary_gene_id(gene):
    mousemine_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["mousemine secondary id", "mousemine secondary identifier, mousemine secondary gene id", "mousemine secondary gene identifier"]):
        if iden["identifier"] not in mousemine_array:
            mousemine_array.append(iden["identifier"])

    if mousemine_array:
        return mousemine_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "entrez id", "entrez identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi id", "ncbi identifier", "ncbi-geneid"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gene_obj = mousemine(gene)
            mousemine_array.append(gene_obj["secondary_id"])
    
    return mousemine_array
            
#   RATMINE
def ratmine(gene):
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ratmine primary id", "ratmine primary identifier", "ratmine primary gene id", "ratmine primary gene identifier"]):
    
        s = Service("http://ratmine.mcw.edu/ratmine")
        Gene = s.model.Gene
        q = s.query(Gene).select("*").where("Gene", "LOOKUP", iden["identifier"])
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
                elif x[0] == "geneType":
                    gene_object["gene_type"] = temp_str.strip()
                elif x[0] == "id":
                    gene_object["id"] = temp_str.strip()
                elif x[0] == "length":
                    gene_object["length"] = temp_str.strip()
                elif x[0] == "name":
                    gene_object["name"] = temp_str.strip()
                elif x[0] == "ncbi_gene_number":
                    gene_object["ncbiGeneNumber"] = temp_str.strip()
                elif x[0] == "pharmGKBidentifier":
                    gene_object["pharmGKB_id"] = temp_str.strip()
                elif x[0] == "primaryIdentifier":
                    gene_object["primary_id"] = temp_str.strip()
                elif x[0] == "score":
                    gene_object["score"] = temp_str.strip()
                elif x[0] == "scoreType":
                    gene_object["score_type"] = temp_str.strip()
                elif x[0] == "secondaryIdentifier":
                    gene_object["secondary_id"] = temp_str.strip()
                elif x[0] == "symbol":
                    gene_object["symbol"] = temp_str.strip()
                        
        return gene_object
    
            
#   Ratmine Gene ID
def get_ratmine_gene_id(gene):
    ratmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ratmine id", "ratmine identifier", "ratmine gene id", "ratmine gene identifier"]):
        if iden["identifier"] not in ratmine_array:
            ratmine_array.append(iden["identifier"])
    return ratmine_array

#   Ratmine Primary Gene ID
def get_ratmine_primary_gene_id(gene):
    ratmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ratmine primary id", "ratmine primary identifier", "ratmine primary gene id", "ratmine primary gene identifier"]):
        if iden["identifier"] not in ratmine_array:
            ratmine_array.append(iden["identifier"])
    return ratmine_array

#   Ratmine Secondary Gene ID
def get_ratmine_secondary_gene_id(gene):
    ratmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["ratmine secondary id", "ratmine secondary identifier", "ratmine secondary gene id", "ratmine secondary gene identifier"]):
        if iden["identifier"] not in ratmine_array:
            ratmine_array.append(iden["identifier"])
    return ratmine_array
        
#   WORMMINE
def wormmine(gene):
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["wormmine primary id", "wormmine primary identifier", "wormmine primary gene id", "wormmine primary gene identifier"]):
    
        s = Service("http://intermine.wormbase.org/tools/wormmine")
        Gene = s.model.Gene
        q = s.query(Gene).select("*").where("Gene", "LOOKUP", iden["identifier"])
        gene_object = {}  
        for row in q.rows():
            process = row.__str__()
            for x in re.findall(r"(\w+)=('[0-9A-Za-z:()\- \[\]<>\.,]{1,}'|None|[0-9]{1,})", process):

                temp_str = x[1]
                if temp_str[0] == "'" and temp_str[-1] == "'":
                    temp_str = temp_str[1:-1]

                if x[0] == "id":
                    gene_object["id"] = temp_str.strip()
                elif x[0] == "lastUpdated":
                    gene_object["last_updated"] = temp_str.strip()
                elif x[0] == "length":
                    gene_object["length"] = temp_str.strip()
                elif x[0] == "name":
                    gene_object["name"] = temp_str.strip()
                elif x[0] == "operon":
                    gene_object["operon"] = temp_str.strip()
                elif x[0] == "primary_id":
                    gene_object["primary_id"] = temp_str.strip()
                elif x[0] == "score":
                    gene_object["score"] = temp_str.strip()
                elif x[0] == "score_type":
                    gene_object["score_type"] = temp_str.strip()
                elif x[0] == "secondary_id":
                    gene_object["secondary_id"] = temp_str.strip()
                elif x[0] == "symbol":
                    gene_object["symbol"] = temp_str.strip()
                        
        return gene_object
    
#   Wormmine Gene ID
def get_wormmine_gene_id(gene):
    wormmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["wormmine id", "wormmine identifier", "wormmine gene id", "wormmine gene identifier"]):
        if iden["identifier"] not in wormmine_array:
            wormmine_array.append(iden["identifier"])
    return wormmine_array

#   Wormmine Primary Gene ID
def get_wormmine_primary_gene_id(gene):
    wormmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["wormmine primary id", "wormmine primary identifier", "wormmine primary gene id", "wormmine primary gene identifier", "wormbase primary id", "wormbase primary identifier"]):
        if iden["identifier"] not in wormmine_array:
            wormmine_array.append(iden["identifier"])
    return wormmine_array

#   Wormmine Secondary Gene ID
def get_wormmine_secondary_gene_id(gene):
    wormmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["wormmine secondary id", "wormmine secondary identifier", "wormmine secondary gene id", "wormmine secondary gene identifier"]):
        if iden["identifier"] not in wormmine_array:
            wormmine_array.append(iden["identifier"])
    return wormmine_array
    
#   YEASTMINE
def yeastmine():
    s = Service("https://yeastmine.yeastgenome.org:443/yeastmine/service")
    Gene = s.model.Gene
    q = s.query(Gene).select("*").where("Gene", "LOOKUP", "Rad51")
    gene_object = {}
    for row in q.rows():
        process = row.__str__()
        for x in re.findall(r"(\w+)=('[0-9A-Za-z:()\- \[\]<>\.,]{1,}'|None|[0-9]{1,})", process):
            print(x)
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["yeastmine primary id", "yeastmine primary identifier", "yeastmine primary gene id", "yeastmine primary gene identifier"]):
        s = Service("https://yeastmine.yeastgenome.org:443/yeastmine/service")
        Gene = s.model.Gene
        q = s.query(Gene).select("*").where("Gene", "LOOKUP", iden["identifier"])
        gene_object = {}  
        for row in q.rows():
            process = row.__str__()
            for x in re.findall(r"(\w+)=('[0-9A-Za-z:()\- \[\]<>\.,]{1,}'|None|[0-9]{1,})", process):

                temp_str = x[1]
                if temp_str[0] == "'" and temp_str[-1] == "'":
                    temp_str = temp_str[1:-1]
                    
                if x[0] == "cytoLocation":
                    gene_object["cytogenetic_location"] = temp_str.strip()
                elif x[0] == "description":
                    gene_object["description"] = temp_str.strip()
                elif x[0] == "featAttribute":
                    gene_object["feature_attribute"] = temp_str.strip()
                elif x[0] == "featureType":
                    gene_object["feature_type"] = temp_str.strip()
                elif x[0] == "functionSummary":
                    gene_object["function_summary"] = temp_str.strip()
                elif x[0] == "id":
                    gene_object["id"] = temp_str.strip()
                elif x[0] == "jasparAccession":
                    gene_object["jaspar_accession"] = temp_str.strip()
                elif x[0] == "jasparClass":
                    gene_object["jaspar_class"] = temp_str.strip()
                elif x[0] == "jasparFamily":
                    gene_object["jaspar_family"] = temp_str.strip()
                elif x[0] == "length":
                    gene_object["length"] = temp_str.strip()
                elif x[0] == "phenotypeSummary":
                    gene_object["phenotype_summary"] = temp_str.strip()
                elif x[0] == "primaryIdentifier":
                    gene_object["primary_id"] = temp_str.strip()
                elif x[0] == "qualifier":
                    gene_object["qualifier"] = temp_str.strip()
                elif x[0] == "score":
                    gene_object["score"] = temp_str.strip()
                elif x[0] == "scoreType":
                    gene_object["score_type"] = temp_str.strip()
                elif x[0] == "secondaryIdentifier":
                    gene_object["secondary_id"] = temp_str.strip()
                elif x[0] == "status":
                    gene_object["status"] = temp_str.strip()
                elif x[0] == "symbol":
                    gene_object["symbol"] = temp_str.strip()
                elif x[0] == "name":
                    gene_object["name"] = temp_str.strip()
                elif x[0] == "sgdAlias":
                    gene_object["sgd_alias"] = temp_str.strip()
                        
        return gene_object
    
#   Yeastmine Gene ID
def get_yeastmine_gene_id(gene):
    yeastmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["yeastmine id", "yeastmine identifier", "yeastmine gene id", "yeastmine gene identifier"]):
        if iden["identifier"] not in yeastmine_array:
            yeastmine_array.append(iden["identifier"])
    return yeastmine_array

#   Yeastmine Primary Gene ID
def get_yeastmine_primary_gene_id(gene):
    yeastmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["yeastmine primary id", "yeastmine primary identifier", "yeastmine primary gene id", "yeastmine primary gene identifier"]):
        if iden["identifier"] not in yeastmine_array:
            yeastmine_array.append(iden["identifier"])
    return yeastmine_array

#   Yeastmine Secondary Gene ID
def get_yeastmine_secondary_gene_id(gene):
    yeastmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["yeastmine secondary id", "yeastmine secondary identifier", "yeastmine secondary gene id", "yeastmine secondary gene identifier"]):
        if iden["identifier"] not in yeastmine_array:
            yeastmine_array.append(iden["identifier"])
    return yeastmine_array
    
#   ZEBRAFISHMINE
def zebrafishmine(gene):
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["zebrafishmine primary id", "zebrafishmine primary identifier", "zebrafishmine primary gene id", "zebrafishmine primary gene identifier"]):
    
        s = Service("http://zebrafishmine.org")
        Gene = s.model.Gene
        q = s.query(Gene).select("*").where("Gene", "LOOKUP", iden["identifier"])
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
                elif x[0] == "id":
                    gene_object["id"] = temp_str.strip()
                elif x[0] == "length":
                    gene_object["length"] = temp_str.strip()
                elif x[0] == "name":
                    gene_object["name"] = temp_str.strip()
                elif x[0] == "primaryIdentifier":
                    gene_object["primary_id"] = temp_str.strip()
                elif x[0] == "score":
                    gene_object["score"] = temp_str.strip()
                elif x[0] == "scoreType":
                    gene_object["score_type"] = temp_str.strip()
                elif x[0] == "secondaryIdentifier":
                    gene_object["secondary_id"] = temp_str.strip()
                elif x[0] == "symbol":
                    gene_object["symbol"] = temp_str.strip()
                        
        return gene_object
            
#   Zebrafishmine Gene ID
def get_zebrafishmine_gene_id(gene):
    zebrafishmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["zebrafishmine id", "zebrafishmine identifier", "zebrafishmine gene id", "zebrafishmine gene identifier"]):
        if iden["identifier"] not in zebrafishmine_array:
            zebrafishmine_array.append(iden["identifier"])
    return zebrafishmine_array

#   Zebrafishmine Primary Gene ID
def get_zebrafishmine_primary_gene_id(gene):
    zebrafishmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["zebrafishmine primary id", "zebrafishmine primary identifier", "zebrafishmine primary gene id", "zebrafishmine primary gene identifier"]):
        if iden["identifier"] not in zebrafishmine_array:
            zebrafishmine_array.append(iden["identifier"])
    return zebrafishmine_array

#   Zebrafishmine Secondary Gene ID
def get_zebrafishmine_secondary_gene_id(gene):
    zebrafishmine_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(gene.identifiers, ["zebrafishmine secondary id", "zebrafishmine secondary identifier", "zebrafishmine secondary gene id", "zebrafishmine secondary gene identifier"]):
        if iden["identifier"] not in zebrafishmine_array:
            zebrafishmine_array.append(iden["identifier"])
    return zebrafishmine_array
    
#   UNIT TESTS
def intermine_unit_tests(ensembl_gene_id, ncbi_gene_id, ratmine_primary_id, wormmine_primary_id):
    
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