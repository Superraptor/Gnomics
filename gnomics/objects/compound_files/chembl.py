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
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get ChEMBL identifier.
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
from chembl_webresource_client.new_client import new_client
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    chembl_unit_tests("C01576", "6918092")
    
# Returns ChEMBL molecule.
def get_chembl_molecule(compound, user = None):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'chembl molecule' or com_obj['object_type'].lower() == 'chembl':
                return com_obj['object']
    molecule = new_client.molecule
    chembl_molecule = molecule.get([gnomics.objects.compound.Compound.chembl_id(compound, user = user)])
    compound.compound_objects.append(
        {
            'object': chembl_molecule,
            'object_type': "ChEMBL molecule"
        }
    )
    return chembl_molecule

#   Get ChEMBL ID.
def get_chembl_id(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            uni = UniChem()
            # Other mappings that can be done here:
            # ibm, drugbank, nih_ncc, atlas, chebi, surechem,
            # pubchem_dotf, pubchem, chembl, pdb, pharmgkb,
            # hmdb, mcule, zinc, sellect, iuphar, fdasrc, 
            # patents, pubchem_tpharma, emolecules
            mapping = uni.get_mapping("kegg_ligand", "chembl")
            com.identifiers.append(
                {
                    'identifier': mapping[ident["identifier"]],
                    'language': None,
                    'identifier_type': "ChEMBL",
                    'source': "KEGG"
                }
            )
            return mapping[ident["identifier"]]
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com, user = user)) + "/xrefs/RegistryID/JSONP"
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
                if "CHEMBL" in xref:
                    com.identifiers.append(
                        {
                            'identifier': xref,
                            'language': None,
                            'identifier_type': "ChEMBL",
                            'source': "PubChem"
                        }
                    )
                    return xref

#   UNIT TESTS
def chembl_unit_tests(kegg_compound_id, pubchem_cid):
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("Getting ChEMBL ID from KEGG Compound ID (%s):" % kegg_compound_id)
    print("- " + get_chembl_id(kegg_compound_com) + "\n")
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting ChEMBL ID from PubChem CID (%s):" % pubchem_cid)
    print("- " + get_chembl_id(pubchem_com) + "\n")

#   MAIN
if __name__ == "__main__": main()