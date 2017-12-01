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
#   Get transcripts from protein.
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
import gnomics.objects.protein
import gnomics.objects.transcript

#   Other imports.
import json
import requests
import urllib.error
import urllib.parse
import urllib.request

#   MAIN
def main():
    protein_transcript_unit_tests("Q13907", "IDI1_HUMAN")
    
#   Get transcripts.
def get_transcripts(prot):
    transcript_id_array = []
    transcript_obj_array = []
    for ident in prot.identifiers:
        if ident["identifier_type"].lower() == "uniprotkb id" or ident["identifier_type"].lower() == "uniprotkb identifier" or ident["identifier_type"].lower() == "uniprot id" or ident["identifier_type"].lower() == "uniprot identifier":
            # Ensembl Transcript
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ID",
                "to": "ENSEMBL_TRS_ID",
                "format": "tab",
                "query": ident["identifier"],
            }
            data = urllib.parse.urlencode(params)
            data = data.encode("utf-8")
            request = urllib.request.Request(url, data)
            contact = ""
            request.add_header("User-Agent", "Python %s" % contact)
            response = urllib.request.urlopen(request)
            page = response.read(200000).decode("utf-8")
            newline_sp = page.split("\n")
            id_from = newline_sp[0].split("\t")[0].strip()
            id_to = newline_sp[0].split("\t")[1].strip()
            for counter, line in enumerate(newline_sp):
                if (counter > 0) and (len(newline_sp[1].split("\t")) > 1):
                    orig_id = newline_sp[1].split("\t")[0].strip()
                    new_id = newline_sp[1].split("\t")[1].strip()
                    if new_id not in transcript_id_array:
                        transcript_id_array.append(new_id)
                        temp_transcript = gnomics.objects.transcript.Transcript(identifier = new_id, identifier_type = "Ensembl Transcript ID", source = "UniProt")
                        transcript_obj_array.append(temp_transcript)
        elif ident["identifier_type"].lower() == "uniprotkb ac" or ident["identifier_type"].lower() == "uniprotkb acc" or ident["identifier_type"].lower() == "uniprotkb accession" or ident["identifier_type"].lower() == "uniprot accession":
            # Ensembl Transcript
            url = "http://www.uniprot.org/uploadlists/"
            params = {
                "from": "ACC",
                "to": "ENSEMBL_TRS_ID",
                "format": "tab",
                "query": ident["identifier"],
            }
            data = urllib.parse.urlencode(params)
            data = data.encode("utf-8")
            request = urllib.request.Request(url, data)
            contact = ""
            request.add_header("User-Agent", "Python %s" % contact)
            response = urllib.request.urlopen(request)
            page = response.read(200000).decode("utf-8")
            newline_sp = page.split("\n")
            id_from = newline_sp[0].split("\t")[0].strip()
            id_to = newline_sp[0].split("\t")[1].strip()
            for counter, line in enumerate(newline_sp):
                if (counter > 0) and (len(newline_sp[1].split("\t")) > 1):
                    orig_id = newline_sp[1].split("\t")[0].strip()
                    new_id = newline_sp[1].split("\t")[1].strip()
                    if new_id not in transcript_id_array:
                        transcript_id_array.append(new_id)
                        temp_transcript = gnomics.objects.transcript.Transcript(identifier = new_id, identifier_type = "Ensembl Transcript ID", source = "UniProt")
                        transcript_obj_array.append(temp_transcript)
    return transcript_obj_array
    
#   UNIT TESTS
def protein_transcript_unit_tests(uniprot_kb_ac, uniprot_kb_id):
    uniprot_kb_ac_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_ac, language = None, identifier_type = "UniProt accession", source = "UniProt", taxon = "Homo sapiens")
    print("Getting drugs from UniProtKB accession (%s):" % uniprot_kb_ac)
    for obj in get_transcripts(uniprot_kb_ac_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    uniprot_kb_id_prot = gnomics.objects.protein.Protein(identifier = uniprot_kb_id, language = None, identifier_type = "UniProt identifier", source = "UniProt", taxon = "Homo sapiens")
    print("\nGetting drugs from UniProtKB identifier (%s):" % uniprot_kb_id)
    for obj in get_transcripts(uniprot_kb_id_prot):
        for iden in obj.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
#   MAIN
if __name__ == "__main__": main()