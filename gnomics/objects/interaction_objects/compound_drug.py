#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get drugs from compound.
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
import gnomics.objects.drug

#   Other imports.
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    rxcui_unit_tests("LVX8N1UT73", "CHEMBL44657", "CHEBI:4911", "Q418817")
    
#   Get drugs.
def get_drugs(compound):
    id_array = []
    drug_array = []
    for ident in compound.identifiers:
        if ident["identifier_type"].lower() == "unii" or ident["identifier_type"].lower() == "fda unique ingredient identifier code" or ident["identifier_type"].lower() == "unique ingredient identifier":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=UNII_CODE&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = x, identifier_type = "RxCUI", language = None, source = "RxNorm")
                    drug_array.append(temp_drug)
                    id_array.append(x)
        elif ident["identifier_type"].lower() == "chembl" or ident["identifier_type"].lower() == "chembl id" or ident["identifier_type"].lower() == "chembl identifier":
            atc_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["atc_classifications"]
            for atc in atc_array_from_chembl:
                atc_string = atc.rsplit("/", 1)[1]
                if atc_string not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = atc_string, language = None, identifier_type = "ATC Classification", source = "ChEMBL")
                    id_array.append(atc_string)
                    drug_array.append(temp_drug)
            syn_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["molecule_synonyms"]
            for syn in syn_array_from_chembl:
                if syn["syn_type"] == "BAN" and syn["molecule_synonym"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "BAN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["molecule_synonym"])
                if syn["syn_type"] == "BAN" and syn["synonyms"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["synonyms"], identifier_type = "BAN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["synonyms"])
            syn_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["molecule_synonyms"]
            for syn in syn_array_from_chembl:
                if syn["syn_type"] == "TRADE_NAME" and syn["molecule_synonym"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "Trade Name", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["molecule_synonym"])
                if syn["syn_type"] == "TRADE_NAME" and syn["synonyms"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["synonyms"].strip(), identifier_type = "Trade Name", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["synonyms"])
            syn_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["molecule_synonyms"]
            for syn in syn_array_from_chembl:
                if syn["syn_type"] == "FDA" and syn["molecule_synonym"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "FDA Approved Name", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["molecule_synonym"])
                if syn["syn_type"] == "FDA" and syn["synonyms"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["synonyms"].strip(), identifier_type = "FDA Approved Name", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["synonyms"])
            syn_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["molecule_synonyms"]
            for syn in syn_array_from_chembl:
                if syn["syn_type"] == "INN" and syn["molecule_synonym"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "INN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["molecule_synonym"])
                if syn["syn_type"] == "INN" and syn["synonyms"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["synonyms"].strip(), identifier_type = "INN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["synonyms"])
            syn_array_from_chembl = gnomics.objects.compound.Compound.chembl_molecule(compound)[0]["molecule_synonyms"]
            for syn in syn_array_from_chembl:
                if syn["syn_type"] == "JAN" and syn["molecule_synonym"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "JAN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["molecule_synonym"])
                if syn["syn_type"] == "JAN" and syn["synonyms"] not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn["molecule_synonym"].strip(), identifier_type = "JAN", language = None, source = "ChEMBL")
                    drug_array.append(temp_drug)
                    id_array.append(syn["synonyms"])
        elif ident["identifier_type"].lower() == "chebi" or ident["identifier_type"].lower() == "chebi id" or ident["identifier_type"].lower() == "chebi identifier":
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(compound).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "drugbank accession" and accession._DatabaseAccession__typ.lower() not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = accession._DatabaseAccession__accession_number, identifier_type = "DrugBank Accession", language = None, source = "ChEBI")
                    drug_array.append(temp_drug)
                    id_array.append(accession._DatabaseAccession__accession_number)
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(compound).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "drug central accession" and accession._DatabaseAccession__typ.lower() not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = accession._DatabaseAccession__accession_number, identifier_type = "Drug Central Accession", language = None, source = "ChEBI")
                    drug_array.append(temp_drug)
                    id_array.append(accession._DatabaseAccession__accession_number)
            syn_array_from_chebi = gnomics.objects.compound.Compound.chebi_entity(compound).get_names()
            for syn in syn_array_from_chebi:
                if syn._Name__typ == "INN" and syn._Name__name not in id_array:
                    temp_drug = gnomics.objects.drug.Drug(identifier = syn._Name__name, identifier_type = "INN", language = syn._Name__language, source = "ChEBI")
                    drug_array.append(temp_drug)
                    id_array.append(syn._Name__name)
            db_accessions = gnomics.objects.compound.Compound.chebi_entity(compound).get_database_accessions()
            for accession in db_accessions:
                if accession._DatabaseAccession__typ.lower() == "kegg drug accession":
                    temp_drug = gnomics.objects.drug.Drug(identifier = accession._DatabaseAccession__accession_number, identifier_type = "KEGG DRUG Accession", language = syn._Name__language, source = "ChEBI")
                    drug_array.append(temp_drug)
                    id_array.append(accession._DatabaseAccession__accession_number)
        elif ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.compound.Compound.wikidata(compound):
                com_array = []
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "atc code":
                        for x in prop_dict:
                            temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "ATC Code", language = None, source = "Wikidata")
                            drug_array.append(temp_drug)
                            id_array.append(x["mainsnak"]["datavalue"]["value"])
                    elif en_prop_name.lower() == "rxnorm cui":
                        for x in prop_dict:
                            temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "RxCUI", language = None, source = "Wikidata")
                            drug_array.append(temp_drug)
                            id_array.append(x["mainsnak"]["datavalue"]["value"])
                    elif en_prop_name.lower() == "ndf-rt id":
                        for x in prop_dict:
                            temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NDF-RT ID", language = None, source = "Wikidata")
                            drug_array.append(temp_drug)
                            id_array.append(x["mainsnak"]["datavalue"]["value"])
                    elif en_prop_name.lower() == "world health organisation international nonproprietary name":
                        for x in prop_dict:
                            temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"]["text"], identifier_type = "INN", language = x["mainsnak"]["datavalue"]["value"]["language"], source = "Wikidata")
                            drug_array.append(temp_drug)
                            id_array.append(x["mainsnak"]["datavalue"]["value"])
                    elif en_prop_name.lower() == "kegg id":
                        for x in prop_dict:
                            if "D" in x["mainsnak"]["datavalue"]["value"]:
                                temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "NDF-RT ID", language = None, source = "Wikidata")
                                drug_array.append(temp_drug)
                                id_array.append(x["mainsnak"]["datavalue"]["value"])
                    elif en_prop_name.lower() == "drugbank id":
                        for x in prop_dict:
                            temp_drug = gnomics.objects.drug.Drug(identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "DrugBank ID", language = None, source = "Wikidata")
                            drug_array.append(temp_drug)
                            id_array.append(x["mainsnak"]["datavalue"]["value"])
    return drug_array
    
