#
#
#
#
#

#
#   Get OMIM gene.
#

#
#   IMPORT SOURCES:
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
import gnomics.objects.gene

#   Other imports.
import requests

#   MAIN
def main():
    omim_unit_tests("hsa:5315", "ENSG00000157764")

# Returns OMIM identifier.
def get_omim_gene_id(gene):
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "omim gene" or ident["identifier_type"].lower() == "omim gene id" or ident["identifier_type"].lower() == "omim gene identifier" or ident["identifier_type"].lower() == "omim" or ident["identifier_type"].lower() == "omim id":
            return ident["identifier"]
    for ident in gene.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg gene id":
            gene.identifiers.append({
                'identifier': gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["OMIM"],
                'language': None,
                'identifier_type': "OMIM gene identifier",
                'taxon': "Homo sapiens",
                'source': "OMIM"
            })
            return gnomics.objects.gene.Gene.kegg_gene(gene)["DBLINKS"]["OMIM"]
        elif ident["identifier_type"].lower() == "ensembl gene" or ident["identifier_type"].lower() == "ensembl gene id" or ident["identifier_type"].lower() == "ensembl gene identifier" or ident["identifier_type"].lower() == "ensembl":
            server = "https://rest.ensembl.org"
            ext = "/xrefs/id/" + ident["identifier"]
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            for new_id in decoded:
                if new_id["dbname"] == "MIM_GENE":
                    gene.identifiers.append({
                        'identifier': new_id["primary_id"],
                        'language': None,
                        'identifier_type': "OMIM gene identifier",
                        'taxon': "Homo sapiens",
                        'source': "Ensembl"
                    })
                    return new_id["primary_id"]
        elif ident["identifier_type"].lower() == "wikidata" or ident["identifier_type"].lower() == "wikidata id" or ident["identifier_type"].lower() == "wikidata identifier" or ident["identifier_type"].lower() == "wikidata accession":
            for stuff in gnomics.objects.gene.Gene.wikidata(gene):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "omim id":
                        for x in prop_dict:
                            gnomics.objects.gene.Gene.add_identifier(gene, identifier = x["mainsnak"]["datavalue"]["value"], identifier_type = "OMIM ID", language = None, source = "Wikidata")
                            gene_array.append(x["mainsnak"]["datavalue"]["value"])
        
#   UNIT TESTS
def omim_unit_tests(kegg_gene_id, ensembl_gene_id):
    kegg_gene = gnomics.objects.gene.Gene(identifier = kegg_gene_id, identifier_type = "KEGG GENE ID", language = None, taxon = "Homo sapiens", source = "KEGG")
    print("Getting OMIM gene IDs from KEGG GENE ID (%s):" % kegg_gene_id)
    print("- %s" % get_omim_gene_id(kegg_gene))
    ensembl_gene = gnomics.objects.gene.Gene(identifier = ensembl_gene_id, identifier_type = "Ensembl Gene ID", language = None, taxon = "Homo sapiens", source = "Ensembl")
    print("\nGetting OMIM gene IDs from Ensembl Gene ID (%s):" % ensembl_gene_id)
    print("- %s" % get_omim_gene_id(ensembl_gene))

#   MAIN
if __name__ == "__main__": main()