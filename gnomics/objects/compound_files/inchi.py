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

#   MAIN
def main():
    inchi_unit_tests("33510", "CHEBI:4911", "C01576", "CHEMBL44657", "36462", "33419-42-0", "")

#   Get InChI.
def get_inchi(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "inchi":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user = user).inchi,
                    'language': None,
                    'identifier_type': "InChI",
                    'source': "ChemSpider"
                }
            )
            return gnomics.objects.compound.Compound.inchi(com, user = user)
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.pubchem_compound(com).inchi,
                    'language': None,
                    'identifier_type': "InChI",
                    'source': "PubChem"
                }
            )
            return gnomics.objects.compound.Compound.inchi(com, user)
        elif ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chebi_entity(com).get_inchi(),
                    'language': None,
                    'identifier_type': "InChI",
                    'source': "ChEBI"
                }
            )
            return gnomics.objects.compound.Compound.inchi(com, user)
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            return gnomics.objects.compound.Compound.inchi(com, user)
    for com_obj in com.compound_objects:
        if 'object_type' in com_obj:
            if com_obj['object_type'].lower() == 'pybel' or com_obj['object_type'].lower() == 'pybel mol' or com_obj['object_type'].lower() == 'mol':
                com.identifiers.append(
                    {
                        'identifier': com_obj["object"].write("inchi").strip(),
                        'language': None,
                        'identifier_type': "InChI",
                        'source': "Pybel MOL"
                    }
                )
                return gnomics.objects.compound.Compound.inchi(com, user)

#	Get InChI key.
def get_inchi_key(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "inchi key":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user).inchikey,
                    'language': None,
                    'identifier_type': "InChI key",
                    'source': "ChemSpider"
                }
            )
            return get_inchi_key(com, user)
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.pubchem_compound(com).inchikey,
                    'language': None,
                    'identifier_type': "InChI key",
                    'source': "PubChem"
                }
            )
            return gnomics.objects.compound.Compound.inchi_key(com, user)
        elif ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chebi_entity(com).get_inchi_key(),
                    'language': None,
                    'identifier_type': "InChI key",
                    'source': "ChEBI"
                }
            )
            return gnomics.objects.compound.Compound.inchi_key(com, user)
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            com.chebi_id
            return gnomics.objects.compound.Compound.inchi_key(com, user)

#	Get standard InChI.
def get_standard_inchi(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "standard inchi":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user).stdinchi,
                    'language': None,
                    'identifier_type': "Standard InChI",
                    'source': "ChemSpider"
                }
            )
            return gnomics.objects.compound.Compound.chemspider_compound(com, user).stdinchi
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["standard_inchi"],
                    'language': None,
                    'identifier_type': "Standard InChI",
                    'source': "ChEMBL"
                }
            )
            return gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["standard_inchi"]
        elif ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas":
            std_inchi = cirpy.resolve(ident["identifier"], "stdinchi")
            
            com.identifiers.append(
                {
                    'identifier': std_inchi,
                    'language': None,
                    'identifier_type': "Standard InChI",
                    'source': "CIR"
                }
            )
            return std_inchi
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
        
#   Get standard InChI key.
def get_standard_inchi_key(com, user = None):
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "standard inchi key":
            return ident["identifier"]
    for ident in com.identifiers:
        if (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chemspider_compound(com, user).stdinchikey,
                    'language': None,
                    'identifier_type': "Standard InChI key",
                    'source': "ChemSpider"
                }
            )
            return gnomics.objects.compound.Compound.chemspider_compound(com, user).stdinchikey
        elif ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas":
            std_inchi_key = cirpy.resolve(ident["identifier"], "stdinchikey")
            
            com.identifiers.append(
                {
                    'identifier': std_inchi_key,
                    'language': None,
                    'identifier_type': "Standard InChI key",
                    'source': "CIR"
                }
            )
            return std_inchi_key
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            com.identifiers.append(
                {
                    'identifier': gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["standard_inchi_key"],
                    'language': None,
                    'identifier_type': "Standard InChI key",
                    'source': "ChEMBL"
                }
            )
            return gnomics.objects.compound.Compound.chembl_molecule(com)[0]["molecule_structures"]["standard_inchi_key"]

#   UNIT TESTS
def inchi_unit_tests(chemspider_id, chebi_id, kegg_compound_id, chembl_id, pubchem_cid, cas_rn, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting InChI from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_inchi(chemspider_com, user = user) + "\n")
        
        print("Getting InChI key from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_inchi_key(chemspider_com, user = user) + "\n")
        
        print("Getting standard InChI from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_standard_inchi(chemspider_com, user = user) + "\n")
        
        print("Getting standard InChI key from ChemSpider ID (%s):" % chemspider_id)
        print("- " + get_standard_inchi_key(chemspider_com, user = user) + "\n")

        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("Getting InChI from ChEBI ID (%s):" % chebi_id)
        print("- " + get_inchi(chebi_com, user = user) + "\n")
        
        print("Getting InChI key from ChEBI ID (%s):" % chebi_id)
        print("- " + get_inchi_key(chebi_com, user = user) + "\n")
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("Getting InChI from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_inchi(kegg_compound_com, user = user) + "\n")
        
        print("Getting InChI key from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_inchi_key(kegg_compound_com, user = user) + "\n")
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("Getting standard InChI from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_standard_inchi(chembl_com, user = user) + "\n")
        
        print("Getting standard InChI key from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_standard_inchi_key(chembl_com, user = user) + "\n")
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("Getting InChI from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_inchi(pubchem_com, user = user) + "\n")
        
        print("Getting InChI key from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_inchi_key(pubchem_com, user = user) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting standard InChI from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_standard_inchi(cas_com) + "\n")
        
        print("Getting standard InChI key from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_standard_inchi_key(cas_com) + "\n")
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI Compound conversion...\n")
        
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("Getting InChI from ChEBI ID (%s):" % chebi_id)
        print("- " + get_inchi(chebi_com, user = user) + "\n")
        
        print("Getting InChI key from ChEBI ID (%s):" % chebi_id)
        print("- " + get_inchi_key(chebi_com, user = user) + "\n")
        
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("Getting InChI from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_inchi(kegg_compound_com, user = user) + "\n")
        
        print("Getting InChI key from KEGG Compound ID (%s):" % kegg_compound_id)
        print("- " + get_inchi_key(kegg_compound_com, user = user) + "\n")
        
        chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
        print("Getting standard InChI from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_standard_inchi(chembl_com, user = user) + "\n")
        
        print("Getting standard InChI key from ChEMBL ID (%s):" % chembl_id)
        print("- " + get_standard_inchi_key(chembl_com, user = user) + "\n")
        
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("Getting InChI from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_inchi(pubchem_com, user = user) + "\n")
        
        print("Getting InChI key from PubChem CID (%s):" % pubchem_cid)
        print("- " + get_inchi_key(pubchem_com, user = user) + "\n")
        
        cas_com = gnomics.objects.compound.Compound(identifier = str(cas_rn), identifier_type = "CAS Registry Number", source = "CAS")
        print("Getting standard InChI from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_standard_inchi(cas_com) + "\n")
        
        print("Getting standard InChI key from CAS Registry Number (%s):" % cas_rn)
        print("- " + get_standard_inchi_key(cas_com) + "\n")

#   MAIN
if __name__ == "__main__": main()