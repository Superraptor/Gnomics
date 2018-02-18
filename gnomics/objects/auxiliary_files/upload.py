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
#   Upload file for querying.
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
import gnomics.objects.biological_process
import gnomics.objects.cellular_component
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.molecular_function
import gnomics.objects.phenotype
import gnomics.objects.person
import gnomics.objects.symptom
import gnomics.objects.variation

#   Other imports.
from itertools import combinations, product
import json
import requests
import time
import xml.etree.ElementTree

#   MAIN
def main():
    upload_unit_tests("../../scripts/other_scripts/overview_pm_sample_queries.xml")
    
#   Once everything is loaded, get known references
#   to create a vocabulary for the identifier alongside
#   a directory of synonyms.
#
#   (make sure to remove stopwords).
def create_vocabulary(identifier_dict):
    print("NOT FUNCTIONAL.")
    
    # Second: get all references for all synonyms.
    # This will use `disease_reference.py`,
    # `phenotype_reference.py`, `variation_reference.py`,
    # `gene_reference.py`, and `symptom_reference.py`.
    
    # Third: extract all text from all references.
    # This will use the abstract function in the reference
    # object.
    
    # Fourth: magic, part 1.
    # Remove stopwords.
    # Make histograms of vocabulary that shows up
    # that isn't any of the synonyms; then rank
    # how often each word or phrase shows up.
    
    # Fifth: magic, part 2.
    # Look at overlapping references and compare
    # vocabularies.
    
    # Sixth: magic, part 3.
    # Find way to integrate demographic data...?
    # Use overlapping vocabularies to rank other
    # abstracts, based on matching a synonym, a term,
    # or the vocabulary.

