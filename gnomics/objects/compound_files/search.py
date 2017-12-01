#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMSPIPY
#           http://chemspipy.readthedocs.io/en/latest/
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Search for compounds.
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
from chemspipy import ChemSpider as chemspider
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    basic_search_unit_tests("etoposide", "C29H32O13", "CC1OCC2C(O1)C(C(C(O2)OC3C4COC(=O)C4C(C5=CC6=C(C=C35)OCO6)C7=CC(=C(C(=C7)OC)OP(=O)(O)O)OC)O)O", "LIQODXNTTZAGID-OCBXBXKTSA-N", "")
    cas_search_unit_tests("33419-42-0")

#   Search.
#
#   Many types of search are included here, currently only
#   through ChemSpider and PubChem, although others are
#   likely to be added in the future.
#
#   TODO: Add RxNorm SOAP API search:
#   https://mor.nlm.nih.gov/download/rxnav/RxNormAPIs.html#uLink=RxNorm_SOAP_findRxcuiByString
#
#   For more on PubChem searching see the following:
#   https://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
#   http://pubchempy.readthedocs.io/en/latest/guide/searching.html
#
#   The 'query' is the string being search.
#   'search_type' is what the query represents. If
#   'search_type' is None, then a general search is
#   performed. 'source' refers to where the search is
#   taking place. If not specified, default is 'chemspider'.
#   'mass_plus_minus' refers to a molecular weight/mass
#   search on ChemSpider, wherein the weight/mass is within
#   that range. It must be a number data type, as strings
#   will not be parsed correctly.
def search(query, user = None, search_type = None, source = "chemspider", mass_plus_minus = 0.001):
    result_set = []
    if source.lower() == "chemspider" or source.lower() == "all":
        if user is not None and user.chemspider_security_token is not None:
            cs = chemspider(user.chemspider_security_token)
            if search_type == None:
                for result in cs.search(query):
                    temp_com = gnomics.objects.compound.Compound(identifier = result.csid, identifier_type = "ChemSpider ID", source = "ChemSpider", name = None)
                    result_set.append(temp_com)
                return result_set
            elif search_type == "formula" or search_type == "molecular formula":
                for result in cs.simple_search_by_formula(query):
                    temp_com = gnomics.objects.compound.Compound(identifier = result.csid, identifier_type = "ChemSpider ID", source = "ChemSpider", name = None)
                    result_set.append(temp_com)
                return result_set
            elif search_type == "mass" and mass_plus_minus is not None:
                for result in cs.simple_search_by_mass(query, mass_plus_minus):
                    temp_com = gnomics.objects.compound.Compound(identifier = result.csid, identifier_type = "ChemSpider ID", source = "ChemSpider", name = None)
                    result_set.append(temp_com)
                return result_set
            else:
                print("No valid search type for ChemSpider was provided.")
                print("Continuing with search type 'None'...")
                return search(query, user = user, search_type = None, source = "chemspider")
        elif source.lower() == "chemspider":
            print("Searching with ChemSpider requires the creation of a User object with a valid ChemSpider security token. Information on obtaining such a token can be found here: 'http://www.chemspider.com/AboutServices.aspx?'.\n")
            print("Continuing with PubChem search...\n")
            return search(query, source = "pubchem")
    if source.lower() == "pubchem" or source.lower() == "all":
        if search_type == None:
            try:
                server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
                ext = "/compound/name/" + str(query) + "/synonyms/JSONP"
                r = requests.get(server+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    print("No results found.")
                    return result_set
                str_r = r.text
                try:
                    l_index = str_r.index("(") + 1
                    r_index = str_r.rindex(")")
                except ValueError:
                    print("Input is not in a JSONP format.")
                    exit()
                res = str_r[l_index:r_index]
                decoded = json.loads(res)
                for result in decoded["InformationList"]["Information"]:
                    result_cid = result["CID"]
                    temp_com = gnomics.objects.compound.Compound(identifier = result_cid, identifier_type = "PubChem CID", source = "PubChem", name = result["Synonym"][0])
                    result_set.append(temp_com)
            except requests.exceptions.RequestException as e:
                print(e)
                print("No results found.")
            return result_set
        elif search_type == "substructure":
            return pubchem.get_compounds(query, "substructure")
        elif search_type == "superstructure":
            return pubchem.get_compounds(query, "superstructure")
        elif search_type == "similarity":
            return pubchem.get_compounds(query, "similarity")
        elif search_type == "identity":
            return pubchem.get_compounds(query, "identity")
        elif search_type.lower() == "smiles":
            format_results = []
            for temp_com in pubchem.get_compounds(query, "smiles"):
                if temp_com.synonyms:
                    new_com = gnomics.objects.compound.Compound(identifier = temp_com.cid, identifier_type = "PubChem CID", source = "PubChem", name = temp_com.synonyms[0])
                    format_results.append(new_com)
                else:
                    new_com = gnomics.objects.compound.Compound(identifier = temp_com.cid, identifier_type = "PubChem CID", source = "PubChem", name = temp_com.iupac_name)
                    format_results.append(new_com)
            return format_results
        elif search_type.lower() == "inchi":
            format_results = []
            for temp_com in pubchem.get_compounds(query, "inchi"):
                if temp_com.synonyms:
                    new_com = gnomics.objects.compound.Compound(identifier = temp_com.cid, identifier_type = "PubChem CID", source = "PubChem", name = temp_com.synonyms[0])
                    format_results.append(new_com)
                else:
                    new_com = gnomics.objects.compound.Compound(identifier = temp_com.cid, identifier_type = "PubChem CID", source = "PubChem", name = temp_com.iupac_name)
                    format_results.append(new_com)
            return format_results
        elif search_type == "sdf":
            return pubchem.get_compounds(query, "sdf")
        elif search_type == "cid":
            return pubchem.get_compounds(query, "cid")
        elif search_type == "cas":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/name/" + str(query) + "/synonyms/JSONP"
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
            for result in decoded["InformationList"]["Information"]:
                for syn in result["Synonym"]:
                    if syn == query:
                        result_cid = result["CID"]
                        temp_com = gnomics.objects.compound.Compound(identifier = result_cid, identifier_type = "PubChem CID", source = "PubChem", name = result["Synonym"][0])
                        result_set.append(temp_com)
            return result_set
        else:
            print("No valid search type for PubChem was provided.")
            print("Continuing with search type 'None'...")
            return search(query, user = None, search_type = None, source = "pubchem")
    else:
        print("No valid search source was provided.")
        if user is not None and user.chemspider_security_token is not None:
            print("Because user and ChemSpider security token are provided, continuing with ChemSpider search...")
            return search(query, user = user, search_type = None, source = "chemspider")
        else:
            print("Because either user not provided or ChemSpider security token is not valid, continuing with PubChem search...")
            return search(query, user = None, search_type = None, source = "pubchem")

#   UNIT TESTS
def basic_search_unit_tests(basic_query, formula_query, smiles_query, inchi_query, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        print("Beginning basic search for '%s'..." % basic_query)
        basic_search_results = search(basic_query, user = user, source = "chemspider")
        print("Search returned %s result(s) with the following ChemSpider IDs:" % str(len(basic_search_results)))
        for com in basic_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
        print("\nContinuing with PubChem search...\n")
        print("Beginning basic search for '%s'..." % basic_query)
        basic_search_results = search(basic_query, source = "pubchem")
        print("Search returned %s result(s) with the following PubChem CIDs:" % str(len(basic_search_results)))
        for com in basic_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
        print("\nContinuing with slightly more complicated searches (molecular formula, SMILES, InChI, etc.)...\n")
        formula_search_results = search(formula_query, user = user, source = "chemspider", search_type = "formula")
        print("\nSearch for molecular formula returned %s result(s) with the following ChemSpider IDs:" % str(len(formula_search_results)))
        for com in formula_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
        smiles_search_results = search(smiles_query, source = "pubchem", search_type = "smiles")
        print("\nSearch for SMILES returned %s result(s) with the following PubChem CIDs:" % str(len(smiles_search_results)))
        for com in smiles_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
    else:
        print("No user provided. Cannot test ChemSpider search without ChemSpider security token.\n")
        print("Continuing with PubChem search...\n")
        print("Beginning basic search for '%s'..." % basic_query)
        basic_search_results = search(basic_query, source = "pubchem")
        print("\nSearch returned %s result(s) with the following PubChem CIDs:" % str(len(basic_search_results)))
        for com in basic_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
        smiles_search_results = search(smiles_query, source = "pubchem")
        print("\nSearch returned %s result(s) with the following PubChem CIDs:" % str(len(smiles_search_results)))
        for com in smiles_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
        inchi_search_results = search(inchi_query, source = "pubchem")
        print("Search returned %s result(s) with the following PubChem CIDs:" % str(len(inchi_search_results)))
        for com in inchi_search_results:
            for ident in com.identifiers:
                print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
            
def cas_search_unit_tests(query):
    print("Beginning CAS search for '%s'..." % query)
    cas_search_results = search(query, search_type = "cas", source = "pubchem")
    print("Search returned %s result(s) with the following PubChem CIDs:" % str(len(cas_search_results)))
    for com in cas_search_results:
        for ident in com.identifiers:
            print("- %s: %s (%s)" % (ident["identifier"], ident["name"], ident["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()