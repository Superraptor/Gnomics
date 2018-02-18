#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       CIRPY
#           http://cirpy.readthedocs.io/en/latest/index.html
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get SMILES.
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
import cirpy
import pubchempy as pubchem
import timeit

#   MAIN
def main():
    smiles_unit_tests("33510", "CHEBI:4911", "33419-42-0", "D00125", "6918092", "CHEMBL44657", "C01576", chemspider_security_token="")
	
#	Get SMILES.
def get_smiles(com, user=None):
    smiles_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["smiles"]):
        if iden["identifier"] not in smiles_array:
            smiles_array.append(iden["identifier"])

    if smiles_array:
        return smiles_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for cs_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                if cs_com.smiles not in smiles_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = cs_com.smiles, language = None, identifier_type = "SMILES", source = "ChemSpider")
                    smiles_array.append(cs_com.smiles)
        
        elif iden["identifier"] not in ids_completed and user is None:
            ids_completed.append(iden["identifier"])
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                if sub_com.get_smiles() not in smiles_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = sub_com.get_smiles(), language = None, identifier_type = "SMILES", source = "ChEBI")
                    smiles_array.append(sub_com.get_smiles())
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            smiles = cirpy.resolve(iden["identifier"], "smiles")
            if smiles not in smiles_array and smiles is not None and smiles != "None":
                gnomics.objects.compound.Compound.add_identifier(com, identifier = smiles, language = None, identifier_type = "SMILES", source = "CIR")
                smiles_array.append(smiles)
                
    if smiles_array:
        return smiles_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier", "kegg accession"]):
        gnomics.objects.compound.Compound.chebi_id(com)
        return gnomics.objects.compound.Compound.smiles(com)

#   Get canonical SMILES.
def get_canonical_smiles(com, user=None):
    smiles_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["canonical smiles"]):
        if iden["identifier"] not in smiles_array:
            smiles_array.append(iden["identifier"])

    if smiles_array:
        return smiles_array
    
    ids_completed = []
        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com):
                if sub_com.canonical_smiles not in smiles_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = sub_com.canonical_smiles, identifier_type = "Canonical SMILES", source = "PubChem", language = None)
                    smiles_array.append(sub_com.canonical_smiles)
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chembl", "chembl id", "chembl identifier", "chembl compound", "chembl compound id", "chembl compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chembl_molecule(com):
                if sub_com["molecule_structures"]["canonical_smiles"] not in smiles_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = sub_com["molecule_structures"]["canonical_smiles"], identifier_type = "Canonical SMILES", source = "ChEMBL", language = None)
                    smiles_array.append(sub_com["molecule_structures"]["canonical_smiles"])
        
    return smiles_array    
    
#	Get isomeric SMILES.
def get_isomeric_smiles(com, user=None):
    smiles_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["isomeric smiles"]):
        if iden["identifier"] not in smiles_array:
            smiles_array.append(iden["identifier"])

    if smiles_array:
        return smiles_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com):
                if sub_com.isomeric_smiles not in smiles_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = sub_com.isomeric_smiles, identifier_type = "Isomeric SMILES", language = None, source = "PubChem")
                    smiles_array.append(sub_com.isomeric_smiles)
    
    return smiles_array
	
#   UNIT TESTS
def smiles_unit_tests(chemspider_id, chebi_id, cas_rn, kegg_drug_id, pubchem_cid, chembl_id, kegg_compound_id, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting SMILES from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        smiles_array = get_smiles(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting SMILES from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        smiles_array = get_smiles(chebi_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("\nGetting SMILES from CAS RN (%s):" % cas_rn)
        start = timeit.timeit()
        smiles_array = get_smiles(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG COMPOUND ID", source = "KEGG")
        print("\nGetting SMILES from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        smiles_array = get_smiles(kegg_compound_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting canonical SMILES from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        smiles_array = get_canonical_smiles(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        print("\nGetting isomeric SMILES from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        smiles_array = get_isomeric_smiles(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("\nGetting canonical SMILES from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        smiles_array = get_canonical_smiles(chembl_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI ID conversion...\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("Getting SMILES from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        smiles_array = get_smiles(chebi_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("\nGetting SMILES from CAS RN (%s):" % cas_rn)
        start = timeit.timeit()
        smiles_array = get_smiles(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG COMPOUND ID", source = "KEGG")
        print("\nGetting SMILES from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        smiles_array = get_smiles(kegg_compound_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting canonical SMILES from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        smiles_array = get_canonical_smiles(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        print("\nGetting isomeric SMILES from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        smiles_array = get_isomeric_smiles(pubchem_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("\nGetting canonical SMILES from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        smiles_array = get_canonical_smiles(chembl_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in smiles_array:
            print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()