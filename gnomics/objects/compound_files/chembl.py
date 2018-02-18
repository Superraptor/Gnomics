#!/usr/bin/env python

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
import timeit

#   MAIN
def main():
    chembl_unit_tests("C01576", "6918092")
    
# Returns ChEMBL molecule.
def get_chembl_molecule(compound, user=None):
    for com_obj in compound.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ['chembl molecule', 'chembl', 'chembl object']:
                return com_obj['object']
            
    for chembl_id in get_chembl_id(compound, user=user):
        molecule = new_client.molecule
        chembl_molecule = molecule.get([chembl_id])
        gnomics.objects.compound.Compound.add_object(compound, obj = chembl_molecule, object_type = "ChEMBL Molecule")
    
    return chembl_molecule

#   Get ChEMBL ID.
def get_chembl_id(com, user=None):
    chembl_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl compound", "chembl compound id", "chembl compound identifier"]):
        if iden["identifier"] not in chembl_array:
            chembl_array.append(iden["identifier"])
            
    if chembl_array:
        return chembl_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            uni = UniChem()
            
            # Other mappings that can be done here:
            # ibm, drugbank, nih_ncc, atlas, chebi, surechem,
            # pubchem_dotf, pubchem, chembl, pdb, pharmgkb,
            # hmdb, mcule, zinc, sellect, iuphar, fdasrc, 
            # patents, pubchem_tpharma, emolecules
            mapping = uni.get_mapping("kegg_ligand", "chembl")
            
            gnomics.objects.compound.Compound.add_identifier(com, identifier = mapping[iden["identifier"]], language = None, identifier_type = "ChEMBL", source = "KEGG")
            
            chembl_array.append(mapping[iden["identifier"]])
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        for cid in gnomics.objects.compound.Compound.pubchem_cid(com, user=user):
            if iden["identifier"] not in ids_completed:
                ids_completed.append(iden["identifier"])

                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/compound/cid/" + str(cid) + "/xrefs/RegistryID/JSONP"

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    print("Something went wrong while trying to attain a PubChem PUG REST connection...")
                else:
                    str_r = r.text
                    try:
                        l_index = str_r.index("(") + 1
                        r_index = str_r.index(")")
                        res = str_r[l_index:r_index]
                        decoded = json.loads(res)

                        for xref in decoded["InformationList"]["Information"][0]["RegistryID"]:
                            if "CHEMBL" in xref and xref not in chembl_array and "SCHEMBL" not in xref:
                                gnomics.objects.compound.Compound.add_identifier(com, identifier = xref, language = None, identifier_type = "ChEMBL", source = "PubChem")

                                chembl_array.append(xref)

                    except ValueError:
                        print("Input is not in a JSONP format.")

    return chembl_array            

#   UNIT TESTS
def chembl_unit_tests(kegg_compound_id, pubchem_cid):
    kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
    print("\nGetting ChEMBL ID from KEGG Compound ID (%s):" % kegg_compound_id)
    start = timeit.timeit()
    chembl_array = get_chembl_id(kegg_compound_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in chembl_array:
        print("\t- %s" % str(com))
    
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("\nGetting ChEMBL ID from PubChem CID (%s):" % pubchem_cid)
    start = timeit.timeit()
    chembl_array = get_chembl_id(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for com in chembl_array:
        print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()