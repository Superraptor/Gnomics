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
#   Get GO accession.
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
import gnomics.objects.auxiliary_files.identifier
import gnomics.objects.biological_process

#   Other imports.
from bioservices import QuickGO
import re
import timeit

#   MAIN
def main():
    go_unit_tests("GO_0061621")

#   Get QuickGO object.
def get_quickgo_obj(biological_process):
    quickgo_array = []
    
    for obj in biological_process.biological_process_objects:
        if obj["object_type"] in ["quickgo", "quick go", "quickgo object", "quick go object"]:
            quickgo_array.append(obj["object"])
            
    if quickgo_array:
        return quickgo_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(biological_process.identifiers, ["go accession", "go acc", "go id", "go identifier"]):
        
        new_id = iden["identifier"]
        if "_" in new_id:
            new_id = new_id.replace("_", ":")
        
        s = QuickGO(verbose=False)
        
        # Changed from the standard URL; see here:
        # https://github.com/cokelaer/bioservices/issues/94
        s.url = "http://www.ebi.ac.uk/QuickGO-Old"
        
        res = s.Term(new_id, frmt="obo")
        
        go_term = re.findall(r'name: ([^\n]+)\n', res)
        go_definition = re.findall(r'def: "([^\n]+)"\n', res)
        synonyms = re.findall(r'synonym: "([^\n]+)" ', res)
        interpro_xrefs = re.findall(r'xref: InterPro:([^\n]+)\n', res)
        metacyc_xrefs = re.findall(r'xref: MetaCyc:([^\n]+)\n', res)
        nif_xrefs = re.findall(r'xref: NIF_Subcellular:([^\n]+)\n', res)
        uniprotkb_kw_xrefs = re.findall(r'xref: UniProtKB-KW:([^\n]+)\n', res)
        uniprotkb_subcell_xrefs = re.findall(r'xref: UniProtKB-SubCell:([^\n]+)\n', res)
        wikipedia_xrefs = re.findall(r'xref: Wikipedia:([^\n]+)\n', res)
        categories = re.findall(r'is_a: ([^\n]+) ! ', res)
        
        temp_obj = {
            "go_term": go_term[0],
            "definition": go_definition[0],
            "synonyms": synonyms,
            "interpro": interpro_xrefs,
            "metacyc": metacyc_xrefs,
            "nif_subcellular": nif_xrefs,
            "uniprotkb-kw": uniprotkb_kw_xrefs,
            "uniprotkb-subcell": uniprotkb_subcell_xrefs,
            "wikipedia": wikipedia_xrefs,
            "is_a": categories
        }
        gnomics.objects.biological_process.BiologicalProcess.add_object(biological_process, obj=temp_obj, object_type="QuickGO Object")
        
        quickgo_array.append(temp_obj)
        
    return quickgo_array

#   Get GO accession.
def get_go_accession(bio, user = None):
    go_array = []
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(bio.identifiers, ["go accession", "go acc", "go id", "go identifier"]):
        if iden["identifier"] not in go_array:
            go_array.append(iden["identifier"])
    return go_array

#   UNIT TESTS
def go_unit_tests(go_acc):
    bio_proc = gnomics.objects.biological_process.BiologicalProcess(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ontology Lookup Service")
    get_quickgo_obj(bio_proc)

#   MAIN
if __name__ == "__main__": main()