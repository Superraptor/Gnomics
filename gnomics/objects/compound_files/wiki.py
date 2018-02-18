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
#       WIKIPEDIA
#           https://pypi.python.org/pypi/wikipedia
#

#
#   Get Wikipedia information.
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

#   Other imports.
from wikidata.client import Client
import pubchempy as pubchem
import timeit

#   MAIN
def main():
    wiki_unit_tests("CHEBI:4911", "C01576", "36462")

#   Get Wikipedia accession.
def get_english_wikipedia_accession(com, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in wiki_array and iden["language"] == "en":
            wiki_array.append(iden["identifier"])
            
    if wiki_array:
        return wiki_array
    
    ids_completed = []
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "wikipedia accession" and accession._DatabaseAccession__accession_number not in wiki_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, language = "en", identifier_type = "Wikipedia Accession", source = "ChEBI")
                        wiki_array.append(accession._DatabaseAccession__accession_number)
        
    if wiki_array:
        return wiki_array
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com, user = user)
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "wikipedia accession" and accession._DatabaseAccession__accession_number not in wiki_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, language = "en", identifier_type = "Wikipedia Accession", source = "ChEBI")
                        wiki_array.append(accession._DatabaseAccession__accession_number)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com, user = user)
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                db_accessions = sub_com.get_database_accessions()
                for accession in db_accessions:
                    if accession._DatabaseAccession__typ.lower() == "wikipedia accession" and accession._DatabaseAccession__accession_number not in wiki_array:
                        gnomics.objects.compound.Compound.add_identifier(com, identifier = accession._DatabaseAccession__accession_number, language = "en", identifier_type = "Wikipedia Accession", source = "ChEBI")
                        wiki_array.append(accession._DatabaseAccession__accession_number)
    
    return wiki_array

#   Get Wikidata accession.
def get_wikidata_accession(com, user=None):
    wiki_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in wiki_array:
            wiki_array.append(iden["identifier"])
        
    if wiki_array:
        return wiki_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
        
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]

            r = requests.get(base+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                print("There was a problem accessing the Wikipedia API")
            else:
                decoded = json.loads(r.text)      
                wikidata_id = decoded["query"]["pages"]["pageprops"]["wikibase_item"]
                gnomics.objects.compound.Compound.add_identifier(identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
                wiki_array.append(wikidata_id)
        
    return wiki_array
            
#   Get Wikidata object.
def get_wikidata_object(compound, user=None):
    wikidata_obj_array = []
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['wikidata object', 'wikidata']:
                wikidata_obj_array.append(assay_obj['object'])
    
    if wikidata_obj_array:
        return wikidata_obj_array
    
    for wikidata_id in get_wikidata_accession(compound):
        client = Client()
        entity = client.get(wikidata_id, load=True)
        gnomics.objects.compound.Compound.add_object(compound, obj=entity.attributes, object_type="Wikidata Object")
        wikidata_obj_array.append(entity.attributes)
        
    return wikidata_obj_array
        
#   UNIT TESTS
def wiki_unit_tests(chebi_id, kegg_compound_id, pubchem_cid):
    
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting Wikipedia accession from ChEBI ID (%s):" % chebi_id)
    start = timeit.timeit()
    wiki_array = get_english_wikipedia_accession(chebi_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in wiki_array:
        print("\t- %s" % str(com))
    
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting Wikipedia accession from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    wiki_array = get_english_wikipedia_accession(kegg_compound_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in wiki_array:
        print("\t- %s" % str(com))
    
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting Wikipedia accession from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    wiki_array = get_english_wikipedia_accession(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in wiki_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()