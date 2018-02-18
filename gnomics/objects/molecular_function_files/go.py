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
#   Get GO data for molecular functions.
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
import gnomics.objects.molecular_function

#   Other imports.
from bioservices import QuickGO
import json
import re
import requests

#   MAIN
def main():
    go_unit_tests("GO:0003824", "K15406")
    
#   Get QuickGO object.
def get_quickgo_obj(molecular_function):
    quickgo_array = []
    
    for obj in molecular_function.molecular_function_objects:
        if obj["object_type"] in ["quickgo", "quick go", "quickgo object", "quick go object"]:
            quickgo_array.append(obj["object"])
            
    if quickgo_array:
        return quickgo_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(molecular_function.identifiers, ["go accession", "go acc", "go id", "go identifier"]):
        
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
        gnomics.objects.molecular_function.MolecularFunction.add_object(molecular_function, obj=temp_obj, object_type="QuickGO Object")
        
        quickgo_array.append(temp_obj)
        
    return quickgo_array

#   Get GO Accession.
def get_go_accession(molec, user=None):

    molec_array = []
    for ident in molec.identifiers:
        if ident["identifier_type"].lower() in ["go acc", "go accession", "go id", "go identifier"]:
            molec_array.append(ident["identifier"])

    if molec_array:
        return molec_array

    for ident in molec.identifiers:
        if ident["identifier_type"] is not None:
            if ident["identifier_type"].lower() in ["kegg orthology", "kegg ko", "kegg orthology id", "kegg orthology identifier", "kegg ko id", "kegg ko identifier"]:
                for kegg_obj in gnomics.objects.molecular_function.MolecularFunction.kegg_orthology(molec):
                    if "DBLINKS" in kegg_obj:
                        if "GO" in kegg_obj["DBLINKS"]:
                            for temp_go in kegg_obj["DBLINKS"]["GO"].split(" "):
                                temp_go_id = "GO:"+str(temp_go)
                                
                                server = "https://rest.ensembl.org"
                                ext = "/ontology/id/" + temp_go_id + "?"
                                r = requests.get(server + ext, headers = {
                                    "Content-Type" : "application/json"
                                })

                                if not r.ok:
                                    print("Something went wrong.")
                                else:
                                    
                                    decoded = r.json()
                                    
                                    if decoded["namespace"] == "molecular_function":
                                        go_acc = decoded["accession"]
                                        go_name = decoded["name"]
                                        gnomics.objects.molecular_function.MolecularFunction.add_identifier(molec, identifier=go_acc, identifier_type="GO Accession", language=None, source="Ensembl", name=go_name)
                                        
                                        molec_array.append(go_acc)
                                    
    return molec_array

#   UNIT TESTS
def go_unit_tests(go_acc, kegg_orthology_id):
    molec_ftn = gnomics.objects.molecular_function.MolecularFunction(identifier=go_acc, identifier_type="GO Accession", language=None, source="Ontology Lookup Service")
    print(get_quickgo_obj(molec_ftn))
    
    kegg_orthology = gnomics.objects.molecular_function.MolecularFunction(identifier = kegg_orthology_id, identifier_type = "KEGG ORTHOLOGY ID", source = "KEGG")
    print("\nGetting GO Accession from KEGG ORTHOLOGY ID (%s):" % kegg_orthology_id)
    for iden in get_go_accession(kegg_orthology):
        print("- %s" % str(iden))

#   MAIN
if __name__ == "__main__": main()