#!/usr/bin/env python

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
from gnomics.objects.reference_files.amazon import get_asin
from gnomics.objects.reference_files.chembl import get_chembl_obj, get_chembl_id
from gnomics.objects.reference_files.citation import parse_citation
from gnomics.objects.reference_files.doi import get_doi, get_doi_object
from gnomics.objects.reference_files.dpla import get_dpla_uuid
from gnomics.objects.reference_files.elsevier import get_eid, sciencedirect_search
from gnomics.objects.reference_files.goodreads import get_goodreads_id
from gnomics.objects.reference_files.google import get_google_books_multiple_references, get_google_books_id
from gnomics.objects.reference_files.gutenberg import get_project_gutenberg_id
from gnomics.objects.reference_files.hades import get_hades_collection_guide_id, get_hades_struc_id
from gnomics.objects.reference_files.isbn import get_isbn10, get_isbn13
from gnomics.objects.reference_files.isbndb import get_isbndb_books, get_isbndb_book_id
from gnomics.objects.reference_files.librarything import get_librarything_id
from gnomics.objects.reference_files.lccn import get_lccn
from gnomics.objects.reference_files.oclc import classify
from gnomics.objects.reference_files.openlibrary import openlibrary_books_api, get_openlibrary_id
from gnomics.objects.reference_files.pdf import get_pdf_url, download_pdf
from gnomics.objects.reference_files.pii import get_pii
from gnomics.objects.reference_files.pmc import get_pmc_id
from gnomics.objects.reference_files.pubmed import get_pmid
from gnomics.objects.reference_files.search import eutils_search, google_scholar_search, openlibrary_search
from gnomics.objects.reference_files.springer import get_springer_journal_id
from gnomics.objects.reference_files.wiki import get_wikidata_accession, get_wikidata_object

#   Import further methods.
from gnomics.objects.interaction_objects.reference_person import get_authors
from gnomics.objects.interaction_objects.reference_patent import get_patents
from gnomics.objects.interaction_objects.reference_pathway import get_pathways
from gnomics.objects.interaction_objects.reference_variation import get_variations

# Other imports.
from Bio import Entrez
from Bio.Entrez import efetch, read
from metapub import PubMedFetcher
import metapub
from pubmed_lookup import PubMedLookup, Publication
import timeit

#   MAIN
def main():
    reference_unit_tests()
    
