#
#
#
#
#

#
#   IMPORT SOURCES:
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get CAS registry numbers.
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
import json
import pubchempy as pubchem
import re
import requests

#   MAIN
def main():
    cas_unit_tests("CHEBI:4911", "33510", "C01576", "6918092", "Q418817", "fd4ce40f-23e5-44be-91f5-a40b92ab1580")

#   Get CAS.
def get_cas(com, user = None):
    cas_array = []
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "cas registry number" or ident["identifier_type"].lower() == "cas":
            cas_array.append(ident["identifier"])
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(com).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "cas registry number" and accession._DatabaseAccession__accession_number not in cas_array:
                    com.identifiers.append(
                        {
                            'identifier': accession._DatabaseAccession__accession_number,
                            'language': None,
                            'identifier_type': "CAS Registry Number",
                            'source': "ChEBI"
                        }
                    )
                    cas_array.append(accession._DatabaseAccession__accession_number)
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is not None:
            cas_num_regex = re.compile("^([0-9]{2,7}-[0-9]{2}-[0-9])$")
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(gnomics.objects.compound.Compound.pubchem_cid(com, user = user)) + "/synonyms/JSONP"
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
            synonym_list = decoded["InformationList"]["Information"][0]["Synonym"]
            final_num = []
            for synonym in synonym_list:
                if re.match(cas_num_regex, synonym) and synonym not in cas_array:
                    com.identifiers.append(
                        {
                            'identifier': synonym,
                            'language': None,
                            'identifier_type': "CAS Registry Number",
                            'source': "PubChem"
                        }
                    )
                    cas_array.append(synonym)
        elif (ident["identifier_type"].lower() == "chemspider" or ident["identifier_type"].lower() == "chemspider id" or ident["identifier_type"].lower() == "chemspider identifier") and user is None:
            print("Cannot use ChemSpider conversion when user is None. Please create and pass a valid user with a ChemSpider security token to this method.")
        elif ident["identifier_type"].lower() == "pubchem cid" or ident["identifier_type"].lower() == "cid":
            server = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            ext = "/compound/cid/" + str(ident["identifier"]) + "/xrefs/RN/JSONP"
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
                regi = result["RN"]
                for reg in regi:
                    if reg not in cas_array:
                        com.identifiers.append({"identifier" : reg, "identifier_type" : "CAS Registry Number", "source" : "PubChem", "language" : None})
                        cas_array.append(reg)
        elif ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
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
                    if en_prop_name.lower() == "cas registry number":
                        for x in prop_dict:
                            gnomics.objects.compound.Compound.add_identifier(com, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "CAS Registry Number", language = None, source = "Wikidata")
                            cas_array.append(x["mainsnak"]["datavalue"]["value"])
    if cas_array:
        return cas_array
    for ident in com.identifiers:
        if ident["identifier_type"].lower() == "kegg compound" or ident["identifier_type"].lower() == "kegg compound id" or ident["identifier_type"].lower() == "kegg compound accession":
            gnomics.objects.compound.Compound.chebi_id(com)
            return get_cas(com)

#   UNIT TESTS
def cas_unit_tests(chebi_id, chemspider_id, kegg_compound_id, pubchem_cid, wikidata_accession, chemspider_security_token = None):
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting CAS Registry Number from ChemSpider ID (%s):" % chemspider_id)
        for com in get_cas(chemspider_com, user = user):
            print("- %s" % str(com))
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting CAS Registry Number from ChEBI ID (%s):" % chebi_id)
        for com in get_cas(chebi_com, user = user):
            print("- %s" % str(com))
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting CAS Registry Number from PubChem CID (%s):" % pubchem_cid)
        for com in get_cas(pubchem_com):
            print("- %s" % str(com))
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting CAS Registry Number from KEGG Compound ID (%s):" % kegg_compound_id)
        for com in get_cas(kegg_compound_com, user = user):
            print("- %s" % str(com))
        wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
        print("\nGetting CAS Registry Number from Wikidata Accession (%s):" % wikidata_accession)
        for com in get_cas(wikidata_com):
            print("- " + str(com))
    else:
        print("No user provided. Cannot test ChemSpider conversion without ChemSpider security token.\n")
        print("Continuing with ChEBI ID conversion...\n")
        chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
        print("\nGetting CAS Registry Number from ChEBI ID (%s):" % chebi_id)
        for com in get_cas(chebi_com, user = user):
            print("- %s" % str(com))
        pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
        print("\nGetting external registry IDs from PubChem CID (%s):" % pubchem_cid)
        for com in get_cas(pubchem_com):
            print("- %s" % str(com))
        kegg_compound_com = gnomics.objects.compound.Compound(identifier = str(kegg_compound_id), identifier_type = "KEGG Compound ID", source = "KEGG")
        print("\nGetting CAS Registry Number from KEGG Compound ID (%s):" % kegg_compound_id)
        for com in get_cas(kegg_compound_com, user = user):
            print("- %s" % str(com))

#   MAIN
if __name__ == "__main__": main()