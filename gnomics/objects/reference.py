#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIBGEN
#           https://github.com/etlapale/bibgen
#       BIOPYTHON
#           http://biopython.org/
#       METAPUB
#           https://pypi.python.org/pypi/metapub
#       PUBMED-LOOKUP
#           https://pypi.python.org/pypi/pubmed-lookup
#

#
#   Create instance of a reference.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS
from gnomics.objects.user import User

# Import sub-methods.
from gnomics.objects.reference_files.chembl import get_chembl_obj, get_chembl_id
from gnomics.objects.reference_files.citation import parse_citation
from gnomics.objects.reference_files.doi import get_doi
from gnomics.objects.reference_files.pii import get_pii
from gnomics.objects.reference_files.pmc import get_pmc_id
from gnomics.objects.reference_files.pubmed import get_pmid
from gnomics.objects.reference_files.search import eutils_search, google_scholar_search, openlibrary_search
from gnomics.objects.reference_files.url import extract_urls

#   Import further methods.
from gnomics.objects.interaction_objects.reference_variation import get_variations
from gnomics.objects.interaction_objects.reference_patent import get_patents
from gnomics.objects.interaction_objects.reference_pathway import get_pathways

# Other imports.
from Bio import Entrez
from Bio.Entrez import efetch, read
from metapub import PubMedFetcher
from pubmed_lookup import PubMedLookup, Publication
import scholarly

#   MAIN
def main():
    print("NOT FUNCTIONAL.")
    