#   Search via file upload.
def search(file_path, user = None, file_format = "xml"):
    if file_format == "xml":
        e = xml.etree.ElementTree.parse(file_path).getroot()
        
        topic_dict = {}
        for topic in e.findall("topic"):
            topic_dict[topic.attrib["number"]] = {}
            for child in topic.getchildren():
                topic_dict[topic.attrib["number"]][child.tag] = child.text
                
        mapping_dict = {}
        for topic, topic_info in topic_dict.items():
            mapping_dict[topic] = {}
            for topic_type, topic_terms in topic_info.items():
                if topic_type.lower() == "disease":
                    
                    # Make more exact search.
                        # Get synonyms and other identifiers.
                    if topic_terms is not None:
                        mapping_dict[topic]["disease"] = gnomics.objects.disease.Disease.search(topic_terms.strip(), search_type = "exact")

                        for disease in mapping_dict[topic]["disease"]:
                            gnomics.objects.disease.Disease.all_identifiers(disease)

                        new_dis_array = []
                        pair_list = pairs_no_dupes(mapping_dict[topic]["disease"], mapping_dict[topic]["disease"])
                        dis_done = []
                        for dis_pair in pair_list:

                            dis3_check = gnomics.objects.disease.Disease.merge(dis_pair[0], dis_pair[1])

                            if dis3_check and (dis_pair[0] not in dis_done and dis_pair[1] not in dis_done):

                                new_dis_array.append(dis3_check)
                                dis_done.append(dis_pair[0])
                                dis_done.append(dis_pair[1])

                        if new_dis_array:
                            mapping_dict[topic]["disease"] = new_dis_array
                    
                elif topic_type.lower() == "gene":
                    mapping_dict[topic]["gene"] = {}
                    mapping_dict[topic]["variation"] = {}
                    mapping_dict[topic]["molecular_function"] = {}
                    
                    if topic_terms:
                        gene_topic_array = topic_terms.split(",")
                        for gene_topic in gene_topic_array:

                            if "(" in gene_topic and ")" in gene_topic:

                                gene_name = gene_topic.strip().split(" ")[0]
                                var_name = gene_topic.strip().split(" ")[1].replace(")","").replace("(","")

                                # Search for gene name.
                                mapping_dict[topic]["gene"][gene_name.strip()] = gnomics.objects.gene.Gene.search(gene_name.strip())
                                for gene in mapping_dict[topic]["gene"][gene_name.strip()]:
                                    gnomics.objects.gene.Gene.all_identifiers(gene)

                                # Search for variation using gene name and variation name.
                                mapping_dict[topic]["variation"][gene_topic.strip()] = gnomics.objects.variation.Variation.search(gene_topic.strip(), taxon = "Homo sapiens", source = "ebi")
                                if gene_name.strip() in mapping_dict[topic]["variation"]:
                                    for variation in mapping_dict[topic]["variation"][gene_name.strip()]:
                                        gnomics.objects.variation.Variation.all_identifiers(variation)

                            else:
                                sub_gene_topic_array = gene_topic.split(" ")

                                # Try searching for each substring as a gene. If not a gene, then search for the string in OLS.
                                for sub_gene_topic in sub_gene_topic_array:

                                    gene_search = gnomics.objects.gene.Gene.search(sub_gene_topic.strip())
                                    if gene_search:
                                        mapping_dict[topic]["gene"][sub_gene_topic.strip()] = gene_search

                                        for gene in mapping_dict[topic]["gene"][sub_gene_topic.strip()]:
                                            gnomics.objects.gene.Gene.all_identifiers(gene)
                                    else:

                                        # Use full string to search in OLS.

                                        # Search for molecular function.
                                        molecular_function_search_full = gnomics.objects.molecular_function.MolecularFunction.search(gene_topic.strip(), search_type = "exact")
                                        mapping_dict[topic]["molecular_function"][gene_topic.strip()] = molecular_function_search_full

                                        for molec in mapping_dict[topic]["molecular_function"][gene_topic.strip()]:
                                            gnomics.objects.molecular_function.MolecularFunction.all_identifiers(molec, user = None)


                                        # After full string search, begin
                                        # single word search.

                                        # Search for molecular function.
                                        molecular_function_search_part = gnomics.objects.molecular_function.MolecularFunction.search(sub_gene_topic.strip(), search_type = "exact")
                                        mapping_dict[topic]["molecular_function"][sub_gene_topic.strip()] = molecular_function_search_part

                                        for molec in mapping_dict[topic]["molecular_function"][sub_gene_topic.strip()]:
                                            gnomics.objects.molecular_function.MolecularFunction.all_identifiers(molec, user = None)
                            
                elif topic_type.lower() == "demographic":
                    
                    if topic_terms:
                    
                        # Search for demographic information.
                        mapping_dict[topic]["demographics"] = gnomics.objects.person.parse_demographics(topic_terms)
                    
                elif topic_type.lower() == "other":
                    
                    mapping_dict[topic]["other"] = {}
                
                    if topic_terms:
                        other_topic_array = topic_terms.split(",")
                        for other_topic in other_topic_array:
                            if other_topic != "None" and other_topic is not None:

                                mapping_dict[topic]["other"][other_topic.strip()] = {}

                                # Search as a disease.
                                    # Get synonyms and other identifiers.
                                mapping_dict[topic]["other"][other_topic.strip()]["disease"] = gnomics.objects.disease.Disease.search(other_topic.strip(), search_type = "exact")
                                for disease in mapping_dict[topic]["other"][other_topic.strip()]["disease"]:
                                    gnomics.objects.disease.Disease.all_identifiers(disease)
                                new_dis_array_other = []
                                pair_list = pairs_no_dupes(mapping_dict[topic]["other"][other_topic.strip()]["disease"], mapping_dict[topic]["other"][other_topic.strip()]["disease"])
                                dis_done_other = []
                                for dis_pair in pair_list:
                                    dis3_check_other = gnomics.objects.disease.Disease.merge(dis_pair[0], dis_pair[1])
                                    if dis3_check_other and (dis_pair[0] not in dis_done_other and dis_pair[1] not in dis_done_other):
                                        new_dis_array_other.append(dis3_check_other)
                                        dis_done_other.append(dis_pair[0])
                                        dis_done_other.append(dis_pair[1])
                                if new_dis_array_other:
                                    mapping_dict[topic]["other"][other_topic.strip()]["disease"] = new_dis_array_other

                                # Search as a phenotype.
                                    # Get synonyms and other identifiers.
                                mapping_dict[topic]["other"][other_topic.strip()]["phenotype"] = gnomics.objects.phenotype.Phenotype.search(other_topic.strip(), taxon = "Homo sapiens", search_type = "exact")
                                for phenotype in mapping_dict[topic]["other"][other_topic.strip()]["phenotype"]:
                                    gnomics.objects.phenotype.Phenotype.all_identifiers(phenotype)

                                # Search as a symptom.
                                    # Make more exact search.
                                    # Try to find acronyms as well.
                                    # Get synonyms and other identifiers.
                                mapping_dict[topic]["other"][other_topic.strip()]["symptom"] = gnomics.objects.symptom.Symptom.search(other_topic.strip())
                                for symptom in mapping_dict[topic]["other"][other_topic.strip()]["symptom"]:
                                    gnomics.objects.symptom.Symptom.all_identifiers(symptom)
                        
                else:
                    print("Tag '%s' not recognized. Skipping..." % topic_type)
                    
        return mapping_dict
    
