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
#   Get Wikipedia information.
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

#   Other imports.
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
import json
import re
import requests

#   MAIN
def main():
    wiki_unit_tests("ENSG00000012048", "BRCA2")
    
#   Get Wikipedia accession (Arabic).
def get_arabic_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "ar":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Catalan).
def get_catalan_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "ca":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (German).
def get_german_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "de":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (English).
def get_english_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "en":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                
                try:
                
                    results = sparql.query().convert()

                    for result in results["results"]["bindings"]:
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                        
                except:
                    print("Something went wrong.")
                    
    return wiki_array

#   Get Wikipedia accession (Spanish).
def get_spanish_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "es":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Estonian).
def get_estonian_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "et":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Finnish).
def get_finnish_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "fi":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (French).
def get_french_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "fr":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Italian).
def get_italian_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "it":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Japanese).
def get_japanese_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "en":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Korean).
def get_korean_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "ko":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Dutch).
def get_dutch_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "nl":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                    
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Polish).
def get_polish_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "pl":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Portuguese).
def get_portuguese_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "pt":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Slovenian).
def get_slovenian_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "sl":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Tamil).
def get_tamil_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "ta":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Ukrainian).
def get_ukrainian_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "uk":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikipedia accession (Urdu).
def get_urdu_wikipedia_accession(gene, user = None):
    wiki_array = []
    
    for ident in gene.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]) and ident["language"] == "ur":
            wiki_array.append(ident["identifier"])
            
    if wiki_array:
        return wiki_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            for ext_id in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P594 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ext_id)
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                
                for result in results["results"]["bindings"]:
                    wikidata_regex = re.compile('Q[1-9]\d*')
                    if not re.findall(wikidata_regex, result["itemLabel"]["value"]):
                        temp_iden = gnomics.objects.gene.Gene.add_identifier(gene, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
    return wiki_array

#   Get Wikidata accession.
def get_wikidata_accession(gene):
    gene_array = []
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["wikidata accession", "wikidata"]:
            gene_array.append(ident["identifier"])
            
    if gene_array:
        return gene_array
            
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]:
        
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = json.loads(r.text)
            for key, value in decoded["query"]["pages"].items():
                
                if "pageprops" in value:
                
                    wikidata_id = value["pageprops"]["wikibase_item"]
                    gnomics.objects.gene.Gene.add_identifier(gene, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")

                    gene_array.append(wikidata_id)
                    
                elif "pageid" in value:
                    
                    wikidata_id = value["pageid"]
                    if "Q" in str(wikidata_id):
                        gnomics.objects.gene.Gene.add_identifier(gene, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")

                        gene_array.append(wikidata_id)
                    
            return gene_array
                
    if gene_array:
        return gene_array
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene identifier", "ensembl gene id"]:
            get_english_wikipedia_accession(gene)
            return get_wikidata_accession(gene)

#   Get Wikidata object.
def get_wikidata_object(gene):
    wikidata_obj_array = []
    for gene_obj in gene.gene_objects:
        if 'object_type' in gene_obj:
            if gene_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(gene_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in get_wikidata_accession(gene):
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.gene.Gene.add_object(gene, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   UNIT TESTS
def wiki_unit_tests(ensembl_gene_id, wikipedia_accession):
    ensembl_gene = gnomics.objects.gene.Gene(identifier = str(ensembl_gene_id), identifier_type = "Ensembl Gene ID", source = "Ensembl")
    print("Getting English Wikipedia accession from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for gen in get_english_wikipedia_accession(ensembl_gene):
        print("- %s" % gen)        
    print("\nGetting Wikidata accession from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for gen in get_wikidata_accession(ensembl_gene):
        print("- %s" % gen)
        
    wikipedia_gene = gnomics.objects.gene.Gene(identifier = str(wikipedia_accession), identifier_type = "Wikipedia Accession", source = "Wikipedia", language="en")
    print("\nGetting Korean Wikipedia accession from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for gen in get_wikidata_accession(ensembl_gene):
        print("- %s" % gen)
    
#   MAIN
if __name__ == "__main__": main()