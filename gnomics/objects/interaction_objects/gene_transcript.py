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
#   Get transcripts from a gene.
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
import gnomics.objects.transcript

#   Other imports.
import json
import re
import requests
import timeit

#   MAIN
def main():
    gene_transcript_unit_tests("Q227339", "ENSG00000099899", "BRCA2")

# Get transcripts.
def get_transcripts(gene):
    trans_id_array = []
    trans_array = []
    trans_dict = {}
    
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() in ["wikidata", "wikidata id", "wikidata identifier", "wikidata accession"]:
            for stuff in gnomics.objects.gene.Gene.wikidata(gene):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "refseq rna id":
                        for x in prop_dict:
                            if x["mainsnak"] not in trans_id_array:
                                temp_transcript = gnomics.objects.transcript.Transcript(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "RefSeq RNA ID", source = "Wikidata")
                                trans_array.append(temp_transcript)
                                trans_id_array.append(x["mainsnak"])
                    elif en_prop_name.lower() == "ensembl transcript id":
                        for x in prop_dict:
                            if x["mainsnak"] not in trans_id_array:
                                temp_transcript = gnomics.objects.transcript.Transcript(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Ensembl Transcript ID", source = "Wikidata")
                                trans_array.append(temp_transcript)
                                trans_id_array.append(x["mainsnak"])
         
        elif ident["identifier_type"].lower() in ["ensembl", "ensembl id", "ensembl identifier", "ensembl gene id", "ensembl gene identifier"]:
            if ident["taxon"] is not None:
                proc_taxon = ident["taxon"].lower().replace(" ", "_")

                base = "http://apprisws.bioinfo.cnio.es:80/rest/"
                ext = "exporter/id/" + proc_taxon + "/" + ident["identifier"] + "?format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                ensembl_pattern = re.compile("ENS([GT]|MUST|RNOT|DART)\d{11}|Y[A-Z]{2}\d{3}[A-Z](-[A-Z])?|FBtr\d{7}|Q\d{4}|((([0-9]?[A-Z]{1,4}\d{1,3})[A-Z0-9]?)|(cTel\d{2}X)|([0-9]RSSE)|(Y[0-9]{1,3}[A-Z]\d{1,2}((LA|UA)|[A-C][A-Z]?)))*(\.\d{1,4}[a-z]?)+")
                refseq_pattern = re.compile("(N|X)(M|R)_(\d{6}|\d{9})")

                for x in decoded:
                    if "transcript_name" in x:
                        if x["transcript_name"] not in trans_id_array and x["transcript_id"] not in trans_id_array:
                            if ensembl_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            elif refseq_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            else:
                                print(x["transcript_id"])
                    elif "transcript_id" in x:
                        if x["transcript_id"] not in trans_id_array:
                            if ensembl_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS")
                                trans_array.append(temp_trans)
                                trans_id_array.append(temp_trans)
                            elif refseq_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            else:
                                print(x["transcript_id"])
                    else:
                        print(x)
                    
        elif ident["identifier_type"].lower() in ["hugo gene name", "hgnc approved symbol", "hugo gene name id", "hugo gene name identifier", "hgnc symbol", "hgnc gene symbol"]:
            
            if ident["taxon"] is not None:
                proc_taxon = ident["taxon"].lower().replace(" ", "_")

                base = "http://apprisws.bioinfo.cnio.es:80/rest/"
                ext = "exporter/name/" + proc_taxon + "/" + str(ident["identifier"]) + "?format=json"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = json.loads(r.text)

                ensembl_pattern = re.compile("ENS([GT]|MUST|RNOT|DART)\d{11}|Y[A-Z]{2}\d{3}[A-Z](-[A-Z])?|FBtr\d{7}|Q\d{4}|((([0-9]?[A-Z]{1,4}\d{1,3})[A-Z0-9]?)|(cTel\d{2}X)|([0-9]RSSE)|(Y[0-9]{1,3}[A-Z]\d{1,2}((LA|UA)|[A-C][A-Z]?)))*(\.\d{1,4}[a-z]?)+")
                refseq_pattern = re.compile("(N|X)(M|R)_(\d{6}|\d{9})")

                for x in decoded:
                    if "transcript_name" in x:
                        if x["transcript_name"] not in trans_id_array and x["transcript_id"] not in trans_id_array:
                            if ensembl_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            elif refseq_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            else:
                                continue
                    elif "transcript_id" in x:
                        if x["transcript_id"] not in trans_id_array:
                            if ensembl_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS")
                                trans_array.append(temp_trans)
                                trans_id_array.append(temp_trans)
                            elif refseq_pattern.match(x["transcript_id"]):
                                temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                trans_array.append(temp_trans)
                                trans_id_array.append(x["transcript_id"])
                                trans_id_array.append(x["transcript_name"])
                            else:
                                continue
                    else:
                        continue
                        
        elif ident["identifier_type"].lower() in ["entrez", "entrez gene", "entrez geneid", "entrez gene id", "entrez gene identifier", "ncbi", "ncbi entrez", "ncbi entrez gene", "ncbi entrez geneid", "ncbi entrez gene id", "ncbi entrez gene identifier", "ncbi gene", "ncbi geneid", "ncbi gene id", "ncbi gene identifier", "ncbi-geneid", "entrez id", "entrez identifier", "ncbi id", "ncbi identifier"]:
            for ensembl_gene in gnomics.objects.gene.Gene.ensembl_gene_id(gene):
        
                if ident["taxon"] is not None:
                    proc_taxon = ident["taxon"].lower().replace(" ", "_")

                    base = "http://apprisws.bioinfo.cnio.es:80/rest/"
                    ext = "exporter/id/" + proc_taxon + "/" + ensembl_gene + "?format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})

                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()

                    decoded = json.loads(r.text)

                    ensembl_pattern = re.compile("ENS([GT]|MUST|RNOT|DART)\d{11}|Y[A-Z]{2}\d{3}[A-Z](-[A-Z])?|FBtr\d{7}|Q\d{4}|((([0-9]?[A-Z]{1,4}\d{1,3})[A-Z0-9]?)|(cTel\d{2}X)|([0-9]RSSE)|(Y[0-9]{1,3}[A-Z]\d{1,2}((LA|UA)|[A-C][A-Z]?)))*(\.\d{1,4}[a-z]?)+")
                    refseq_pattern = re.compile("(N|X)(M|R)_(\d{6}|\d{9})")

                    for x in decoded:
                        if "transcript_name" in x:
                            if x["transcript_name"] not in trans_id_array and x["transcript_id"] not in trans_id_array:
                                if ensembl_pattern.match(x["transcript_id"]):
                                    temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS", name = x["transcript_name"])
                                    trans_array.append(temp_trans)
                                    trans_id_array.append(x["transcript_id"])
                                    trans_id_array.append(x["transcript_name"])
                                elif refseq_pattern.match(x["transcript_id"]):
                                    temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                    trans_array.append(temp_trans)
                                    trans_id_array.append(x["transcript_id"])
                                    trans_id_array.append(x["transcript_name"])
                                else:
                                    print(x["transcript_id"])
                        elif "transcript_id" in x:
                            if x["transcript_id"] not in trans_id_array:
                                if ensembl_pattern.match(x["transcript_id"]):
                                    temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "Ensembl Transcript ID", source = "APPRIS")
                                    trans_array.append(temp_trans)
                                    trans_id_array.append(temp_trans)
                                elif refseq_pattern.match(x["transcript_id"]):
                                    temp_trans = gnomics.objects.transcript.Transcript(identifier = x["transcript_id"], identifier_type = "RefSeq RNA ID", source = "APPRIS", name = x["transcript_name"])
                                    trans_array.append(temp_trans)
                                    trans_id_array.append(x["transcript_id"])
                                    trans_id_array.append(x["transcript_name"])
                                else:
                                    print(x["transcript_id"])
                        else:
                            print(x)
        
    return trans_array
        
#   UNIT TESTS
def gene_transcript_unit_tests(wikidata_accession, ensembl_gene_id, hgnc_symbol):
    hgnc_gene = gnomics.objects.gene.Gene(identifier = hgnc_symbol, identifier_type = "HGNC Approved Symbol", language = None, taxon = "Homo sapiens", source = "APPRIS")
    print("\nGetting transcripts from HGNC Gene Symbol (%s):" % hgnc_symbol)
    start = timeit.timeit()
    all_trans = get_transcripts(hgnc_gene)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for trans in all_trans:
        for iden in trans.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
    wikidata_gene = gnomics.objects.gene.Gene(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, taxon = "Homo sapiens", source = "Wikidata")
    print("Getting transcripts from Wikidata Accession (%s):" % wikidata_accession)
    for trans in get_transcripts(wikidata_gene):
        for iden in trans.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "APPRIS")
    print("\nGetting transcripts from Ensembl Gene ID (%s):" % ensembl_gene_id)
    for trans in get_transcripts(ensembl_gene):
        for iden in trans.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()