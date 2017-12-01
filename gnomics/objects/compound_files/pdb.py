#
#
#
#
#

#
#   IMPORT SOURCES:
#

#
#   Get PBD Ligand ID.
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
import gnomics.objects.compound

#   Other imports.
import linecache
import json
import requests

#   MAIN
def main():
    pdb_unit_tests("Q418817")

#   Get PDB Ligand ID.
def get_pdb_ligand_id(com):
    pdb_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pdb ligand" or ident["identifier_type"].lower() == "pdb ligand id" or ident["identifier_type"].lower() == "pdb ligand identifier":
            pdb_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.compound.Compound.wikidata(com):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "pdb ligand id":
                        for x in prop_dict:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "PDB Ligand ID", language = None, source = "Wikidata")
                            pdb_array.append(x["mainsnak"]["datavalue"]["value"])
    return pdb_array

#   UNIT TESTS
def pdb_unit_tests(wikidata_accession):
    wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
    print("Getting PDB Ligand IDs from Wikidata Accession (%s):" % wikidata_accession)
    for pdb in get_pdb_ligand_id(wikidata_com):
        print("- " + str(pdb))

#   MAIN
if __name__ == "__main__": main()