#
#
#
#
#

#
#   IMPORT SOURCES:
#       EUTILS
#           https://github.com/biocommons/eutils
#

#
#   Create instance of a gene.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

#   Import modules.
from gnomics.objects.user import User

#   Other imports.
import eutils.client
import re
import requests

#   Import sub-methods.
from gnomics.objects.gene_files.ensembl import get_ensembl_gene_id
from gnomics.objects.gene_files.entrez import get_ncbi_entrez_gene, get_ncbi_entrez_gene_id
from gnomics.objects.gene_files.hgnc import get_hgnc_gene_id, get_hgnc_gene_symbol
from gnomics.objects.gene_files.kegg import get_kegg_gene, get_kegg_gene_id
from gnomics.objects.gene_files.mine import get_flymine_gene_id, get_flymine_primary_gene_id
from gnomics.objects.gene_files.omim import get_omim_gene_id
from gnomics.objects.gene_files.pharos import get_pharos_gene_id
from gnomics.objects.gene_files.search import search
from gnomics.objects.gene_files.vega import get_vega_gene_id
from gnomics.objects.gene_files.wiki import get_arabic_wikipedia_accession, get_catalan_wikipedia_accession, get_german_wikipedia_accession, get_english_wikipedia_accession, get_spanish_wikipedia_accession, get_estonian_wikipedia_accession, get_finnish_wikipedia_accession, get_french_wikipedia_accession, get_italian_wikipedia_accession, get_japanese_wikipedia_accession, get_korean_wikipedia_accession, get_dutch_wikipedia_accession, get_polish_wikipedia_accession, get_portuguese_wikipedia_accession, get_slovenian_wikipedia_accession, get_tamil_wikipedia_accession, get_ukrainian_wikipedia_accession, get_urdu_wikipedia_accession, get_wikidata_accession, get_wikidata_object

#   Import further methods.
from gnomics.objects.interaction_objects.gene_compound import get_compounds
from gnomics.objects.interaction_objects.gene_disease import get_diseases
from gnomics.objects.interaction_objects.gene_pathway import get_pathways
from gnomics.objects.interaction_objects.gene_phenotype import get_phenotypes
from gnomics.objects.interaction_objects.gene_protein import get_proteins
from gnomics.objects.interaction_objects.gene_tissue import get_tissue_expression

#   MAIN
def main():
    gene_unit_tests()

