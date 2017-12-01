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
#   Get PubChem CIDs and PubChem SIDs.
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
import pubchempy as pubchem
import json
import requests

#   MAIN
def main():
    cid_unit_tests("33510", "C01576", "Q418817", "")
    sids_unit_tests("6918092")
    
# Returns PubChem compound from CID.
def get_pubchem_compound(compound, user = None):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'pubchem compound' or com_obj['object_type'].lower() == 'pubchem':
                return com_obj['object']
    pubchem_compound = pubchem.Compound.from_cid(gnomics.objects.compound.Compound.pubchem_cid(compound, user = user))
    compound.compound_objects.append({
        'object': pubchem_compound,
        'object_type': "PubChem compound"
    })
    return pubchem_compound

#   Get CID.
def get_cids(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            results = pubchem.get_compounds(gnomics.objects.compound.Compound.inchi(com, user = user), 'inchi')
            com.identifiers.append({
                'identifier': results[0].cid,
                'language': None,
                'identifier_type': "CID",
                'source': "PubChem"
            })
            return str(results[0].cid)
        elif ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            # Returns SID.
            pubchem_sid = str(gnomics.objects.compound.Compound.kegg_compound_db_entry(com)["DBLINKS"]["PubChem"])
            # Get CIDs from SIDs.
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/substance/sid/" + str(pubchem_sid) + "/JSONP"
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
            com_array = []
            for temp_com in decoded["PC_Substances"][0]["compound"]:
                if "id" in temp_com:
                    if temp_com["id"]["type"] == 1 and "id" in temp_com["id"]:
                        if "cid" in temp_com["id"]["id"]:
                            com_array.append(temp_com["id"]["id"]["cid"])
            return com_array
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
        elif ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.compound.Compound.wikidata(com):
                com_array = []
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "pubchem cid":
                        for x in prop_dict:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "CAS Registry Number", language = None, source = "Wikidata")
                            com_array.append(x["mainsnak"]["datavalue"]["value"])
                return com_array
            
#   Get SIDs.
def get_sids(com, user = None):
    sid_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "sid":
            sid_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            sid_array_from_pubchem = gnomics.objects.compound.Compound.pubchem_compound(com).sids
            for sid in sid_array_from_pubchem:
                if sid not in sid_array:
                    com.identifiers.append(
                        {
                            'identifier': sid,
                            'language': None,
                            'identifier_type': "PubChem SID",
                            'source': "PubChem"
                        }
                    )
                    sid_array.append(sid)
    return sid_array

#   UNIT TESTS
def cid_unit_tests(chemspider_id, kegg_compound_id, wikidata_accession, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("\nCreating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting PubChem CID from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_cids(chemspider_com, user = user))
        kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting PubChem CID from KEGG Compound ID (%s):" % kegg_compound_id)
        for com in get_cids(kegg_com, user = user):
            print("- %s" % str(com))
        wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
        print("\nGetting PubChem CID from Wikidata Accession (%s):" % wikidata_accession)
        for com in get_cids(wikidata_com):
            print("- " + str(com))
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with KEGG Compound conversion...\n")
        kegg_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("Getting PubChem CID from KEGG Compund ID (%s):" % kegg_compound_id)
        for com in get_cids(kegg_com, user = user):
            print("- %s" % str(com))
            
def sids_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting PubChem SIDs from PubChem CID (%s):" % pubchem_cid)
    for com in get_sids(pubchem_com):
        print("- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()