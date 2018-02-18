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
#   Get InChI.
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
    inchi_unit_tests("33510", "CHEBI:4911", "C01576", "CHEMBL44657", "36462", "33419-42-0", "fd4ce40f-23e5-44be-91f5-a40b92ab1580")

#   Get InChI.
def get_inchi(com, user=None):
    inchi_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["inchi", "standard inchi", "iupac international chemical", "iupac international chemical id", "iupac international chemical identifier", "standard iupac international chemical", "standard iupac international chemical id", "standard iupac international chemical identifier"]):
        if iden["identifier"] not in inchi_array:
            inchi_array.append(iden["identifier"])
            
    if inchi_array:
        return inchi_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user = user):
                temp_inchi = sub_com.inchi
                if temp_inchi not in inchi_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "InChI", language = None, source = "ChemSpider")
                    inchi_array.append(temp_inchi)
            
        elif user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com, user = user):
                temp_inchi = sub_com.inchi
                if temp_inchi not in inchi_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "InChI", language = None, source = "PubChem")
                    inchi_array.append(temp_inchi)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                temp_inchi = sub_com.get_inchi()
                if temp_inchi not in inchi_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "InChI", language = None, source = "ChEBI")
                    inchi_array.append(temp_inchi)
                
    if inchi_array:
        return inchi_array
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_inchi(com, user = user)
                
    if inchi_array:
        return inchi_array
    
    for com_obj in com.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() in ["pybel", "pybel mol", "mol"]:
                gnomics.objects.compound.Compound.add_identifier(com, identifier = com_obj["object"].write("inchi").strip(), identifier_type = "InChI", language = None, source = "Pybel MOL")
                inchi_array.append(com_obj["object"].write("inchi").strip())
        
    return inchi_array

#	Get InChI key.
def get_inchi_key(com, user=None):
    
    inchi_key_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["inchi key", "standard inchi key", "iupac international chemical id key", "iupac international chemical identifier key", "standard iupac international chemical id key", "standard iupac international chemical identifier key", "inchikey"]):
        if iden["identifier"] not in inchi_key_array:
            inchi_key_array.append(iden["identifier"])
            
    if inchi_key_array:
        return inchi_key_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                temp_inchi_key = sub_com.inchikey
                if temp_inchi_key not in inchi_key_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "InChI Key", language = None, source = "ChemSpider")
                    inchi_key_array.append(temp_inchi_key)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cid", "pubchem cid", "pubchem compound", "pubchem compound id", "pubchem compound identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.pubchem_compound(com):
                temp_inchi_key = sub_com.inchikey
                if temp_inchi_key not in inchi_key_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "InChI Key", language = None, source = "PubChem")
                    inchi_key_array.append(temp_inchi_key)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chebi", "chebi id", "chebi identifier"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chebi_entity(com):
                temp_inchi_key = sub_com.get_inchi_key()
                if temp_inchi_key not in inchi_key_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "InChI Key", language = None, source = "ChEBI")
                    inchi_key_array.append(temp_inchi_key)
                
    if inchi_key_array:
        return inchi_key_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["kegg compound", "kegg compound id", "kegg compound identifier", "kegg", "kegg compound accession", "kegg id", "kegg identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            return get_inchi_key(com, user = user)
            
    return inchi_key_array

#	Get standard InChI.
def get_standard_inchi(com, user=None):
    
    inchi_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["standard inchi", "standard iupac international chemical", "standard iupac international chemical id", "standard iupac international chemical identifier"]):
        if iden["identifier"] not in inchi_array:
            inchi_array.append(iden["identifier"])
            
    if inchi_array:
        return inchi_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
    
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                temp_inchi = sub_com.stdinchi
                if temp_inchi not in inchi_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "Standard InChI", language = None, source = "ChemSpider")
                    inchi_array.append(temp_inchi)
                
        elif user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chembl", "chembl compound", "chembl compound id", "chembl compound identifier", "chembl id", "chembl identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            for sub_com in gnomics.objects.compound.Compound.chembl_molecule(com):
                temp_inchi = sub_com["molecule_structures"]["standard_inchi"]
                if temp_inchi not in inchi_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "Standard InChI", language = None, source = "ChEMBL")
                    inchi_array.append(temp_inchi)
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            temp_inchi = cirpy.resolve(iden["identifier"], "stdinchi")
            if temp_inchi not in inchi_array and temp_inchi is not None and temp_inchi != "None":
                gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi, identifier_type = "Standard InChI", language = None, source = "CIR")
                inchi_array.append(temp_inchi)

    return inchi_array
        