#   UNIT TESTS
def rxcui_unit_tests(unii, chembl_id, chebi_id, wikidata_accession):
    unii_com = gnomics.objects.compound.Compound(identifier = str(unii), identifier_type = "UNII", source = "FDA")
    print("\nGetting drugs (RxCUIs) from compound (UNII) (%s):" % unii)
    for rx in get_drugs(unii_com):
        for iden in rx.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    chembl_com = gnomics.objects.compound.Compound(identifier = str(chembl_id), identifier_type = "ChEMBL ID", source = "ChEMBL")
    print("\nGetting drug identifiers from compound (ChEMBL ID) (%s):" % chembl_id)
    for rx in get_drugs(chembl_com):
        for iden in rx.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    chebi_com = gnomics.objects.compound.Compound(identifier = str(chebi_id), identifier_type = "ChEBI ID", source = "ChEBI")
    print("\nGetting drug identifiers from compound (ChEBI ID) (%s):" % chebi_id)
    for rx in get_drugs(chebi_com):
        for iden in rx.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
    wikidata_com = gnomics.objects.compound.Compound(identifier = str(wikidata_accession), identifier_type = "Wikidata Accession", source = "Wikidata")
    print("\nGetting drug identifiers from Wikidata Accession (%s):" % wikidata_accession)
    for rx in get_drugs(wikidata_com):
        for iden in rx.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()