#   REFERENCE CLASS
class Reference(object):
    """
        Reference class
        
        A reference is any kind of citation to a published
        or unpublished source.
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
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        # An identifier could be a PMID (PubMED ID) for example.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of reference objects.
        self.reference_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a reference.
    def add_identifier(reference, identifier=None, identifier_type=None, language=None, source=None, name=None):
        reference.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a reference.
    def add_object(reference, obj=None, object_type=None):
        reference.reference_objects.append({
            'object': obj,
            'object_type': object_type
        })
    
    """
        Reference objects
        
        ChEMBL Document Object
        DOI Article
        Google Book
        PMC ID Article
        PMID Article
        PubTator Object
        Wikidata Object
    """
    
    # Get ChEMBL document object.
    def chembl_document(ref, user=None):
        return get_chembl_obj(ref)
    
    # Get DOI article.
    def doi_article(ref, user=None):
        article_array = []
        fetch = PubMedFetcher()
        for doi in Reference.doi(ref):
            article = fetch.article_by_doi(doi)
            article_array.append(article)
        return article
    
    # Get DOI object.
    def doi_object(ref, user=None):
        return get_doi_object(ref)
    
    # Get Google Book object.
    def google_book(ref, user=None):
        return get_google_books_multiple_references(ref)
       
    # Get ISBNdb object.
    def isbndb(ref, user=None):
        return get_isbndb_books(ref, user=user)
    
    # Get OpenLibrary object.
    def openlibrary(ref, user=None, jscmd=False):
        return openlibrary_books_api(ref, user=user, jscmd=True)
        
    # Get PMCID article.
    def pmcid_article(ref, user=None):
        article_array = []
        fetch = PubMedFetcher()
        for pmcid in Reference.pmcid(ref):
            article = fetch.article_by_pmcid(pmcid)
            article_array.append(article)
        return article
    
    # Get publication object from PubMed ID.
    # Example of what this outputs can
    # be seen here:
    # https://pypi.python.org/pypi/pubmed-lookup
    def pmid_article(ref, user=None):
        article_array = []
        if user:
            if user.email is not None:
                for pmid in Reference.pmid(ref):
                    url = "http://www.ncbi.nlm.nih.gov/pubmed/" + str(pmid)
                    lookup = PubMedLookup(url, user.email)
                    publication = Publication(lookup)
                    article_array.append(publication)

        fetch = PubMedFetcher()
        for pmid in Reference.pmid(ref):
            article = fetch.article_by_pmid(pmid)
            article_array.append(article)
                
        return article_array
    
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
    def pubtator(pmid, concept="BioConcept", format="JSON", user=None):
        pubtator_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + str(concept) + "/" + str(pmid) + "/" + str(format) + "/"
        
    # Get Wikidata object.
    def wikidata(ref, user=None):
        return get_wikidata_object(ref)
    
    """
        Reference identifiers
        
        Amazon Standard Identification Number (ASIN)
        ChEMBL ID
        DOI
        DPLA UUID
        EID (Elsevier ID)
        Goodreads ID
        Google Books ID
        Hades Collection Guide ID
        Hades Struc ID
        ISBN-10
        ISBN-13
        Library of Congress Control Number (LCCN)
        OpenLibrary ID (OLID)
        PII
        PMC ID
        PMID (PubMed ID)
        Project Gutenberg ID
        Wikidata Accession
    """
    
    # Return all identifiers.
    def all_identifiers(reference, user=None):
        Reference.asin(reference, user=user)
        Reference.chembl_id(reference, user=user)
        Reference.doi(reference, user=user)
        Reference.dpla_uuid(reference, user=user)
        Reference.eid(reference, user=user)
        Reference.goodreads_id(reference, user=user)
        Reference.google_books_id(reference, user=user)
        Reference.hades_collection_guide_id(reference, user=user)
        Reference.hades_struc_id(reference, user=user)
        Reference.isbn10(reference, user=user)
        Reference.isbn13(reference, user=user)
        Reference.lccn(reference, user=user)
        Reference.openlibrary_id(reference, user=user)
        Reference.pii(reference, user=user)
        Reference.pmc_id(reference, user=user)
        Reference.pmid(reference, user=user)
        Reference.project_gutenberg_id(reference, user=user)
        Reference.wikidata_accession(reference, user=user)
        return reference.identifiers
    
    # Get ASIN.
    def asin(ref, user=None):
        return get_asin(ref)
    
    # Get ChEMBL ID.
    def chembl_id(ref, user=None):
        return get_chembl_id(ref)
    
    # Get DOI.
    def doi(ref, user=None):
        return get_doi(ref)
    
    # Get DPLA UUID.
    def dpla_uuid(ref, user=None):
        return get_dpla_uuid(ref)
    
    # Get EID.
    def eid(ref, user=None):
        return get_eid(ref)
    
    # Get Goodreads ID.
    def goodreads_id(ref, user=None):
        return get_goodreads_id(ref)
    
    # Get Google Books ID.
    def google_books_id(ref, user=None):
        return get_google_books_id(ref)
    
    # Get Hades Collection Guide ID.
    def hades_collection_guide_id(ref, user=None):
        return get_hades_collection_guide_id(ref)
    
    # Get Hades Struc ID.
    def hades_struc_id(ref, user=None):
        return get_hades_struc_id(ref)
    
    # Get LCCN.
    def lccn(ref, user=None):
        return get_lccn(ref)
    
    # Get OpenLibrary ID.
    def openlibrary_id(ref, user=None):
        return get_openlibrary_id(ref, user=user)
    
    # Get ISBN-10.
    def isbn10(ref, user=None):
        return get_isbn10(ref)
    
    # Get ISBN-13.
    def isbn13(ref, user=None):
        return get_isbn13(ref)
    
    # Get ISBNdb Book ID.
    def isbndb_book_id(ref, user=None):
        return get_isbndb_book_id(ref, user=user)
    
    # Get PII.
    def pii(ref, user=None):
        return get_pii(ref)
    
    # Get PMC ID.
    def pmc_id(ref, user=None):
        return get_pmc_id(ref)
    
    # Get PubMed ID.
    def pmid(ref, user=None):
        return get_pmid(ref)
    
    # Get Project Gutenberg ID.
    def project_gutenberg_id(ref, user=None):
        return get_project_gutenberg_id(ref)
    
    # Get Wikidata Accession.
    def wikidata_accession(ref, user=None):
        return get_wikidata_accession(ref)
    
    """
        Interaction objects:
        
        Authors
        Patents
        Pathways
        Variations
    """
    
    # Return interaction objects.
    def all_interaction_objects(reference, user=None):
        interaction_obj = {}
        interaction_obj["Authors"] = Reference.authors(reference, user=user)
        interaction_obj["Patents"] = Reference.patents(reference, user=user)
        interaction_obj["Pathways"] = Reference.pathways(reference, user=user)
        interaction_obj["Variations"] = Reference.variations(reference, user=user)
        return interaction_obj
    
    # Return authors.
    def authors(reference, user=None):
        return get_authors(reference, user=user)
    
    # Return patents.
    def patents(reference, user=None):
        return get_patents(reference, user=user)
    
    # Return pathways.
    def pathways(reference, user=None):
        return get_pathways(reference, user=user)
    
    # Return variations.
    def variations(reference, user=None):
        return get_variations(reference, user=user)
                
    """
        Reference properties
        
        Abstract
        Citation
        Citation (Mini)
        Day
        DDC (Dewey Decimal Classification)
        Journal
        LCC (Library of Congress Classification)
        Month
        Pages
        Publisher
        Reference type
        Title
        Volume
        Year
    """
    
    def all_properties(reference, user=None):
        property_dict = {}
        property_dict["Abstract"] = Reference.abstract(reference, user=user)
        property_dict["Citation"] = Reference.cite(reference, user=user)
        property_dict["Mini-Citation"] = Reference.mini_cite(reference, user=user)
        property_dict["Day"] = Reference.day(reference, user=user)
        property_dict["Journal"] = Reference.journal(reference, user=user)
        property_dict["DDC"] = Reference.ddc(reference, user=user)
        property_dict["LCC"] = Reference.lcc(reference, user=user)
        property_dict["Month"] = Reference.month(reference, user=user)
        property_dict["Title"] = Reference.title(reference, user=user)
        property_dict["Pages"] = Reference.pages(reference, user=user)
        property_dict["Publisher"] = Reference.publisher(reference, user=user)
        property_dict["Type"] = Reference.reference_type(reference, user=user)
        property_dict["Volume"] = Reference.volume(reference, user=user)
        property_dict["Year"] = Reference.year(reference, user=user)
        return property_dict
    
    # Returns publication date.
    def publication_date(ref, user=None):
        prop_array = []
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.append(obj["publication_date"])
        return prop_array
    
    # Returns by statement.
    def by_statement(ref, user=None):
        prop_array = []
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.append(obj["by_statement"])
        return prop_array
    
    # Returns number of pages.
    def number_of_pages(ref, user=None):
        prop_array = []
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.append(obj["number_of_pages"])
        return prop_array
    
    # Returns notes.
    def notes(ref, user=None):
        prop_array = []
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.append(obj["notes"])
        return prop_array
    
    # Returns weight.
    def weight(ref, user=None):
        prop_array = []
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.append(obj["weight"])
        return prop_array
    
    # Returns subject(s).
    def subject(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "subject" in article["message"]:
                    for x in article["message"]["subject"]:
                        prop_array.append(x)
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.extend(obj["subjects"])
        return prop_array
    
    # Returns title.
    def title(ref, user=None):
        title_array = []
        for article in Reference.pmid_article(ref, user=user):
            title_array.append(article.title)
        for doc in Reference.chembl_document(ref, user=user):
            title_array.append(doc["title"])
        for obj in Reference.google_book(ref, user=user):
            title_array.append(obj["Title"])
        for obj in Reference.openlibrary(ref, user=user):
            title_array.append(obj["title"])
        return title_array
    
    # Returns subtitle.
    def subtitle(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "subtitle" in article["message"]:
                    for x in article["message"]["subtitle"]:
                        prop_array.append(x)
        return prop_array
    
    # Returns journal.
    def journal(ref, user=None):
        journal_array = []
        for article in Reference.pmid_article(ref, user=user):
            try:
                journal_array.append(article.journal)
            except:
                print("Something went wrong.")
        for doc in Reference.chembl_document(ref, user=user):
            journal_array.append(doc["journal"])
        return journal_array
    
    # Returns journal full title.
    def journal_full_title(ref, user=None):
        journal_array = []
        for doc in Reference.chembl_document(ref, user=user):
            journal_array.append(doc["journal_full_title"])
        return journal_array
    
    # Returns Springer Journal ID.
    def springer_journal_id(ref, user=None):
        journal_array = []
        for journal_name in journal(ref, user=user):
            journal_array.extend(get_springer_journal_id(journal_name))
        return journal_array
    
    # Returns Dewey Decimal Classification (DDC).
    def ddc(reference, user=None):
        prop_array = []
        for classification in classify(reference, return_type="ddc"):
            if classification not in prop_array:
                prop_array.append(classification)
        for obj in Reference.openlibrary(reference, user=user):
            prop_array.append(obj["ddc"])
        return prop_array
    
    # Returns Library of Congress Classification (LCC).
    def lcc(reference, user=None):
        prop_array = []
        for classification in classify(reference, return_type="lcc"):
            if classification not in prop_array:
                prop_array.append(classification)
        for obj in Reference.openlibrary(reference, user=user):
            prop_array.append(obj["lcc"])
        return prop_array
    
    # Returns year.
    def year(ref, user=None):
        prop_array = []
        for article in Reference.pmid_article(ref, user=user):
            try:
                prop_array.append(article.year)
            except:
                print("Something went wrong.")
        for doc in Reference.chembl_document(ref, user=user):
            title_array.append(doc["year"])
        for obj in Reference.google_book(ref, user=user):
            title_array.append(obj["Year"])
        return prop_array
    
    # Returns month.
    def month(reference, user=None):
        prop_array = []
        for article in Reference.pmid_article(reference, user=user):
            try:
                prop_array.append(article.month)
            except:
                print("Something went wrong.")
        return prop_array
    
    # Returns day.
    def day(reference, user=None):
        prop_array = []
        for article in Reference.pmid_article(reference, user=user):
            try:
                prop_array.append(article.day)
            except:
                print("Something went wrong.")
        return prop_array
    
    # Returns citation.
    def cite(reference, user=None):
        prop_array = []
        for article in Reference.pmid_article(reference, user=user):
            try:
                prop_array.append(article.cite())
            except:
                print("Something went wrong.")
        return prop_array
    
    # Returns mini-citation.
    def mini_cite(reference, user=None):
        prop_array = []
        for article in Reference.pmid_article(reference, user=user):
            try:
                prop_array.append(article.cite_mini())
            except:
                print("Something went wrong.")
        return prop_array
    
    # Returns abstract.
    def abstract(ref, user=None):
        prop_array = []
        for article in Reference.pmid_article(ref, user=user):
            try:
                prop_array.append(repr(article.abstract))
            except:
                print("Something went wrong.")
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["abstract"])
        return prop_array
    
    # Returns publisher(s).
    def publisher(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "publisher" in article["message"]:
                    prop_array.append(article["message"]["publisher"])
        for obj in Reference.google_book(ref, user=user):
            prop_array.append(obj["Publisher"])
        for obj in Reference.openlibrary(ref, user=user):
            prop_array.extend(obj["Publishers"])
        return prop_array
    
    # Returns reference type.
    def reference_type(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "type" in article["message"]:
                    prop_array.append(article["message"]["type"])
        return prop_array
    
    # Returns pages.
    def pages(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "page" in article["message"]:
                    prop_array.append(article["message"]["page"])
        return prop_array
    
    # Returns first page.
    def last_page(ref, user=None):
        prop_array = []
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["first_page"])
        return prop_array
    
    # Returns last page.
    def last_page(ref, user=None):
        prop_array = []
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["last_page"])
        return prop_array
    
    # Returns volume.
    def volume(ref, user=None):
        prop_array = []
        for article in Reference.doi_object(ref, user=user):
            if "message" in article:
                if "volume" in article["message"]:
                    prop_array.append(article["message"]["volume"])
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["volume"])
        return prop_array
    
    # Returns issue.
    def issue(ref, user = None):
        prop_array = []
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["issue"])
        return prop_array
    
    # Returns document type.
    def document_type(ref, user=None):
        prop_array = []
        for doc in Reference.chembl_document(ref, user=user):
            prop_array.append(doc["doc_type"])
        return prop_array
    
    """
        Reference URLs
        
    """
    
    # Return links.
    def all_urls(reference, user=None):
        url_dict = {}
        return url_dict
    
    # Returns URL.
    def url(reference, user=None):
        url_array = []
        for article in Reference.pmid_article(reference, user=user):
            url_array.append(article.pmid_article.url)
        return url_array
    
    # Returns MeSH URL.
    def mesh_url(source, mesh_uid):
        base_url = "https://meshb.nlm.nih.gov/record/ui?ui="
        return base_url + mesh_uid
    
    # Returns PubMed URL.
    def pubmed_url(reference, user=None):
        url_array = []
        for article in Reference.pmid_article(reference, user=user):
            url_array.append(article.pmid_article.pubmed_url)
        return url_array
    
    """
        Auxiliary functions
        
        Extract URLs from text
        Parse full citation for potential identifiers
        Search
    """
    
    # Extract URLs.
    def extract_urls(text, user=None):
        return extract_urls(text)
    
    # Parse citation.
    def parse_citation(citation, score_threshold=None, normalized_score_threshold=100, user=None):
        return parse_citation(citation, score_threshold=score_threshold, normalized_score_threshold=normalized_score_threshold)
        
    # Perform basic reference search.
    def search(source = "PubMed", level = "basic", db = "PubMed", query = None, unlabeled_string = None, affiliation = None, article_identifier = None, all_fields = None, author = None, author_identifier = None, book = None, corporate_author = None, create_date = None, completion_date = None, conflict_of_interest = None, ec_rn_number = None, editor = None, entrez_date = None, filter_citations = None, first_author_name = None, full_author_name = None, full_investigator_name = None, grant_number = None, investigator = None, isbn = None, issue = None, journal = None, language = None, last_author = None, location_id = None, mesh_date = None, mesh_major_topic = None, mesh_subheadings = None, mesh_terms = None, modification_date = None, nlm_unique_id = None, other_term = None, owner = None, pagination = None, personal_name_as_subject = None, pharmacological_action = None, place_of_publication = None, pmid = None, publisher = None, publication_date = None, publication_type = None, retmax = None, retmode = None, secondary_source_id = None, sort = None, subset = None, supplementary_concept = None, text_words = None, title = None, title_abstract = None, transliterated_title = None, uid = None, volume = None, raw = False, exact = False, user = None):
        
        if source.lower() in ["pubmed"] and level.lower() == "complex":
            
            return eutils_search(db = db, retmode = retmode, retmax = retmax, sort = sort, unlabeled_string = unlabeled_string, affiliation = affiliation, article_identifier = article_identifier, all_fields = all_fields, author = author, author_identifier = author_identifier, book = book, corporate_author = corporate_author, create_date = create_date, completion_date = completion_date, conflict_of_interest = conflict_of_interest, ec_rn_number = ec_rn_number, editor = editor, entrez_date = entrez_date, filter_citations = filter_citations, first_author_name = first_author_name, full_author_name = full_author_name, full_investigator_name = full_investigator_name, grant_number = grant_number, investigator = investigator, isbn = isbn, issue = issue, journal = journal, language = language, last_author = last_author, location_id = location_id, mesh_date = mesh_date, mesh_major_topic = mesh_major_topic, mesh_subheadings = mesh_subheadings, mesh_terms = mesh_terms, modification_date = modification_date, nlm_unique_id = nlm_unique_id, other_term = other_term, owner = owner, pagination = pagination, personal_name_as_subject = personal_name_as_subject, pharmacological_action = pharmacological_action, place_of_publication = place_of_publication, pmid = pmid, publisher = publisher, publication_date = publication_date, publication_type = publication_type, secondary_source_id = secondary_source_id, subset = subset, supplementary_concept = supplementary_concept, text_words = text_words, title = title, title_abstract = title_abstract, transliterated_title = transliterated_title, uid = uid, volume = volume, raw = raw, exact = exact)
        
        elif source.lower() in ["pubmed"] and level.lower() == "basic":
            
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
                
                # This is where the basic reference
                # search redirects for now, but it
                # is relatively slow.
                fetch = PubMedFetcher()
                pubmed_id_list = fetch.pmids_for_query(query)
                ref_list = []
                for pubmed_id in pubmed_id_list:
                    try:
                        article = fetch.article_by_pmid(pubmed_id) # Need a faster way to get titles...
                        temp_ref = Reference(identifier = str(pubmed_id), identifier_type = "PubMed ID", source = "PubMed", name = article.title)
                        ref_list.append(temp_ref)
                    except metapub.exceptions.InvalidPMID:
                        print("An invalid PMID error occurred.")
                        temp_ref = Reference(identifier = str(pubmed_id), identifier_type = "PubMed ID", source = "PubMed")
                        ref_list.append(temp_ref)
                    else:
                        temp_ref = Reference(identifier = str(pubmed_id), identifier_type = "PubMed ID", source = "PubMed")
                        ref_list.append(temp_ref)
                return ref_list
        
        elif source.lower() in ["google", "google scholar"]:
            return google_scholar_search(unlabeled_string)
        
        elif source.lower() in ["openlibrary"]:
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
    @property
    def get_mesh_from_pmid(self, user):
        Entrez.email = user.email
        handle = efetch(db = "pubmed", id = str(self.pmid), retmode = "xml")
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
    
    def pdf(ref, target_directory="../../data"):
        for x in get_pdf_url(ref):
            download_pdf(ref)
    
    def pdf_url(ref):
        return get_pdf_url(ref)
    
#   UNIT TESTS
def reference_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()