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
#   Get Ensembl transcript.
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
import gnomics.objects.transcript

#   Other imports.
import requests
import timeit

#   MAIN
def main():
    ensembl_unit_tests("NM_001014431.1")
    
# Returns Ensembl object.
def get_ensembl_transcript(transcript):
    ensembl_obj_array = []
    
    for trans_obj in transcript.transcript_objects:
        if trans_obj["object_type"].lower() in ["ensembl", "ensembl transcript", "ensembl object", "ensembl transcript object"]:
            ensembl_obj_array.append(trans_obj["object"])
    
    if ensembl_obj_array:
        return ensembl_obj_array
    
    for ensembl_id in get_ensembl_transcript_id(transcript):
        server = "https://rest.ensembl.org"
        ext = "/lookup/id/" + str(ensembl_id) + "?expand=1"
        r = requests.get(server+ext, headers={"Content-Type": "application/json"})
        
        if not r.ok:
            print("Something went wrong.")
            
        else:
            decoded = r.json()

            new_ensembl_obj = {
                'source': decoded["source"],
                'object_type': decoded["object_type"],
                'logic_name': decoded["logic_name"],
                'seq_region_name': decoded["seq_region_name"],
                'db_type': decoded["db_type"],
                'is_canonical': decoded["is_canonical"],
                'strand': decoded["strand"],
                'id': decoded["id"],
                'version': decoded["version"],
                'species': decoded["species"],
                'assembly_name': decoded["assembly_name"],
                'display_name': decoded["display_name"],
                'end': decoded["end"],
                'biotype': decoded["biotype"],
                'start': decoded["start"]
            }

            temp_ensembl_obj = {
                'object': new_ensembl_obj,
                'object_type': "Ensembl Transcript"
            }
            gnomics.objects.transcript.Transcript.add_object(transcript, obj = new_ensembl_obj, object_type = "Ensembl Transcript")
            ensembl_obj_array.append(new_ensembl_obj)
        
    return ensembl_obj_array

# Returns Ensembl transcript identifier.
def get_ensembl_transcript_id(transcript):
    ensembl_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["ensembl", "ensembl id", "ensembl identifier", "ensembl transcript", "ensembl transcript id", "ensembl transcript identifier"]):
        if iden["identifier"] not in ensembl_array:
            ensembl_array.append(iden["identifier"])
    
    if ensembl_array:
        return ensembl_array

    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(transcript.identifiers, ["refseq", "refseq id", "refseq identifier", "refseq rna id", "refseq rna identifier", "refseq rna", "refseq accession", "refseq rna accession", "refseq mrna", "refseq mrna id", "refseq mrna identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            server = "https://rest.ensembl.org"
            ext = "/xrefs/symbol/" + str(iden["taxon"]).lower().replace(" ", "_") + "/" + str(iden["identifier"]) + "?expand=1"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                print("Something went wrong.")

            else:
                decoded = r.json()
                for result in decoded:
                    if result["type"] == "transcript":
                        if result["id"] not in ensembl_array:
                            ensembl_array.append(result["id"])
                            gnomics.objects.transcript.Transcript.add_identifier(transcript, identifier=result["id"], identifier_type="Ensembl Transcript ID", language=None, source="Ensembl")
                            
    return ensembl_array
        
#   UNIT TESTS
def ensembl_unit_tests(refseq_id):
    refseq_trans = gnomics.objects.transcript.Transcript(identifier = str(refseq_id), identifier_type = "RefSeq mRNA ID", source = "Entrez", taxon="Homo sapiens")
    print("Getting Ensembl Transcript ID from RefSeq mRNA ID (%s):" % refseq_id)
    start = timeit.timeit()
    all_ensembl = get_ensembl_transcript_id(refseq_trans)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for iden in all_ensembl:
        print("- %s" % str(iden))

#   MAIN
if __name__ == "__main__": main()