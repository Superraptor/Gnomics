#
#
#
#
#

#
#   IMPORT SOURCES:
#       CIRPY
#           http://cirpy.readthedocs.io/en/latest/
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

#   MAIN
def main():
    smiles_unit_tests("33510", "CHEBI:4911", "33419-42-0", "D00125", "6918092", "CHEMBL44657", "C01576")
	
#	Get SMILES.
def get_smiles(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "smiles":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user).smiles,
                'language': None,
                'identifier_type': "SMILES",
                'source': "ChemSpider"
            })
            return gnomics.objects.compound.Compound.smiles(com, user = user)
        elif ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id":
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.chebi_entity(com).get_smiles(),
                'language': None,
                'identifier_type': "SMILES",
                'source': "ChEBI"
            })
            return gnomics.objects.compound.Compound.chebi_entity(com).get_smiles()
        elif ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas" or ident["identifier_type"].lower() == "cas rn":
            print("Due to issues with Pybel this function is only working with CIR. Please check back in future versions of the software for a Pybel version of this function.")
            smiles = cirpy.resolve(ident["identifier"], "smiles")
            com.identifiers.append({
                'identifier': smiles,
                'language': None,
                'identifier_type': "SMILES",
                'source': "CIR"
            })
            return smiles
        elif ident["identifier_type"].lower() == "kegg drug" or ident["identifier_type"].lower() == "kegg drug id" or ident["identifier_type"].lower() == "kegg drug accession" or ident["identifier_type"].lower() == "kegg drug identifier":
            print("Due to issues with Pybel this function is not currently working. Please check back in future versions of the software.")
            return ""
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            print("Due to issues with Pybel this function is not currently working. Please check back in future versions of the software.")
            return ""
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            return gnomics.objects.compound.Compound.smiles(com)

#   Get canonical SMILES.
def get_canonical_smiles(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "canonical smiles":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.pubchem_compound(com).canonical_smiles,
                'language': None,
                'identifier_type': "Canonical SMILES",
                'source': "PubChem"
            })
            return gnomics.objects.compound.Compound.pubchem_compound(com).canonical_smiles
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["canonical_smiles"],
                'language': None,
                'identifier_type': "Canonical SMILES",
                'source': "ChEMBL"
            })
            return gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["canonical_smiles"]
    
#	Get isomeric SMILES.
def get_isomeric_smiles(com):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "isomeric smiles":
            return ident["identifier"]
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append({
                'identifier': gnomics.objects.compound.Compound.pubchem_compound(com).isomeric_smiles,
                'language': None,
                'identifier_type': "Isomeric SMILES",
                'source': "PubChem"
            })
            return gnomics.objects.compound.Compound.pubchem_compound(com).isomeric_smiles
	
#   UNIT TESTS
def smiles_unit_tests(chemspider_id, chebi_id, cas_rn, kegg_drug_id, pubchem_cid, chembl_id, kegg_compound_id, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting SMILES from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_smiles(chemspider_com, user = user) + "\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("Getting SMILES from ChEBI ID (%s):" % chebi_id)
        print("- " + get_smiles(chebi_com) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting SMILES from CAS RN (%s):" % cas_rn)
        print("- " + get_smiles(cas_com) + "\n")
        
        kegg_drug_com = gnomics.objects.compound.Compound(identifier = str(kegg_drug_id), identifier_type = "KEGG DRUG ID", source = "KEGG")
        print("Getting SMILES from KEGG Drug ID (%s):" % kegg_drug_id)
        print("- " + get_smiles(kegg_drug_com) + "\n")
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG COMPOUND ID", source = "KEGG")
        print("Getting SMILES from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_smiles(kegg_compound_com) + "\n")
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("Getting SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_smiles(pubchem_com) + "\n")
        
        print("Getting canonical SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_canonical_smiles(pubchem_com) + "\n")
        
        print("Getting isomeric SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_isomeric_smiles(pubchem_com) + "\n")
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("Getting canonical SMILES from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_canonical_smiles(chembl_com) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting SMILES from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_smiles(cas_com) + "\n")
        
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI ID conversion...\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("Getting SMILES from ChEBI ID (%s):" % chebi_id)
        print("- " + get_smiles(chebi_com) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting SMILES from CAS RN (%s):" % cas_rn)
        print("- " + get_smiles(cas_com) + "\n")
        
        kegg_drug_com = gnomics.objects.compound.Compound(identifier = str(kegg_drug_id), identifier_type = "KEGG DRUG ID", source = "KEGG")
        print("Getting SMILES from KEGG Drug ID (%s):" % kegg_drug_id)
        print("- " + get_smiles(kegg_drug_com) + "\n")
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG COMPOUND ID", source = "KEGG")
        print("Getting SMILES from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_smiles(kegg_compound_com) + "\n")
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("Getting SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_smiles(pubchem_com) + "\n")
        
        print("Getting canonical SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_canonical_smiles(pubchem_com) + "\n")
        
        print("Getting isomeric SMILES from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_isomeric_smiles(pubchem_com) + "\n")
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("Getting canonical SMILES from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_canonical_smiles(chembl_com) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting SMILES from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_smiles(cas_com) + "\n")

#   MAIN
if __name__ == "__main__": main()