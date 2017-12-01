#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       CHEMOPY
#           https://www.researchgate.net/publication/235919352_UserGuide_for_chemopy
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get ChEBI identifier.
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
from bioservices import *
from libchebipy import ChebiEntity, ChebiException, Comment, CompoundOrigin, DatabaseAccession, Formula, Name, Reference, Relation, Structure
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    chebi_unit_tests("C01576", "6918092")
    
# Get ChEBI entity.
def get_chebi_entity(compound, user = None):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'chebi entity' or com_obj['object_type'].lower() == 'chebi':
                return com_obj['object']
    chebi_object = ChebiEntity(gnomics.objects.compound.Compound.chebi_id(compound, user = user))
    compound.compound_objects.append(
        {
            'object': chebi_object,
            'object_type': "ChEBI entity"
        }
    )
    return chebi_object

#   Get ChEBI ID.
def get_chebi_id(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            return ident["identifier"].upper()
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            kegg = KEGG(verbose = False)
            map_kegg_chebi = kegg.conv("chebi", "compound")
            com.identifiers.append(
                {
                    'identifier': map_kegg_chebi["cpd:" + ident["identifier"]].upper(),
                    'language': None,
                    'identifier_type': "ChEBI",
                    'source': "KEGG"
                }
            )
            return map_kegg_chebi["cpd:" + ident["identifier"]].upper()
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com)) + "/xrefs/RegistryID/JSONP"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            str_r = r.text
            try:
                l_index = str_r.index("(") + 1
                r_index = str_r.index(")")
            except ValueError:
                print("Input is not in a JSONP format.")
                exit()
            res = str_r[l_index:r_index]
            decoded = json.loads(res)
            for xref in decoded["InformationList"]["Information"][0]["RegistryID"]:
                split_xref = xref.split(":")
                if split_xref[0] == "CHEBI":
                    com.identifiers.append(
                        {
                            'identifier': xref,
                            'language': None,
                            'identifier_type': "ChEBI",
                            'source': "PubChem"
                        }
                    )
                    return xref

#   UNIT TESTS
def chebi_unit_tests(kegg_compound_id, pubchem_cid):
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting ChEBI ID from KEGG Compound ID (%s):" % kegg_compound_id)
    print("- %s\n" % str(get_chebi_id(kegg_compound_com)))
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting ChEBI ID from PubChem CID (%s):" % pubchem_cid)
    print("- " + get_chebi_id(pubchem_com) + "\n")

#   MAIN
if __name__ == "__main__": main()