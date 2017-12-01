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
import requests

#   MAIN
def main():
    gene_transcript_unit_tests("Q227339")

# Get transcripts.
def get_transcripts(gene):
    trans_array = []
    trans_dict = {}
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
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
                            temp_transcript = gnomics.objects.transcript.Transcript(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "RefSeq RNA ID", source = "Wikidata")
                            trans_array.append(temp_transcript)
                    elif en_prop_name.lower() == "ensembl transcript id":
                        for x in prop_dict:
                            temp_transcript = gnomics.objects.transcript.Transcript(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "Ensembl Transcript ID", source = "Wikidata")
                            trans_array.append(temp_transcript)
    return trans_array
        
#   UNIT TESTS
def gene_transcript_unit_tests(wikidata_accession):
    wikidata_gene = gnomics.objects.gene.Gene(identifier = wikidata_accession, identifier_type = "Wikidata Accession", language = None, taxon = "Homo sapiens", source = "Wikidata")
    print("Getting transcripts from Wikidata Accession (%s):" % wikidata_accession)
    for trans in get_transcripts(wikidata_gene):
        for iden in trans.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()