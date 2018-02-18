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
#   Search for mutations/variants.
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
from Bio import Entrez
from gnomics.objects.user import User
import gnomics.objects.gene
import gnomics.objects.variation

#   Other imports.
import eutils.client
import json
import myvariant
import re
import requests
import timeit
import xmltodict

#   MAIN
def main():
    basic_search_unit_tests("rs717620", "")

#   Search.
#
#   Amino acid codes:
#   http://www.fao.org/docrep/004/Y2775E/y2775e0e.htm
def search(query, user = None, search_type = None, taxon = "Homo sapiens", source = "entrez"):
    result_set = []
    
    if (source.lower() in ["myvariant", "all"]):
        mv = myvariant.MyVariantInfo()
        result = mv.query(query)
        
        for hit in result["hits"]:
            temp_identifier_list = []
            
            temp_var = gnomics.objects.variation.Variation(identifier = hit["_id"], identifier_type = "HGVS ID", language = None, source = "MyVariant", taxon = "Homo sapiens")
            temp_identifier_list.append(hit["_id"])
            
            if "gnomad_genome" in hit:
                if hit["gnomad_genome"]["rsid"] not in temp_identifier_list:
                    gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = hit["gnomad_genome"]["rsid"], identifier_type = "RS Number", language = None, source = "MyVariant", taxon = "Homo sapiens")
                    temp_identifier_list.append(hit["gnomad_genome"]["rsid"])
                
                if "clinvar" in hit:
                    
                    for genomic_hgvs in hit["clinvar"]["hgvs"]["genomic"]:
                        if genomic_hgvs not in temp_identifier_list:
                            gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = genomic_hgvs, identifier_type = "Genomic HGVS ID", language = None, source = "MyVariant", taxon = "Homo sapiens")
                            temp_identifier_list.append(genomic_hgvs)
                        
                    if "coding" in hit["clinvar"]["hgvs"]:
                        if hit["clinvar"]["hgvs"]["coding"] not in temp_identifier_list:
                            gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = hit["clinvar"]["hgvs"]["coding"], identifier_type = "Coding HGVS ID", language = None, source = "MyVariant", taxon = "Homo sapiens")
                            temp_identifier_list.append(hit["clinvar"]["hgvs"]["coding"])
                        
                    if "variant_id" in hit["clinvar"]:
                        if hit["clinvar"]["variant_id"] not in temp_identifier_list:
                            gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = hit["clinvar"]["variant_id"], identifier_type = "Variant ID", language = None, source = "MyVariant", taxon = "Homo sapiens")
                            temp_identifier_list.append(hit["clinvar"]["variant_id"])
                        
                    if "rcv" in hit["clinvar"]:
                        
                        print("here")
                        print(hit)
                        
                        if type(hit["clinvar"]["rcv"]) == list:
                            for sub_hit in hit["clinvar"]["rcv"]:
                                if sub_hit["accession"] not in temp_identifier_list:
                                    gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = sub_hit["accession"], identifier_type = "ClinVar Accession", name = sub_hit["preferred_name"], taxon = "Homo sapiens")
                                    temp_identifier_list.append(sub_hit["accession"])
                        else:
                            if hit["clinvar"]["rcv"]["accession"] not in temp_identifier_list:
                                gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = hit["clinvar"]["rcv"]["accession"], identifier_type = "ClinVar Accession", name = hit["clinvar"]["rcv"]["preferred_name"], taxon = "Homo sapiens")
                                temp_identifier_list.append(hit["clinvar"]["rcv"]["accession"])
                        
            result_set.append(temp_var)
    
    # Adapted from:
    # https://www.ncbi.nlm.nih.gov/dbvar/content/tools/entrez/
    if (source.lower() in ["ncbi", "entrez", "all"]) and user is not None:
        
        if user.email is not None:
        
            Entrez.email = user.email
            paramEutils = {"usehistory": "Y"}
            full_query = "('variant'[Object Type] AND %s)" % query
            
            eSearch = Entrez.esearch(db="dbvar", term=full_query, **paramEutils)
            res = Entrez.read(eSearch)
            
            if res["IdList"]:
                for iden in res["IdList"]:
                    if taxon == "Homo sapiens":
                        temp_var = gnomics.objects.variation.Variation(identifier = iden, identifier_type = "Variant Region ID", language = None, source = "dbVar", name = None, taxon = taxon)
                        result_set.append(temp_var)
            else:
                paramEutils = {"usehistory": "Y"}
                eSearch = Entrez.esearch(db="snp", term=query, **paramEutils)
                res = Entrez.read(eSearch)
                for iden in res["IdList"]:
                    if taxon == "Homo sapiens":
                        temp_var = gnomics.objects.variation.Variation(identifier = iden, identifier_type = "RS Number", language = None, source = "dbSNP", name = None, taxon = taxon)
                        result_set.append(temp_var)
    
        else:
            print("Search cannot continue without a valid user and a valid email address associated with such a user object.")
    
    if (source.lower() in ["ensembl", "all"]):
        
        if taxon == "Homo sapiens":
            server = "https://rest.ensembl.org"
            ext = "/variation/human/" + str(query) + "?"

            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("No match found.")
            else:

                decoded = r.json()
                
                if "name" in decoded:
                    temp_var = gnomics.objects.variation.Variation(identifier = decoded["name"], identifier_type = "Ensembl Variation ID", language = None, source = "Ensembl", taxon = "Homo sapiens")
                    
                    if "rs" in decoded["name"]:
                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = decoded["name"], identifier_type = "RS Number", language = None, source = "Ensembl", taxon = "Homo sapiens")
                        
                    for syn in decoded["synonyms"]:
                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = syn, identifier_type = "Ensembl Synonym", language = None, source = "Ensembl", taxon = "Homo sapiens")
                    
                    result_set.append(temp_var)
        
    if (source.lower() in ["ebi", "embl", "proteins api", "all"]):
        
        var_match = re.compile(r"[ARNDBCEQZGHILKMFPSTWYV]\d+[ARNDBCEQZGHILKMFPSTWYV]")
        matched = re.findall(var_match, query)
        
        var_match_2 = re.compile(r"[ARNDBCEQZGHILKMFPSTWYV]\d+")
        matched_2 = re.findall(var_match_2, query)
        
        if matched:
            
            gene = query.split(" ")[0].strip()
            variation = query.split(" ")[1].strip().replace("(", "").replace(")", "").strip()
            
            # Get Ensembl identifier from gene query.
            server = "https://rest.ensembl.org"
            ext = "/xrefs/symbol/" + taxon.lower().replace(" ", "_") + "/" + gene + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            ensembl_gene_id = ""
            for x in decoded:
                if "ENSG" in x["id"]:
                    ensembl_gene_id = x["id"]
            
            # Get UniProt identifier from Ensembl identifier.
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ensembl_gene_id + "?"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            uniprot_accession = ""
            for x in decoded:
                if x["dbname"] == "Uniprot_gn":
                    uniprot_accession = x["primary_id"]
            
            wild_match = re.compile("([ARNDBCEQZGHILKMFPSTWYV])\d+[ARNDBCEQZGHILKMFPSTWYV]")
            alt_match = re.compile("[ARNDBCEQZGHILKMFPSTWYV]\d+([ARNDBCEQZGHILKMFPSTWYV])")
            
            wildtype = re.findall(wild_match, variation)[0]
            location_1 = ''.join(filter(str.isdigit, variation))
            location_2 = ''.join(filter(str.isdigit, variation))
            alternativesequence = re.findall(alt_match, variation)[0]
        
            url = "https://www.ebi.ac.uk/proteins/api/"
            ext = "variation?offset=0&size=100&wildtype=" + wildtype + "&alternativesequence=" + alternativesequence + "&location=" + str(location_1) + "-" + str(location_2) + "&accession=" + uniprot_accession

            r = requests.get(url+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("Something went wrong.")
            else:
                decoded = r.json()
                
                var_array = []
                var_id_array = []
                for x in decoded:
                    
                    for feat in x["features"]:
                        
                        if "ftId" in feat:

                            temp_var = gnomics.objects.variation.Variation(identifier = feat["ftId"], identifier_type = "ftId", source = "Proteins API")
                            
                            var_id_array.append(feat["ftId"])

                            for xref in feat["xrefs"]:

                                if "COSM" in xref["id"] and xref["id"] not in var_id_array:
                                    gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "COSMIC Mutation ID", source = "COSMIC")
                                    var_id_array.append(xref["id"])

                                elif "rs" in xref["id"] and xref["id"] not in var_id_array:
                                    gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "RS Number", source = "dbSNP")
                                    var_id_array.append(xref["id"])
                                    
                                else:
                                    print("Other identifier found.")
                                    print(xref["id"])

                            result_set.append(temp_var)
                            
                        else:
                            print("No ftId in feature.")
                            print(feat)
        
        elif matched_2:
            
            if len(query.split(" ")) > 1:
                
                gene = query.split(" ")[0].strip()
                variation = query.split(" ")[1].strip().replace("(", "").replace(")", "").strip()

                # Get Ensembl identifier from gene query.
                server = "https://rest.ensembl.org"
                ext = "/xrefs/symbol/" + taxon.lower().replace(" ", "_") + "/" + gene + "?"
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                ensembl_gene_id = ""
                for x in decoded:
                    if "ENSG" in x["id"]:
                        ensembl_gene_id = x["id"]

                # Get UniProt identifier from Ensembl identifier.
                server = "https://rest.ensembl.org"
                ext = "/xrefs/id/" + ensembl_gene_id + "?"
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                uniprot_accession = ""
                for x in decoded:
                    if x["dbname"] == "Uniprot_gn":
                        uniprot_accession = x["primary_id"]

                wild_match = re.compile("([ARNDBCEQZGHILKMFPSTWYV])\d+")

                wildtype = re.findall(wild_match, variation)[0]
                location_1 = ''.join(filter(str.isdigit, variation))
                location_2 = ''.join(filter(str.isdigit, variation))

                url = "https://www.ebi.ac.uk/proteins/api/"
                ext = "variation?offset=0&size=100&wildtype=" + wildtype + "&location=" + str(location_1) + "-" + str(location_2) + "&accession=" + uniprot_accession

                r = requests.get(url+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong.")
                else:
                    decoded = r.json()
                    var_array = []
                    var_id_array = []

                    for x in decoded:
                        for feat in x["features"]:
                            if "ftId" in feat:

                                temp_var = gnomics.objects.variation.Variation(identifier = feat["ftId"], identifier_type = "ftId", source = "Proteins API")
                                var_id_array.append(feat["ftId"])

                                for xref in feat["xrefs"]:
                                    if "COSM" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "COSMIC Mutation ID", source = "COSMIC")
                                        var_id_array.append(xref["id"])

                                    elif "rs" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "RS Number", source = "dbSNP")
                                        var_id_array.append(xref["id"])

                                    elif "RCV" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "ClinVar Accession", source = "ClinVar")
                                        var_id_array.append(xref["id"])

                                    else:
                                        continue

                                result_set.append(temp_var)

                            else:

                                temp_var = gnomics.objects.variation.Variation()
                                for xref in feat["xrefs"]:
                                    if "COSM" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "COSMIC Mutation ID", source = "COSMIC")
                                        var_id_array.append(xref["id"])

                                    elif "rs" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "RS Number", source = "dbSNP")
                                        var_id_array.append(xref["id"])

                                    elif "RCV" in xref["id"] and xref["id"] not in var_id_array:
                                        gnomics.objects.variation.Variation.add_identifier(temp_var, identifier = xref["id"], identifier_type = "ClinVar Accession", source = "ClinVar")
                                        var_id_array.append(xref["id"])

                                    else:
                                        continue

                                if len(temp_var.identifiers) > 0:
                                    result_set.append(temp_var)
    
    if (source.lower() in ["ncbi", "entrez"]) and user is not None:
        print("The Entrez database cannot be searched without a valid user email provided.")
        
    return result_set

#   UNIT TESTS
def basic_search_unit_tests(basic_query, email):
    user = User(email = email)
    print("Beginning basic searches for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="all", user=user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nEntrez search returned %s result(s) with the following identifiers:" % str(len(basic_search_results)))
    for ent in basic_search_results:
        for iden in ent.identifiers:
            print("- %s: %s (%s) [%s]" % (iden["identifier"], iden["name"], iden["identifier_type"], iden["taxon"]))

#   MAIN
if __name__ == "__main__": main()