#   Create terms list.
def terms_list(file_path):
    search_results = search(file_path, user = None, file_format = "xml")
    print(search_results)
    
    new_topic_map = {}
    for topic_no, topic_dict in search_results.items():
        new_topic_map[str(topic_no)] = {}
        for topic_type, topic_map in topic_dict.items():
            new_topic_map[str(topic_no)][topic_type] = {}
            if type(topic_map) != list:
                for thing, thing_dict in topic_map.items():
                    new_topic_map[str(topic_no)][topic_type][thing] = []
                    if thing_dict is list:
                        for sub_thing in thing_dict:
                            for iden in sub_thing.identifiers:
                                if "name" in iden:
                                    if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                        new_topic_map[str(topic_no)][topic_type][thing].append(iden["name"])
                                if "identifier" in iden:
                                    if iden["identifier"] is not None and iden["identifier"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                        new_topic_map[str(topic_no)][topic_type][thing].append(iden["identifier"])
                    else:
                        if topic_type == "demographics":
                            if "name" in thing_dict:
                                if thing_dict["name"] is not None and thing_dict["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                    new_topic_map[str(topic_no)][topic_type][thing].append(thing_dict["name"])
                        elif topic_type == "gene":
                            for gene_array in thing_dict:
                                if gene_array is not None:
                                    for iden in gene_array.identifiers:
                                        if "name" in iden:
                                            if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                                new_topic_map[str(topic_no)][topic_type][thing].append(iden["name"])
                                        if iden["identifier"] is not None and iden["identifier"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                            new_topic_map[str(topic_no)][topic_type][thing].append(iden["identifier"])
                        elif topic_type == "molecular_function":
                            for molec_array in thing_dict:
                                if molec_array is not None:
                                    for iden in molec_array.identifiers:
                                        if "name" in iden:
                                            if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                                new_topic_map[str(topic_no)][topic_type][thing].append(iden["name"])   
                        elif topic_type == "variation":
                            for var_array in thing_dict:
                                if var_array is not None:
                                    for iden in var_array.identifiers:
                                        if "name" in iden:
                                            if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                                new_topic_map[str(topic_no)][topic_type][thing].append(iden["name"])
                                        if iden["identifier"] is not None and iden["identifier"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                            new_topic_map[str(topic_no)][topic_type][thing].append(iden["identifier"])
                        else:
                            if type(thing_dict) == dict:
                                for infra_thing, infra_dict in thing_dict.items():
                                    for x in infra_dict:
                                        if x is not None:
                                            for iden in x.identifiers:
                                                if "name" in iden:
                                                    if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type][thing]:
                                                        new_topic_map[str(topic_no)][topic_type][thing].append(iden["name"])
            else:
                new_topic_map[str(topic_no)][topic_type] = []
                for counter, thing in enumerate(topic_map):
                    for iden in thing.identifiers:
                        if "name" in iden:
                            if iden["name"] is not None and iden["name"] not in new_topic_map[str(topic_no)][topic_type]:
                                new_topic_map[str(topic_no)][topic_type].append(iden["name"])
                                
    return new_topic_map
    
#   Generating pairs from lists.
def pairs(*lists):
    for t in combinations(lists, 2):
        for pair in product(*t):
            if pair[0] != pair[1]:
                yield pair
                
#   Pairs without duplicates.
def pairs_no_dupes(*lists):
    return set(pairs(*lists))

#   UNIT TESTS
def upload_unit_tests(file_path):
    topic_map = terms_list(file_path)
    print(topic_map)

#   MAIN
if __name__ == "__main__": main()