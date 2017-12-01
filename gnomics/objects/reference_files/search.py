#
#
#
#
#

#
#   IMPORT SOURCES:
#       EUTILS
#           https://pypi.python.org/pypi/eutils/0.3.2
#       ISBNLIB
#           https://pypi.python.org/pypi/isbnlib/3.7.2
#


#
#   Search for references.
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
import gnomics.objects.reference

#   Other imports.
import eutils
import isbnlib
import json
import os
import re
import requests
import scholarly
import urllib
import urllib.parse

#   MAIN
def main():
    search_unit_tests()

#   Get search.
    # Get PubMed IDs from query string with
    # auto-tagging where indicated.
    #
    # Field descriptors and tags are located here:
    # https://www.ncbi.nlm.nih.gov/books/NBK3827/#pubmedhelp.Search_Field_Descriptions_and
    #
    # "unlabeled_string" here refers to any string not
    # attached to any of these tags.
    #
    # The following tags are covered here:
    #   ad      = Affiliation
    #   aid     = Article Identifier
    #   all     = All Fields
    #   au      = Author
    #   auid    = Author Identifier
    #   book    = Book
    #   cn      = Corporate Author
    #   crdt    = Create Date
    #   dcom    = Completion Date
    #   cois    = Conflict of Interest
    #   rn      = EC/RN Number
    #   ed      = Editor
    #   edat    = Entrez Date
    #   filter  = Filter
    #   iau     = First Author Name
    #   fau     = Full Author Name
    #   fir     = Full Investigator Name
    #   gr      = Grant Number
    #   ir      = Investigator
    #   isbn    = ISBN
    #   ip      = Issue
    #   ta      = Journal
    #   la      = Language
    #   lastau  = Last Author
    #   lid     = Location ID
    #   mhda    = MeSH Date
    #   majr    = MeSH Major Topic
    #   sh      = MeSH Subheadings
    #   mh      = MeSH Terms
    #   lr      = Modification Date
    #   jid     = NLM Unique ID
    #   ot      = Other Term
    #   pg      = Pagination
    #   ps      = Personal Name as Subject
    #   pa      = Pharmacological Action
    #   pl      = Place of Publication
    #   pmid    = PMID / UID
    #   pubn    = Publisher
    #   dp      = Publication Date
    #   pt      = Publication Type
    #   si      = Secondary Source ID
    #   sb      = Subset
    #   nm      = Supplementary Concept
    #   tw      = Text Words
    #   ti      = Title
    #   tiab    = Title/Abstract
    #   tt      = Transliterated Title
    #   vi      = Volume
