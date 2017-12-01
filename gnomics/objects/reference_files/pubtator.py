#
#
#
#
#

#
#   IMPORT SOURCES:
#       
#

#
#   Get PubTator results.
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
import gnomics.objects.disease
import gnomics.objects.reference
import gnomics.objects.taxon
import gnomics.objects.variation

#   Other imports.
import json
import re
import requests

#   MAIN
def main():
    pubtator_unit_tests("28881388") 
    
# Return PubTator JSON object for further parsing.
    # Six concepts can be searched:
    # 1. Gene
    # 2. Disease
    # 3. Chemical
    # 4. Species
    # 5. Mutation
    # 6. BioConcept
    # "BioConcept" includes all of the other five categories.
    # An example JSON file is at this URL:
    # https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Chemical/19894120/JSON/
def pubtator(pubmed_ref = None, pmid = None, concept="BioConcept", format_type="JSON"):

    # Allow tab-delimited text (PubTator) and XML (BioC) outputs.
    # See here: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/PubTator/tutorial/index.html#AccessannotationsviaRESTfulAPI
    
    if pmid is not None:
        pubtator_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + str(concept) + "/" + str(pmid) + "/" + str(format_type) + "/"
        r = requests.get(pubtator_url, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        matches = re.findall(r'(?:\"text\":\")(?P<text>.+?)(?:\",\"denotations\")', r.text, re.DOTALL)
        match_replace = '"text":"' + matches[0].replace('"', "\'") + '","denotations"'
        pattern = re.compile(r'(?:\"text\":\")(?P<text>.+?)(?:\",\"denotations\")')
        processed_text = pattern.sub(match_replace, r.text)
        decoded = json.loads(processed_text)
        obj_list = []
        for iden in decoded["denotations"]:
            iden_str = iden["obj"].split(":")
            if "Species" in iden_str[0]:
                # NCBI Taxonomy Browser:
                # TaxID, Taxonomy ID, taxon number
                ncbi_species = iden_str[1]
                new_spec = gnomics.objects.taxon.Taxon(identifier = ncbi_species, identifier_type = "TaxID", language = None, source = "PubTator")
                obj_list.append(new_spec)
            elif "Chemical" in iden_str[0]:
                # NCBI MeSH Browser:
                # MeSH ID
                if iden_str[1] != "CHEBI":
                    mesh_chemical = iden_str[1]
                    new_chem = gnomics.objects.compound.Compound(identifier = mesh_chemical, identifier_type = "MeSH ID", language = None, source = "PubTator")
                    obj_list.append(new_chem)
                else:
                    chebi_chemical = iden_str[1] + iden_str[2]
                    new_chem = gnomics.objects.compound.Compound(identifier = chebi_chemical, identifier_type = "ChEBI ID", language = None, source = "PubTator")
                    obj_list.append(new_chem)
            elif "Disease" in iden_str[0]:
                # NCBI MeSH Browser:
                # MeSH ID
                mesh_disease = iden_str[1]
                new_dis = gnomics.objects.disease.Disease(identifier = pmid, identifier_type = "MeSH ID", language = None, source = "PubTator")
                obj_list.append(new_dis)
            elif "Gene" in iden_str[0]:
                # NCBI Gene Browser
                # Gene ID
                ncbi_gene = iden_str[1]
                new_gene = gnomics.objects.gene.Gene(identifier = pmid, identifier_type = "NCBI Gene ID", language = None, source = "PubTator")
                obj_list.append(new_gene)
            elif "Mutation" in iden_str[0]:
                rs_num = "rs" + str(iden_str[2])
            else:
                print("The following could not be identified:")
                print(str(iden_str))
        return obj_list
    elif pubmed_ref is not None:
        obj_list = []
        for ident in pubmed_ref.identifiers:
            if ident["identifier_type"].lower() == "pmid" or ident["identifier_type"].lower() == "pubmed identifier" or ident["identifier_type"].lower() == "pubmed id" or ident["identifier_type"].lower() == "pubmed":
                pubtator_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + str(concept) + "/" + str(ident["identifier"]) + "/" + str(format_type) + "/"
                r = requests.get(pubtator_url, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                matches = re.findall(r'(?:\"text\":\")(?P<text>.+?)(?:\",\"denotations\")', r.text, re.DOTALL)
                match_replace = '"text":"' + matches[0].replace('"', "\'") + '","denotations"'
                pattern = re.compile(r'(?:\"text\":\")(?P<text>.+?)(?:\",\"denotations\")')
                processed_text = pattern.sub(match_replace, r.text)
                decoded = json.loads(processed_text)
                for iden in decoded["denotations"]:
                    iden_str = iden["obj"].split(":")
                    if "Species" in iden_str[0]:
                        # NCBI Taxonomy Browser:
                        # TaxID, Taxonomy ID, taxon number
                        ncbi_species = iden_str[1]
                        new_spec = gnomics.objects.species.Species(identifier = ncbi_species, identifier_type = "TaxID", language = None, source = "PubTator")
                        obj_list.append(new_spec)
                    elif "Chemical" in iden_str[0]:
                        # NCBI MeSH Browser:
                        # MeSH ID
                        if iden_str[1] != "CHEBI":
                            mesh_chemical = iden_str[1]
                            new_chem = gnomics.objects.compound.Compound(identifier = mesh_chemical, identifier_type = "MeSH ID", language = None, source = "PubTator")
                            obj_list.append(new_chem)
                        else:
                            chebi_chemical = iden_str[1] + iden_str[2]
                            new_chem = gnomics.objects.compound.Compound(identifier = chebi_chemical, identifier_type = "ChEBI ID", language = None, source = "PubTator")
                            obj_list.append(new_chem)
                    elif "Disease" in iden_str[0]:
                        # NCBI MeSH Browser:
                        # MeSH ID
                        mesh_disease = iden_str[1]
                        new_dis = gnomics.objects.disease.Disease(identifier = pmid, identifier_type = "MeSH ID", language = None, source = "PubTator")
                        obj_list.append(new_dis)
                    elif "Gene" in iden_str[0]:
                        # NCBI Gene Browser
                        # Gene ID
                        ncbi_gene = iden_str[1]
                        new_gene = gnomics.objects.gene.Gene(identifier = pmid, identifier_type = "NCBI Gene ID", language = None, source = "PubTator")
                        obj_list.append(new_gene)
                    elif "Mutation" in iden_str[0]:
                        rs_num = "rs" + str(iden_str[2])
                    else:
                        print("The following could not be identified:")
                        print(str(iden_str))
                return obj_list
    elif pubmed_ref is None and pmid is None:
        print("A PubMed reference object or a PMID must be provided in order to use PubTator.")
        return ""
    else:
        print("An unknown error occurred.")
        return ""
        
#   UNIT TESTS
def pubtator_unit_tests(pmid):
    print("Getting PubTator results from raw PMID...")
    print(pubtator(pmid = pmid))
    print("\nGetting PubTator results from PubMed reference...")
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    print(pubtator(pubmed_ref = pubmed_ref))

#   MAIN
if __name__ == "__main__": main()