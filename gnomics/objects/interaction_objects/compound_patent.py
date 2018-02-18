#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get patent accession.
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
import gnomics.objects.compound
import gnomics.objects.patent

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    patent_unit_tests("CHEBI:4911", "6918092", "127378063", "C01576")

#   Get Patents.
def get_patents(com):
    patent_array = []
    patent_obj_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["chebi", "chebi id"]:
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "patent accession" and accession._DatabaseAccession__accession_number not in patent_array:
                    temp_patent = gnomics.objects.patent.Patent(identifier=accession._DatabaseAccession__accession_number, language=None, identifier_type="Patent accession", source="ChEBI")
                    patent_obj_array.append(temp_patent)
                    patent_array.append(accession._DatabaseAccession__accession_number)
                    
        elif ident["identifier_type"].lower() in ["pubchem sid", "pubchem substance"]:
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/substance/sid/" + str(ident["identifier"]) + "/xrefs/PatentID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rindex(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for result in decoded["InformationList"]["Information"]:
                patents = result["PatentID"]
                for patent in patents:
                    if patent not in patent_array:
                        
                        temp_patent = gnomics.objects.patent.Patent(identifier=patent, language=None, identifier_type="Patent ID", source="PubChem")
                        patent_obj_array.append(temp_patent)
                        
                        patent_array.append(patent)

        elif ident["identifier_type"].lower() in ["pubchem cid", "cid"]:
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(ident["identifier"]) + "/xrefs/PatentID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.rindex(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for result in decoded["InformationList"]["Information"]:
                patents = result["PatentID"]
                for patent in patents:
                    if patent not in patent_array:
                        
                        temp_patent = gnomics.objects.patent.Patent(identifier=patent, language=None, identifier_type="Patent ID", source="PubChem")
                        patent_obj_array.append(temp_patent)
                        
                        patent_array.append(patent)
                
    if patent_array:
        return patent_obj_array
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["kegg compound", "kegg compound id", "kegg compound accession"]:
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_patents(com)
    

#   UNIT TESTS
def patent_unit_tests(chebi_id, pubchem_cid, pubchem_sid, kegg_compound_id):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting patent accessions from ChEBI ID (%s):" % chebi_id)
    for acc in get_patents(chebi_com):
        for iden in acc.identifiers:
            print("- %s" % str(iden["identifier"]))
        
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting patent accessions from PubChem CID (%s):" % pubchem_cid)
    for acc in get_patents(pubchem_com):
        for iden in acc.identifiers:
            print("- %s" % str(iden["identifier"]))
        
    pubchem_sub = gnomics.objects.compound.Compound(identifier = str(pubchem_sid), identifier_type = "PubChem SID", source = "PubChem")
    print("\nGetting patent accessions from PubChem SID (%s):" % pubchem_sid)
    for acc in get_patents(pubchem_sub):
        for iden in acc.identifiers:
            print("- %s" % str(iden["identifier"]))
        
    kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting patent accessions from KEGG Compound ID (%s):" % kegg_compound_id)
    
    start = timeit.timeit()
    all_patents = get_patents(kegg_com)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for acc in all_patents:
        for iden in acc.identifiers:
            print("- %s" % str(iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()