#   REFERENCE CLASS
class Reference(object):
    """
        Reference class
    """
    
    """
        Reference attributes:
        
        Identifier      = A particular way to identify the
                          reference in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the reference.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        # An identifier could be a PMID (PubMED ID) for example.
        self.identifiers = [
            {
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of reference objects.
        self.reference_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a reference.
    def add_identifier(reference, identifier = None, identifier_type = None, language = None, source = None, name = None):
        reference.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
    
    """
        Reference objects
        
        ChEMBL Document Object
        DOI Article
        PMC ID Article
        PMID Article
        PubTator Object
    """
    
    # Get ChEMBL document object.
    def chembl_document(ref):
        return get_chembl_obj(ref)
    
    def doi_article(ref):
        fetch = PubMedFetcher()
        article = fetch.article_by_doi(Reference.doi(ref))
        
    def pmcid_article(ref):
        fetch = PubMedFetcher()
        article = fetch.article_by_pmcid(Reference.pmcid(ref))
    
    # Get publication object from PubMed ID.
    # Example of what this outputs can
    # be seen here:
    # https://pypi.python.org/pypi/pubmed-lookup
    def pmid_article(ref, user = None):
        if user:
            url = "http://www.ncbi.nlm.nih.gov/pubmed/" + str(Reference.pmid(ref))
            lookup = PubMedLookup(url, user.email)
            publication = Publication(lookup)
            return publication
        else:
            fetch = PubMedFetcher()
            article = fetch.article_by_pmid(Reference.pmid(ref))
            return article
    
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
    def pubtator(pmid, concept="BioConcept", format="JSON"):
        pubtator_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + str(concept) + "/" + str(pmid) + "/" + str(format) + "/"
    
    """
        Reference identifiers
        
        ChEMBL ID
        DOI
        PII
        PMC ID
        PMID (PubMed ID)
    """
    
    # Return all identifiers.
    def all_identifiers(reference, user = None):
        Reference.chembl_id(reference)
        Reference.doi(reference)
        Reference.pii(reference)
        Reference.pmc_id(reference)
        Reference.pmid(reference)
        return reference.identifiers
    
    # Get ChEMBL ID.
    def chembl_id(ref):
        return get_chembl_id(ref)
    
    # Get DOI.
    def doi(ref):
        return get_doi(ref)
    
    # Get PII.
    def pii(ref):
        return get_pii(ref)
    
    # Get PMC ID.
    def pmc_id(ref):
        return get_pmc(ref)
    
    # Get PubMed ID.
    def pmid(ref):
        return get_pmid(ref)
                
    """
        Reference properties
        
    """
    
    def all_properties(reference, user = None):
        property_dict = {}
        return property_dict
    
    # Returns title.
    def title(reference, user = None):
        return Reference.pmid_article(reference, user = user).title
    
    # Returns authors.
    def authors(reference, user = None):
        return Reference.pmid_article(reference, user = user).authors
    
    # Return author first and middle name.
    def first_name(source, full_name):
        print("NOT FUNCTIONAL.")
    
    # Return author last name.
    def last_name(source, full_name):
        print("NOT FUNCTIONAL.")
    
    # Returns journal.
    def journal(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.journal
    
    # Returns year.
    def year(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.year
    
    # Returns month.
    def month(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.month
    
    # Returns day.
    def day(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.day
    
    # Returns URL.
    def url(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.url
    
    # Returns PubMed URL.
    def pubmed_url(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.pubmed_url
    
    # Returns citation.
    def cite(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.cite()
    
    # Returns mini-citation.
    def mini_cite(reference, user = None):
        return Reference.pmid_article(reference, user = user).pmid_article.cite_mini()
    
    # Returns abstract.
    def abstract(ref, user = None):
        return repr(Reference.pmid_article(ref, user = user).abstract)
    
    """
        Reference URLs
        
    """
    
    # Returns MeSH URL.
    def mesh_url(source, mesh_uid):
        base_url = "https://meshb.nlm.nih.gov/record/ui?ui="
        return base_url + mesh_uid
    
    """
        Auxiliary functions
        
        Search
    """
    
    # Extract URLs.
    def extract_urls(text):
        return extract_urls(text)
    
    # Parse citation.
    def parse_citation(citation, score_threshold = None, normalized_score_threshold = 100):
        return parse_citation(citation, score_threshold = score_threshold, normalized_score_threshold = normalized_score_threshold)
        
    # Perform basic reference search.
    def search(source = "PubMed", level = "basic", db = "PubMed", query = None, unlabeled_string = None, affiliation = None, article_identifier = None, all_fields = None, author = None, author_identifier = None, book = None, corporate_author = None, create_date = None, completion_date = None, conflict_of_interest = None, ec_rn_number = None, editor = None, entrez_date = None, filter_citations = None, first_author_name = None, full_author_name = None, full_investigator_name = None, grant_number = None, investigator = None, isbn = None, issue = None, journal = None, language = None, last_author = None, location_id = None, mesh_date = None, mesh_major_topic = None, mesh_subheadings = None, mesh_terms = None, modification_date = None, nlm_unique_id = None, other_term = None, owner = None, pagination = None, personal_name_as_subject = None, pharmacological_action = None, place_of_publication = None, pmid = None, publisher = None, publication_date = None, publication_type = None, retmax = None, retmode = None, secondary_source_id = None, sort = None, subset = None, supplementary_concept = None, text_words = None, title = None, title_abstract = None, transliterated_title = None, uid = None, volume = None, raw = False, exact = False, user = None):
        if source == "PubMed" and level == "complex":
            return eutils_search(db = db, retmode = retmode, retmax = retmax, sort = sort, unlabeled_string = unlabeled_string, affiliation = affiliation, article_identifier = article_identifier, all_fields = all_fields, author = author, author_identifier = author_identifier, book = book, corporate_author = corporate_author, create_date = create_date, completion_date = completion_date, conflict_of_interest = conflict_of_interest, ec_rn_number = ec_rn_number, editor = editor, entrez_date = entrez_date, filter_citations = filter_citations, first_author_name = first_author_name, full_author_name = full_author_name, full_investigator_name = full_investigator_name, grant_number = grant_number, investigator = investigator, isbn = isbn, issue = issue, journal = journal, language = language, last_author = last_author, location_id = location_id, mesh_date = mesh_date, mesh_major_topic = mesh_major_topic, mesh_subheadings = mesh_subheadings, mesh_terms = mesh_terms, modification_date = modification_date, nlm_unique_id = nlm_unique_id, other_term = other_term, owner = owner, pagination = pagination, personal_name_as_subject = personal_name_as_subject, pharmacological_action = pharmacological_action, place_of_publication = place_of_publication, pmid = pmid, publisher = publisher, publication_date = publication_date, publication_type = publication_type, secondary_source_id = secondary_source_id, subset = subset, supplementary_concept = supplementary_concept, text_words = text_words, title = title, title_abstract = title_abstract, transliterated_title = transliterated_title, uid = uid, volume = volume, raw = raw, exact = exact)
        elif source == "PubMed" and level == "basic":
            # Use 'unlabeled_string' or 'query' here.
            # This function already takes completed
            # PubMed queries as strings (with
            # various connectors and constructors).
            if unlabeled_string:
                fetch = PubMedFetcher()
                pubmed_id_list = fetch.pmids_for_query(unlabeled_string)
                ref_list = []
                for pubmed_id in pubmed_id_list:
                    article = fetch.article_by_pmid(pubmed_id) # Need a faster way to get titles...
                    temp_ref = Reference(identifier = str(pubmed_id), identifier_type = "PubMed ID", source = "PubMed", name = article.title)
                    ref_list.append(temp_ref)
                return ref_list
            elif query:
                fetch = PubMedFetcher()
                pubmed_id_list = fetch.pmids_for_query(query)
                print(pubmed_id_list)
                ref_list = []
                for pubmed_id in pubmed_id_list:
                    article = fetch.article_by_pmid(pubmed_id) # Need a faster way to get titles...
                    temp_ref = Reference(identifier = str(pubmed_id), identifier_type = "PubMed ID", source = "PubMed", name = article.title)
                    ref_list.append(temp_ref)
                print(ref_list)
                return ref_list
        elif source == "Google":
            print("NOT FUNCTIONAL.")
            return google_scholar_search(unlabeled_string)
        elif source == "OpenLibrary":
            return openlibrary_search(unlabeled_string)
        
            
    # Get PubMed ID from citation.
    #
    # At least 3 of the 5 (preferably 4 out of 5) should
    # be included.
    #
    # NLM title abbreviation (ISO abbreviation) should
    # be used for journal title.
    def pmids_from_citation(author_last_name = None, year = None, volume = None, first_page = None, journal_title = None):
        fetch = PubMedFetcher()
        return fetch.pmids_from_citation(aulast = author_last_name, year = year, volume = volume, first_page = first_page, jtitle = journal_title)
    
    # Get MeSH terms from PubMed ID.
    def get_mesh_from_pmid(ref, user):
        # Continue from here: https://stackoverflow.com/questions/13652230/cant-get-entrez-to-return-mesh-terms-using-biopython
        Entrez.email = user.email
        handle = efetch(db = "pubmed", id = str(Reference.pmid(ref)), retmode = "xml")
        xml_data = read(handle)[0]
        # Skips articles without MeSH terms
        if u'MeshHeadingList' in xml_data["MedlineCitation"]:
            for mesh in xml_data["MedlineCitation"][u'MeshHeadingList']:
                major = "N"
                qualifiers = mesh[u'QualifierName']
                if len(qualifiers) > 0:
                    major = str(qualifiers[0].attributes.items()[0][1])
                descr = mesh[u'DescriptorName']
                name = descr.title()
    
    """
        External files
        
    """
    
#   UNIT TESTS
    
#   MAIN
if __name__ == "__main__": main()