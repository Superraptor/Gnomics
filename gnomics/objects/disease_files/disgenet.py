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
#   DisGeNET functions.
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
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from pymedtermino import *
from pymedtermino.icd10 import *
from pymedtermino.umls import *
from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON

#   MAIN
def main():
    disgenet_unit_tests("2394", "C0010674")

#   Get gene-disease associations (GDAs).
def get_gdas(dis, gen):
    print("NOT FUNCTIONAL.")
    
#   Get GDA evidence.
def get_gda_evidence():
    print("NOT FUNCTIONAL.")

#   Get genes associated with a disease.
def get_genes(dis):
    print("NOT FUNCTIONAL.")
    
#   Get DisGeNET disease ID.
def get_disgenet(dis):
    id_array = []
    results_array = {}
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            if ident["identifier"] not in id_array:
                sparql = SPARQLWrapper("http://rdf.disgenet.org/sparql/")
                sparql.setQuery("""     
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dctypes: <http://purl.org/dc/dcmitype/>
PREFIX wi: <http://http://purl.org/ontology/wi/core#>
PREFIX eco: <http://http://purl.obolibrary.org/obo/eco.owl#>
PREFIX prov: <http://http://http://www.w3.org/ns/prov#>
PREFIX pav: <http://http://http://purl.org/pav/>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?umls 
    ?umlsTerm 
    ?doid 
    ?doTerm 
WHERE { 
    ?gda sio:SIO_000628 ?umls . 
    ?umls dcterms:title ?umlsTerm ;
        skos:exactMatch ?doid .
    ?doid rdfs:label ?doTerm ;
        rdfs:subClassOf+ <%s> .
    FILTER regex(?umls, "umls/id") 
}    
                """ % doid_obolibrary_url(dis))
                sparql.setReturnFormat(JSON)
                try:
                    results = sparql.query().convert()
                    formatted_results = []
                    for result in results["results"]["bindings"]:
                        formatted_results.append(result)
                    id_array.append(ident["identifier"])
                    results_array[ident["identifier"]] = formatted_results
                except:
                    continue
                
    return results_array
    
#   DOID URL (Ontobee).
def doid_obolibrary_url(dis):
    base_url = "http://purl.obolibrary.org/obo/DOID_"
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["doid", "disease ontology id", "disease ontology identifier"]:
            return base_url + str(ident["identifier"])
        
#   Get genes related to a UMLS ID.
def umls_genes(dis):
    id_array = []
    results_array = {}
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier"]:
            if ident["identifier"] not in id_array:
                sparql = SPARQLWrapper("http://rdf.disgenet.org/sparql/")
                sparql.setQuery("""     
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dctypes: <http://purl.org/dc/dcmitype/>
PREFIX wi: <http://http://purl.org/ontology/wi/core#>
PREFIX eco: <http://http://purl.obolibrary.org/obo/eco.owl#>
PREFIX prov: <http://http://http://www.w3.org/ns/prov#>
PREFIX pav: <http://http://http://purl.org/pav/>
PREFIX obo: <http://purl.obolibrary.org/obo/>

SELECT DISTINCT ?gda 
    <%s> as ?disease 
    ?gene
    ?score 
    ?source 
    ?associationType 
    ?pmid 
    ?sentence 
WHERE { 
    ?gda sio:SIO_000628 <%s> ;
        rdf:type ?associationType ; 
        sio:SIO_000628 ?gene ;
        sio:SIO_000216 ?scoreIRI ;
        sio:SIO_000253 ?source . 
    ?scoreIRI sio:SIO_000300 ?score .
    OPTIONAL { 
        ?gda sio:SIO_000772 ?pmid . 
        ?gda dcterms:description ?sentence .
    } 
}
                """ % (linked_life_data_url(dis), linked_life_data_url(dis)))
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                formatted_results = []
                for result in results["results"]["bindings"]:
                    formatted_results.append(result)
                id_array.append(ident["identifier"])
                results_array[ident["identifier"]] = formatted_results
                
    return results_array
        
#   Get Linked Life Data UMLS URL.
def linked_life_data_url(dis):
    base_url = "http://linkedlifedata.com/resource/umls/id/"
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() in ["umls", "umls id", "umls identifier"]:
            return base_url + str(ident["identifier"])

#   UNIT TESTS
def disgenet_unit_tests(doid, umls_id):
    doid_dis = gnomics.objects.disease.Disease(identifier = str(doid), identifier_type = "DOID", source = "Disease Ontology")
    get_disgenet(doid_dis)
    
    umls_dis = gnomics.objects.disease.Disease(identifier = str(umls_id), identifier_type = "UMLS ID", source = "UMLS")
    umls_genes(umls_dis)
    

#   MAIN
if __name__ == "__main__": main()