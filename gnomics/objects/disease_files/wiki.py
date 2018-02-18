#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
#

#
#   Get UMLS.
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
from gnomics.objects.disease_files.disgenet import get_disgenet
from gnomics.objects.user import User
import gnomics.objects.disease

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata.client import Client
import json
import requests

#   MAIN
def main():
    wiki_unit_tests()

#   Get Arabic Wikipedia Accession.
def get_arabic_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ar":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ar". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ar", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Catalan Wikipedia Accession.
def get_catalan_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ca":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ca". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ca", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array    


#   Get German Wikipedia Accession.
def get_german_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "de":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="de", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get English Wikipedia Accession.
def get_english_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "en":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="en", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Spanish Wikipedia Accession.
def get_spanish_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "es":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],es". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="es", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Estonian Wikipedia Accession.
def get_estonian_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "et":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],et". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="et", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Finnish Wikipedia Accession.
def get_finnish_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "fi":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fi". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fi", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get French Wikipedia Accession.
def get_french_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "fr":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],fr". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="fr", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Italian Wikipedia Accession.
def get_italian_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "it":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],it". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="it", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Japanese Wikipedia Accession.
def get_japanese_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ja":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ja". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ja", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Korean Wikipedia Accession.
def get_korean_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ko":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ko". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ko", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Dutch Wikipedia Accession.
def get_dutch_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "nl":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="nl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Polish Wikipedia Accession.
def get_polish_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "pl":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Portuguese Wikipedia Accession.
def get_portuguese_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "pt":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],pt". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="pt", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Slovenian Wikipedia Accession.
def get_slovenian_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "sl":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],sl". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="sl", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Tamil Wikipedia Accession.
def get_tamil_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ta":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ta". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ta", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array


#   Get Ukrainian Wikipedia Accession.
def get_ukrainian_wikipedia_accession(dis, user=None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "uk":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],uk". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="uk", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Urdu Wikipedia Accession.
def get_urdu_wikipedia_accession(dis, user = None):
    wiki_array = []
    
    ids_completed = []
    for ident in dis.identifiers:
        if (ident["identifier_type"].lower() in ["wikipedia", "wikipedia accession"]) and ident["language"] == "ur":
            if ident["identifier"] not in wiki_array and ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                wiki_array.append(ident["identifier"])
                
    if wiki_array:
        return wiki_array
    
    for ident in dis.identifiers:
                                
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P699 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P2892 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P4229 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P486 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P492 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
                    
        elif ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
                sparql_query = """
                SELECT ?item ?itemLabel 
                WHERE 
                {
                  ?item wdt:P1692 "%s".
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],ur". }
                }""" % (ident["identifier"])
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()

                for result in results["results"]["bindings"]:
                    if result["itemLabel"]["value"] not in wiki_array:
                        temp_iden = gnomics.objects.disease.Disease.add_identifier(dis, identifier = result["itemLabel"]["value"], identifier_type = "Wikipedia Accession", language="ur", source="Wikidata")

                        wiki_array.append(result["itemLabel"]["value"])
        
    return wiki_array

#   Get Wikidata accession.
def get_wikidata_accession(dis):
    dis_array = []
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["wikidata accession", "wikidata", "wikidata identifier", "wikidata id"]:
            dis_array.append(ident["identifier"])
            
    if dis_array:
        return dis_array
            
    ids_completed = []
    for ident in dis.identifiers:
        
        if ident["identifier_type"].lower() in ["wikipedia accession", "wikipedia"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
        
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
                        if wikidata_id not in dis_array:
                            gnomics.objects.disease.Disease.add_identifier(dis, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                            dis_array.append(wikidata_id)
                    
                    elif "pageid" in value:
                        wikidata_id = value["pageid"]
                        if wikidata_id not in dis_array:
                            if "Q" in str(wikidata_id):
                                gnomics.objects.disease.Disease.add_identifier(dis, identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                                dis_array.append(wikidata_id)
                    
                return dis_array
                
    if dis_array:
        return dis_array
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    if dis_array:
        return dis_array
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier", "umls cui"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    if dis_array:
        return dis_array
        
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["icd10", "icd10 code", "icd10 id", "icd10 identifier", "icd-10-cm", "icd-10-cm code", "icd-10-cm id", "icd-10-cm identifier"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    if dis_array:
        return dis_array
                    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["mesh", "mesh id", "mesh identifier", "mesh code", "mesh uid"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    if dis_array:
        return dis_array
                    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["omim", "omim id", "omim identifier", "omim disease id", "mim number", "mim"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    if dis_array:
        return dis_array
                    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["icd9", "icd-9", "icd-9-cm", "icd-9-cm id", "icd-9-cm identifier", "icd-9-cm code"]:
            if ident["identifier"] not in ids_completed:
                ids_completed.append(ident["identifier"])
                if len(get_english_wikipedia_accession(dis)) > 0:
                    return get_wikidata_accession(dis)
        
    return dis_array

#   Get Wikidata object.
def get_wikidata_object(dis):
    wikidata_obj_array = []
    for dis_obj in dis.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(dis_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in get_wikidata_accession(dis):
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.disease.Disease.add_object(dis, obj = entity.attributes, object_type = "Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array

#   Get Wikidata Synonyms
def get_wikidata_synonyms(dis, language="en"):
    wiki_syn_array = []
    wiki_id_array = []
    
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["wikidata accession", "wikidata"]:
            if ident["name"] not in wiki_syn_array and ident["identifier"] not in wiki_id_array:
                if ident["name"] is not None:
                    wiki_syn_array.append(ident["name"])
                wiki_id_array.append(ident["identifier"])
                for stuff in gnomics.objects.disease.Disease.wikidata(dis):
                    if language.lower() in ["english", "en", "eng", "all"]:
                        if "en" in stuff["aliases"]:
                            for syn in stuff["aliases"]["en"]:
                                if syn["value"] not in wiki_syn_array:
                                    wiki_syn_array.append(syn["value"])
                                    gnomics.objects.disease.Disease.add_identifier(dis, identifier=ident["identifier"], identifier_type="Wikidata Accession", source="Wikidata", name=syn["value"])
     
    return wiki_syn_array
    
#   UNIT TESTS
def wiki_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()