def eutils_search(db = "PubMed", exact = False, raw = False, retmode = None, retmax = None, sort = None, unlabeled_string = None, affiliation = None, article_identifier = None, all_fields = None, author = None, author_identifier = None, book = None, corporate_author = None, create_date = None, completion_date = None, conflict_of_interest = None, ec_rn_number = None, editor = None, entrez_date = None, filter_citations = None, first_author_name = None, full_author_name = None, full_investigator_name = None, grant_number = None, investigator = None, isbn = None, issue = None, journal = None, language = None, last_author = None, location_id = None, mesh_date = None, mesh_major_topic = None, mesh_subheadings = None, mesh_terms = None, modification_date = None, nlm_unique_id = None, other_term = None, owner = None, pagination = None, personal_name_as_subject = None, pharmacological_action = None, place_of_publication = None, pmid = None, publisher = None, publication_date = None, publication_type = None, secondary_source_id = None, subset = None, supplementary_concept = None, text_words = None, title = None, title_abstract = None, transliterated_title = None, uid = None, volume = None):
    ref_set = []
    result_set = []
    if not exact:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
        if db is not None:
            base_url = base_url + "db=" + str(db) + "&"
        if retmode is not None:
            base_url = base_url + "retmode=" + str(retmode) + "&"
        if retmax is not None:
            base_url = base_url + "retmax=" + str(retmax) + "&"
        else:
            base_url = base_url + "retmax=" + str(100000) + "&"
        if sort is not None:
            base_url = base_url + "sort=" + str(sort) + "&"
        term_url = "term="
        if unlabeled_string is not None:
            term_url = eutils_param_process(unlabeled_string)
        if affiliation is not None:
            term_url = term_url + eutils_param_process(affiliation, "ad")
        if article_identifier is not None:
            term_url = term_url + eutils_param_process(article_identifier, "aid")
        if all_fields is not None:
            term_url = term_url + eutils_param_process(all_fields, "all", raw = raw)
        if author is not None:
            term_url = term_url + eutils_param_process(author, "au")
        if author_identifier is not None:
            term_url = term_url + eutils_param_process(author_identifier, "auid")
        if book is not None:
            term_url = term_url + eutils_param_process(book, "book")
        if corporate_author is not None:
            term_url = term_url + eutils_param_process(corporate_author, "cn")
        if create_date is not None:
            term_url = term_url + eutils_param_process(create_date, "crdt")
        if completion_date is not None:
            term_url = term_url + eutils_param_process(completion_date, "dcom")
        if conflict_of_interest is not None:
            term_url = term_url + eutils_param_process(conflict_of_interest, "cois")
        if ec_rn_number is not None:
            term_url = term_url + eutils_param_process(ec_rn_number, "rn")
        if editor is not None:
            term_url = term_url + eutils_param_process(editor, "ed")
        if entrez_date is not None:
            term_url = term_url + eutils_param_process(entrez_date, "edat")
        if filter_citations is not None:
            term_url = term_url + eutils_param_process(filter_citations, "filter")
        if first_author_name is not None:
            term_url = term_url + eutils_param_process(first_author_name, "iau")
        if full_author_name is not None:
            term_url = term_url + eutils_param_process(full_author_name, "fau")
        if full_investigator_name is not None:
            term_url = term_url + eutils_param_process(full_investigator_name, "fir")
        if grant_number is not None:
            term_url = term_url + eutils_param_process(grant_number, "gr")
        if investigator is not None:
            term_url = term_url + eutils_param_process(investigator, "ir")
        if isbn is not None:
            term_url = term_url + eutils_param_process(isbn, "isbn")
        if issue is not None:
            term_url = term_url + eutils_param_process(issue, "ip")
        if journal is not None:
            term_url = term_url + eutils_param_process(journal, "ta")
        if language is not None:
            term_url = term_url + eutils_param_process(language, "la")
        if last_author is not None:
            term_url = term_url + eutils_param_process(last_author, "lastau")
        if location_id is not None:
            term_url = term_url + eutils_param_process(location_id, "lid")
        if mesh_date is not None:
            term_url = term_url + eutils_param_process(mesh_date, "mhda")
        if mesh_major_topic is not None:
            term_url = term_url + eutils_param_process(mesh_major_topic, "majr")
        if mesh_subheadings is not None:
            term_url = term_url + eutils_param_process(mesh_subheadings, "sh")
        if mesh_terms is not None:
            term_url = term_url + eutils_param_process(mesh_terms, "mh")
        if modification_date is not None:
            term_url = term_url + eutils_param_process(modification_date, "lr")
        if nlm_unique_id is not None:
            term_url = term_url + eutils_param_process(nlm_unique_id, "jid")
        if other_term is not None:
            term_url = term_url + eutils_param_process(other_term, "ot")
        if owner is not None:
            print("NOT FUNCTIONAL.")
        if pagination is not None:
            term_url = term_url + eutils_param_process(pagination, "pg")
        if personal_name_as_subject is not None:
            term_url = term_url + eutils_param_process(personal_name_as_subject, "ps")
        if pharmacological_action is not None:
            term_url = term_url + eutils_param_process(pharmacological_action, "pa")
        if place_of_publication is not None:
            term_url = term_url + eutils_param_process(place_of_publication, "pl")
        if pmid is not None:
            term_url = term_url + eutils_param_process(pmid, "pmid")
        if publisher is not None:
            term_url = term_url + eutils_param_process(publisher, "pubn")
        if publication_date is not None:
            term_url = term_url + eutils_param_process(publication_date, "dp")
        if publication_type is not None:
            term_url = term_url + eutils_param_process(publication_type, "pt")
        if secondary_source_id is not None:
            term_url = term_url + eutils_param_process(secondary_source_id, "si")
        if subset is not None:
            term_url = term_url + eutils_param_process(subset, "sb")
        if supplementary_concept is not None:
            term_url = term_url + eutils_param_process(supplementary_concept, "nm")
        if text_words is not None:
            term_url = term_url + eutils_param_process(text_words, "tw")
        if title is not None:
            term_url = term_url + eutils_param_process(title, "ti")
        if title_abstract is not None:
            term_url = term_url + eutils_param_process(title_abstract, "tiab")
        if transliterated_title is not None:
            term_url = term_url + eutils_param_process(transliterated_title, "tt")
        if uid is not None:
            term_url = term_url + eutils_param_process(uid, "pmid")
        if volume is not None:
            term_url = term_url + eutils_param_process(volume, "vi")
        if term_url[-1] == "+":
            term_url = term_url[:-1]
        if term_url[-1] == "&":
            term_url = term_url[:-1]
        r = requests.get(base_url + term_url, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        result_set.append(decoded)
        if retmax is None:
            count_set = int(decoded['esearchresult']['count']) - 100000
            while count_set > 0:
                retstart = int(decoded['esearchresult']['retstart']) + 1
                r = requests.get(base_url + term_url + "&" + "retstart=" + str(retstart), headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = r.json()
                result_set.append(decoded)
                count_set = count_set - 100000
        ec = eutils.Client()
        ref_set = []
        id_set = []
        for dec_set in result_set:
            for pmid in dec_set["esearchresult"]["idlist"]:
                id_set.append(pmid)
        pmset = ec.efetch(db="pubmed", id=id_set)
        for pm in pmset:
            title = pm.title
            authors = pm.authors
            journal = pm.jrnl
            volume = pm.volume
            issue = pm.issue
            year = pm.year
            pages = pm.pages
            pmid = pm.pmid
            doi = pm.doi
            pmc = pm.pmc
            temp_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PubMed ID", source = "Entrez Programming Utilities", language = None, name = title)
            if doi is not None: 
                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = doi, identifier_type = "DOI", source = "Entrez Programming Utilities", language = None, name = title)
            if pmc is not None:
                gnomics.objects.reference.Reference.add_identifier(temp_ref, identifier = pmc, identifier_type = "PMC ID", source = "Entrez Programming Utilities", language = None, name = title)
            ref_set.append(temp_ref)
    else:
        base_url = "https://www.ncbi.nlm.nih.gov/pubmed/?"
        ext_url = ""
        if unlabeled_string: 
            ext_url = ext_url + unlabeled_string
        elif all_fields:
            ext_url = ext_url + all_fields
        ext_url = "term=" + str(urllib.parse.quote_plus('("' + ext_url.replace('"', "'")))
        r = requests.get(base_url + ext_url, headers={"Content-Type": "application/json"})
        if "PMID:" in r.text:
            pmid_html = re.findall('<dt>PMID:</dt>.{1,}?[\d].{1,}?</dd>', r.text)
            pmid = re.findall('\d+', pmid_html[0])
            temp_ref = gnomics.objects.reference.Reference(identifier = pmid[0], identifier_type = "PubMed ID", source = "PubMed", language = None)
            ref_set.append(temp_ref)
    return ref_set

def eutils_param_process(term, iden = None, raw = False):
    if not isinstance(term, list) and not raw:
        if ' and ' in term.lower() or '+and+' in term.lower():
            and_array = (term.lower()).split(' and ')
            term = str("+AND+".join(and_array))
        if ' or ' in term.lower() or '+or+' in term.lower():
            or_array = (term.lower()).split(' or ')
            term = str("+OR+".join(or_array))
        if 'not ' in term.lower() or 'not+' in term.lower():
            not_array = (term.lower()).split('not ')
            term = str("NOT+".join(not_array))
        paren_array = []
        for x in term.split('+'):
            if '"' not in x and x.lower() != "and" and x.lower() != "or" and x.lower() != "not" and x.lower() != "(not":
                if '(' in x:
                    paren_1 = x.split('(')
                    y = paren_1.pop()
                    z = '"' + y
                    paren_1.append(z)
                    if ')' in paren_1:
                        x = '('.join(paren_1)
                        paren_2 = x.split(')')
                        paren_2[0] = paren_2[0] + '"'
                        if iden:
                            paren_2[0] = paren_2[0] + '[' + iden + ']'
                        x = ')'.join(paren_2)
                    else:
                        y = paren_1.pop()
                        z = y + '"'
                        if iden:
                            z = z + '[' + iden + ']'
                        paren_1.append(z)
                        x = '('.join(paren_1)
                    paren_array.append(x)
                elif ')' in x:
                    paren_1 = x.split(')')
                    paren_1[0] = paren_1[0] + '"'
                    if '(' not in paren_1:
                        y = paren_1[0]
                        z = '"' + y 
                        if iden:
                            z = z + '[' + iden + ']'
                        paren_1[0] = z
                    x = ')'.join(paren_1)
                    paren_array.append(x)
                else:
                    paren_array.append('"' + x + '"')
            else:
                paren_array.append(x)
        term = '+'.join(paren_array)
        return str(term + "+")
    elif not raw:
        # Add double quotes to all terms.
        quoted_tm = []
        for tm in term:
            if '"' not in tm:
                if iden:
                    quoted_tm.append('"' + tm.strip() + '"' + '[' + iden + ']')
                else:
                    quoted_tm.append('"' + tm.strip() + '"')
            else:
                if iden:
                    quoted_tm.append(tm.strip() + '[' + iden + ']')
                else:
                    quoted_tm.append(tm.strip())
        return str("+".join(quoted_tm) + "+")
    else:
        # Note that this function still encodes the string
        # as a URL, then replaces spaces with "+".
        # 
        # All replace double quotes (") with single quotes
        # in order to wrap the full string.
        #
        # Next, the all fields tag is added, and the
        # whole thing is wrapped in a parenthetical.
        return urllib.parse.quote_plus('("' + term.replace('"', "'") + '"[All Fields])')

#   Search Google Scholar.
#
#   Scholarly does not currently function, due to
#   restrictions of bots crawling the Google Scholar catalogue.
def google_scholar_search(query):
    print("NOT FUNCTIONAL.")
    
#   ISBN search.
def isbn_search(query):
    return isbn_from_words(query)
    
#   Search OpenLibrary.
def openlibrary_search(query):
    print("NOT FUNCTIONAL.")
    
#   Search Elsevier.
#
#   Various search sources are available:
#   - Scopus
#   - ScienceDirect
def elsevier_search(query, user = None, source = "scopus"):
    print("NOT FUNCTIONAL.")
    # https://dev.elsevier.com/search.html
    
#   Search Springer.
def springer_search(query, user = None):
    print("NOT FUNCTIONAL.")

#   Search Google Books.
def google_books_search(query, user = None):
    base = "https://www.googleapis.com/books/"
    ext = "v1/volumes?q=" + query + "&key=" + user.google_books_api_key
    
#   UNIT TESTS
def search_unit_tests():
    basic_search_results = eutils_search(db = "PubMed", unlabeled_string = "cystic fibrosis and (neuron or (not nerve))", retmode = "JSON")
    print("\nSearch returned %s result(s) with the following reference IDs:" % str(len(basic_search_results)))
    for ref in basic_search_results:
        for iden in ref.identifiers:
            print("- %s: %s (%s)" % ((iden["identifier"]), str(iden["name"]).encode('utf8'), (iden["identifier_type"])))

#   MAIN
if __name__ == "__main__": main()