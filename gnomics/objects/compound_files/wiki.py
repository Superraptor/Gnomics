#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#       WIKIDATA
#           https://pypi.python.org/pypi/Wikidata
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

#   MAIN
def main():
    wiki_unit_tests("CHEBI:4911", "C01576", "36462")

#   Get Wikipedia accession.
def get_english_wikipedia_accession(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "wikipedia accession":
                    com.identifiers.append({
                        'identifier': accession._DatabaseAccession__accession_number,
                        'language': "en",
                        'identifier_type': "Wikipedia accession",
                        'source': "ChEBI"
                    })
                    return accession._DatabaseAccession__accession_number
            print("No mapping found between ChEBI ID and Wikipedia accession...")
            return ""
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com, user = user)
            return gnomics.objects.compound.Compound.wikipedia_accession(com, user = user)
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            gnomics.objects.compound.Compound.chebi_id(com, user = user)
            return gnomics.objects.compound.Compound.wikipedia_accession(com, user = user)

#   Get Wikidata accession.
def get_wikidata_accession(compound):
    for ident in compound.identifiers:
        if ident["identifier_type"].lower() == "wikidata accession" or ident["identifier_type"].lower() == "wikidata":
            return ident["identifier"]
    for ident in compound.identifiers:
        if ident["identifier_type"].lower() == "wikipedia accession" or ident["identifier_type"].lower() == "wikipedia":
            base = "https://en.wikipedia.org/w/api.php"
            ext = "?action=query&prop=pageprops&format=json&titles=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)      
            wikidata_id = decoded["query"]["pages"]["pageprops"]["wikibase_item"]
            gnomics.objects.compound.Compound.add_identifier(identifier = wikidata_id, identifier_type = "Wikidata Accession", language = None, source = "Wikipedia")
            return wikidata_id
            
#   Get Wikidata object.
def get_wikidata_object(compound):
    wikidata_obj_array = []
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'wikidata object' or com_obj['object_type'].lower() == 'wikidata':
                wikidata_obj_array.append(assay_obj['object'])
    if wikidata_obj_array:
        return wikidata_obj_array
    for wikidata_id in [get_wikidata_accession(compound)]:
        client = Client()
        print(wikidata_id)
        entity = client.get(wikidata_id, load=True)
        compound.compound_objects.append({
            'object': entity.attributes,
            'object_type': "Wikidata Object"
        })
        wikidata_obj_array.append(entity.attributes) 
    return wikidata_obj_array
        
#   UNIT TESTS
def wiki_unit_tests(chebi_id, kegg_compound_id, pubchem_cid):
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("Getting Wikipedia accession from ChEBI ID (%s):" % chebi_id)
    print("- " + get_english_wikipedia_accession(chebi_com) + "\n")
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("Getting Wikipedia accession from KEGG Compound ID (%s):" % kegg_compound_id)
    print("- " + get_english_wikipedia_accession(kegg_compound_com) + "\n")
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting Wikipedia accession from PubChem CID (%s):" % pubchem_cid)
    print("- " + get_english_wikipedia_accession(pubchem_com) + "\n")

#   MAIN
if __name__ == "__main__": main()