#   Get standard InChI key.
def get_standard_inchi_key(com, user=None):
    
    inchi_key_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["standard inchi key", "standard iupac international chemical id key", "standard iupac international chemical identifier key", "stdinchikey"]):
        if iden["identifier"] not in inchi_key_array:
            inchi_key_array.append(iden["identifier"])
            
    if inchi_key_array:
        return inchi_key_array
            
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chemspider", "chemspider id", "chemspider identifier", "cs id", "csid"]):
        if iden["identifier"] not in ids_completed and user is not None:
            ids_completed.append(iden["identifier"])
    
            for sub_com in gnomics.objects.compound.Compound.chemspider_compound(com, user):
                temp_inchi_key = sub_com.stdinchikey
                if temp_inchi_key not in inchi_key_array:
                    gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "Standard InChI Key", language = None, source = "ChemSpider")
                    inchi_key_array.append(temp_inchi_key)
                
        elif user is None:
            
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["cas", "cas registry", "cas registry number", "cas rn"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            temp_inchi_key = cirpy.resolve(iden["identifier"], "stdinchikey")
            if temp_inchi_key not in inchi_key_array:
                gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "Standard InChI Key", language = None, source = "CIR")
                inchi_key_array.append(temp_inchi_key)
                
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(com.identifiers, ["chembl", "chembl compound", "chembl compound id", "chembl compound identifier", "chembl id", "chembl identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            
            temp_inchi_key = gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["standard_inchi_key"]
            
            if temp_inchi_key not in inchi_key_array and temp_inchi is not None and temp_inchi != "None":
                gnomics.objects.compound.Compound.add_identifier(com, identifier = temp_inchi_key, identifier_type = "Standard InChI Key", language = None, source = "ChEMBL")
                inchi_key_array.append(temp_inchi_key)
                
    return inchi_key_array

#   UNIT TESTS
def inchi_unit_tests(chemspider_id, chebi_id, kegg_compound_id, chembl_id, pubchem_cid, cas_rn, chemspider_security_token=None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("\nGetting InChI from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        inchi_array = get_inchi(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        inchi_array = get_inchi_key(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI key from ChemSpider ID (%s):" % chemspider_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi_key(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))

        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting InChI from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        inchi_array = get_inchi(chebi_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        inchi_array = get_inchi_key(chebi_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting InChI from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        inchi_array = get_inchi(kegg_compound_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        inchi_array = get_inchi_key(kegg_compound_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("\nGetting standard InChI from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi(chembl_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI key from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi_key(chembl_com, user = user) 
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting InChI from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        inchi_array = get_inchi(pubchem_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        inchi_array = get_inchi_key(pubchem_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("\nGetting standard InChI from CAS Registry Number (%s):" % cas_rn)
        start = timeit.timeit()
        inchi_array = get_standard_inchi(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI key from CAS Registry Number (%s):" % cas_rn)
        start = timeit.timeit()
        inchi_array = get_standard_inchi_key(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI Compound conversion...\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting InChI from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        inchi_array = get_inchi(chebi_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from ChEBI ID (%s):" % chebi_id)
        start = timeit.timeit()
        inchi_array = get_inchi_key(chebi_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting InChI from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        inchi_array = get_inchi(kegg_compound_com, user = user) 
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from KEGG Compound ID (%s):" % kegg_compound_id)
        start = timeit.timeit()
        inchi_array = get_inchi_key(kegg_compound_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("\nGetting standard InChI from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi(chembl_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI key from ChEMBL ID (%s):" % chembl_id)
        start = timeit.timeit()
        inchi_array = get_standard_inchi_key(chembl_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting InChI from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        inchi_array = get_inchi(pubchem_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting InChI key from PubChem CID (%s):" % pubchem_cid)
        start = timeit.timeit()
        inchi_array = get_inchi_key(pubchem_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("\nGetting standard InChI from CAS Registry Number (%s):" % cas_rn)
        start = timeit.timeit()
        inchi_array = get_standard_inchi(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))
        
        print("\nGetting standard InChI key from CAS Registry Number (%s):" % cas_rn)
        start = timeit.timeit()
        inchi_array = get_standard_inchi_key(cas_com)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for com in inchi_array:
            print("\t- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()