#   GENE CLASS
class Gene:
    """
        Gene class:
        
        According to Gerstein et al. (2007), a gene is a
        "genomic sequence (DNA or RNA) directly encoding
        functional product molecules, either RNA or protein."
        
    """
    
    """
        Gene attributes:
        
        Identifier      = A particular way to identify the
                          gene in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Taxon           = The species from which the gene
                          originated (genus and species). 
                          If no such identifier is provided,
                          "Homo sapiens" is assumed.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the gene.
    def __init__(self, identifier = None, identifier_type = None, language = None, taxon = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [
                {
                    'identifier': str(identifier),
                    'language': language,
                    'identifier_type': identifier_type,
                    'taxon': taxon,
                    'source': source,
                    'name': name
                }
            ]
        
        # Initialize dictionary of gene objects.
        self.gene_objects = []
        
    # Add an identifier to a gene.
    def add_identifier(gene, identifier = None, identifier_type = None, taxon = None,  language = None, source = None, name = None):
        gene.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'taxon': taxon,
            'source': source,
            'name': name
        })
        
    # Add an object to a gene.
    def add_object(gene, obj = None, object_type = None):
        gene.gene_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Gene objects:
        
        KEGG Gene
        NCBI Entrez Gene (NCBI Gene ID)
        Wikidata Object
        
    """
    
    # Get KEGG gene object.
    # If no species is specified, Homo sapiens (HSA) is assumed.
    def kegg_gene(gene, taxon = "Homo sapiens"):
        return get_kegg_gene(gene, taxon = taxon)
    
    # Get NCBI Entrez gene object.
    def ncbi_entrez_gene(gene, taxon = "Homo sapiens"):
        return get_ncbi_entrez_gene(gene, taxon = taxon)
    
    # Get Wikidata object.
    def wikidata(gene):
        return get_wikidata_object(gene)
    
    """
        Gene identifiers:
        
        Ensembl gene identifier
        HGNC gene identifier
        KEGG gene identifier
        NCBI gene identifier (Entrez)
        NCBI protein identifier
        OMIM identifier
        Pharos (Tchem) identifier   
        UniProt identifier
        Vega gene identifier
        Wikidata accession
        
    """
    
    # Return all identifiers.
    def all_identifiers(gene, taxon = "Homo sapiens", user = None):
        Gene.ensembl_gene_id(gene, taxon = taxon)
        Gene.flymine_gene_id(gene)
        Gene.flymine_primary_gene_id(gene)
        Gene.hgnc_gene_id(gene)
        Gene.hgnc_gene_symbol(gene)
        Gene.ncbi_entrez_gene_id(gene, taxon = taxon)
        Gene.omim_id(gene)
        Gene.pharos_gene_id(gene)
        Gene.kegg_gene_id(gene)
        Gene.vega_gene_id(gene, taxon = taxon)
        Gene.wikidata_accession(gene)
        return gene.identifiers
    
    # Returns Ensembl gene identifier.
    def ensembl_gene_id(gene, taxon = "Homo sapiens"):
        return get_ensembl_gene_id(gene, taxon = taxon)
    
    # Returns FlyMine gene identifier.
    def flymine_gene_id(gene):
        return get_flymine_gene_id(gene)
    
    # Returns primary FlyMine gene identifier.
    def flymine_primary_gene_id(gene):
        return get_flymine_primary_gene_id(gene)
    
    # Returns HGNC gene identifier.
    def hgnc_gene_id(gene):
        return get_hgnc_gene_id(gene)
    
    # Returns HGNC gene symbol.
    def hgnc_gene_symbol(gene):
        return get_hgnc_gene_symbol(gene)
        
    # Returns NCBI gene identifier.
    def ncbi_entrez_gene_id(gene, taxon = "Homo sapiens"):
        return get_ncbi_entrez_gene_id(gene, taxon = taxon)
    
    # Returns OMIM gene identifier.
    def omim_id(gene):
        return get_omim_gene_id(gene)
    
    # Returns KEGG gene identifier.
    def kegg_gene_id(gene):
        return get_kegg_gene_id(gene)
    
    # Returns Pharos (Tchem) identifier.
    def pharos_gene_id(gene):
        return get_pharos_gene_id(gene)
    
    # Returns Vega gene identifier.
    def vega_gene_id(gene, taxon = "Homo sapiens"):
        return get_vega_gene_id(gene, taxon = taxon)
    
    # Returns Wikidata accession.
    def wikidata_accession(gene):
        return get_wikidata_accession(gene)
    
    """
        Interaction objects:
        
        Compounds
        Diseases
        Pathways
        Taxa
        Tissues
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(gene, user = None):
        interaction_obj = {}
        interaction_obj["Compounds"] = Gene.compounds(gene)
        interaction_obj["Diseases"] = Gene.diseases(gene)
        interaction_obj["Pathways"] = Gene.pathways(gene)
        interaction_obj["Phenotypes"] = Gene.phenotypes(gene)
        interaction_obj["Proteins"] = Gene.proteins(gene)
        print(interaction_obj)
        return interaction_obj
    
    # Get compounds.
    def compounds(gene):
        return get_compounds(gene)
    
    # Get diseases.
    def diseases(gene):
        return get_diseases(gene)
    
    # Get drug interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def drug_interactions(gene, source = "dgidb", interaction_sources = None, interaction_types = None, drug_types = None, source_trust_levels = None):
        if source == "dgidb":
            server = "http://dgidb.genome.wustl.edu"
            ext = "/api/v1/interactions.json?genes=" + gene.hgnc_gene_id
            
            if interaction_sources is not None:
                ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
            if interaction_types is not None:
                ext = ext + (",".join(interaction_types)).replace(" ", "%20")
            if drug_types is not None:
                ext = ext + (",".join(drug_types)).replace(" ", "%20")
            if source_trust_levels is not None:
                ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

            r = requests.get(server+ext, headers={"Content-Type": "application/json"})

            if not r.ok:
                r.raise_for_status()
                sys.exit()

            decoded = r.json()

            return decoded
    
    # Get pathways.
    def pathways(gene):
        return get_pathways(gene)
    
    # Get phenotypes.
    def phenotypes(gene):
        return get_phenotypes(gene)
        
    # Get proteins.
    def proteins(gene, taxon = "Homo sapiens"):
        return get_proteins(gene, taxon = taxon)
       
    # Get tissue expression.
    def tissue_expression(gene):
        return get_tissue_expression(gene)
    
    """
        Gene properties:
        
        Amino acid FASTA [TODO: move to protein???]
        Chromosomal position
        Definition
        Description
        Genomic references
        Map location
        Motifs
        NCBI BLAST
        Nucleotide FASTA
        Orthologs
        Pathway identifiers [move to gene_pathway.py]
        Pathways [move to gene_pathway.py]
        Pfam motifs
        Raw nucleotide sequence
        Type
        
    """
    
    def all_properties(gene, user = None):
        property_dict = {}
        return property_dict
    
    # Get definition.
    def definition(gene, source = "kegg"):
        if source.lower() == "kegg":
            return Gene.kegg_gene(gene)["DEFINITION"]
    
    # Get description.
    def description(gene, source = "ncbi"):
        for gene_obj in Gene.gene_objects(gene):
            if 'object_type' in gene_obj:
                if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['species'].lower() == species):
                    return gene_obj['object'].description
    
    # Get amino acid FASTA.
    def amino_acid_fasta(gene, source = "kegg"):
        if source.lower() == "kegg":
            first_line = ">" + str(Gene.kegg_gene_id(gene)) + "\n"
            return first_line + amino_acid_sequence
        elif source.lower() == "uniprot":
            res = u.searchUnitProtId(Gene.uniprot_id(gene), frmt="fasta")
            return res
    
    # Get genomic references.
    def genomic_references(gene, source = "ncbi"):
        for gene_obj in Gene.gene_objects(gene):
            if 'object_type' in gene_obj:
                if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['species'].lower() == species):
                    return sorted([(r.acv, r.label) for r in gene_obj['object'].references])
    
    # Get motifs.
    def motifs(gene, source = "kegg"):
        if source.lower() == "kegg":
            return Gene.kegg_gene(gen)["MOTIF"]
        
    # Get nucleotide FASTA.
    def nucleotide_fasta(gene, source = "kegg"):
        if source.lower() == "kegg":
            first_line = ">" + str(Gene.kegg_gene_id(gene)) + "\n"
            return first_line + nucleotide_sequence
    
    # Get Pfam motifs.
    def pfam_motifs(gene, source = "kegg"):
        if source.lower() == "kegg":
            return Gene.motifs(gene, source = "kegg")["Pfam"]
        
    # Get position (chromosomal).
    def position(gene, source = "kegg"):
        if source.lower() == "kegg":
            return Gene.kegg_gene(gene)["POSITION"]
    
    # Get raw amino acid sequence.
    def amino_acid_sequence(gene, source = "kegg"):
        if source.lower() == "kegg":
            return "".join(Gene.kegg_gene(gene)["AASEQ"].split())
    
    # Get map location.
    def map_location(gene, source = "ncbi"):
        for gene_obj in Gene.gene_objects(gene):
            if 'object_type' in gene_obj:
                if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['taxon'].lower() == taxon):
                    return gene_obj['object'].maploc
    
    # Get raw nucleotide sequence.
    def nucleotide_sequence(gene, source = "kegg"):
        if source.lower() == "kegg":
            return "".join(Gene.kegg_gene(gene)["NTSEQ"].split())
        
    # Get orthologs.
    # Ensembl function detailed here:
    # https://rest.ensembl.org/documentation/info/homology_ensemblgene
    def orthologs(gene, source = "ensembl"):
        if source.lower() == "ensembl":
            server = "https://rest.ensembl.org"
            ext = "/homology/id/" + Gene.ensembl_id(gene) + "?"
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = r.json()
            return decoded
        
    # Get gene type.
    def gene_type(gene, source = "ncbi"):
        for gene_obj in Gene.gene_objects(gene):
            if 'object_type' in gene_obj:
                if (gene_obj['object_type'].lower() == 'ncbi entrez gene') and (gene_obj['taxon'].lower() == taxon):
                    return gene_obj['object'].type
        
    """
        Gene URLs:
        
        KEGG gene URL
        OMIM URL
        UniProt URL
        
    """
    
    # Get KEGG gene URL.
    def kegg_gene_url(gene):
        base_url = "http://www.kegg.jp/entry/" 
        gene_array = re.findall(r"[^\W\d_]+|\d+", Gene.kegg_gene_id(gene))
        final_gene_from_array = gene_array[0] + ":" + gene_array[1]
        return base_url + final_gene_from_array + ":" + kegg_identifier
    
    # Get OMIM URL.
    def omim_url(gene):
        base_url = "https://www.omim.org/entry/"
        return base_url + Gene.omim_id(gene)
    
    # Get UniProt URL.
    def uniprot_url(gene):
        base_url = "http://www.uniprot.org/uniprot/"
        return base_url + Gene.uniprot_id(gene)
    
    """
        Auxiliary functions:
        
        NCBI BLAST
        Search
    """
    
    # NCBI BLAST from gene sequence.
    # Gene MUST be just the sequence, without a header
    # and without newlines or spaces.
    #
    # Example programs:
    # 'blastp', 'blastn', 'blastx', 'tblastn', 'tblastx'
    #
    # Possible stypes:
    # (Not sure) 'protein', 'nucleotide'
    def ncbi_blast(gene, user, program = "blastp", sequence = "amino acid", database = "uniprotkb", taxon = None):
        s = NCBIblast(verbose = False)
        if sequence == "nucleotide":
            jobid = s.run(program = program, sequence = Gene.nucleotide_sequence(gene), stype = "nucleotide", database = database, email = user.email)
            if taxon == None:
                return s.getResult(jobid, "out")[0:1000]
            elif taxon == "Homo sapiens":
                return [x for x in s.getResult(jobid, "out").split("\n") if "HUMAN" in x]
        elif sequence == "amino acid":
            jobid = s.run(program = program, sequence = Gene.amino_acid_sequence(gene), stype = "protein", database = database, email = user.email)
            if taxon == None:
                return s.getResult(jobid, "out")[0:1000]
            elif taxon == "Homo sapiens":
                return [x for x in s.getResult(jobid, "out").split("\n") if "HUMAN" in x]
        
    """
        External files:
        
        FASTA file
    """
    
    def fasta_file():               # This is for a single sequence.
        print("NOT FUNCTIONAL.")
        
    def group_fasta_file():         # This is for multiple sequences
        print("NOT FUNCTIONAL.")
        
    """
        Auxiliary functions:
        
        Search
        
    """
    
    def search(query, user = None, search_type = None, taxon = "Homo sapiens", source = "ensembl"):
        return search(query, user = user, search_type = search_type, taxon = taxon, source = source)

#   UNIT TESTS
def gene_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()