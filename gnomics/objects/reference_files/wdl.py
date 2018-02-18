#!/usr/bin/env python

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
#   Get references from the World Digital Library (WDL).
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
from bs4 import BeautifulSoup
import json
import requests

#   MAIN
def main():
    wdl_unit_tests("breast cancer", "bre")
    
#   Standard OpenSearch.
#
#   See: 
#   http://www.opensearch.org/Specifications/OpenSearch/1.1#OpenSearch_description_document
def wdl_opensearch(query, language="en", start_page=None, start_index=None, format_type=None):
    if language.lower() in ["en", "eng", "english"]:
        
        base = "https://www.wdl.org/en/search/"
        ext = "?qla=en&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
        
    elif language.lower() in ["ar", "arabic"]:
        base = "https://www.wdl.org/ar/search/"
        ext = "?qla=ar&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    elif language.lower() in ["es", "spanish"]:
        base = "https://www.wdl.org/es/search/"
        ext = "?qla=es&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    elif language.lower() in ["fr", "french"]:
        base = "https://www.wdl.org/fr/search/"
        ext = "?qla=fr&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    elif language.lower() in ["pt", "portuguese"]:
        base = "https://www.wdl.org/pt/search/"
        ext = "?qla=pt&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    elif language.lower() in ["ru", "russian"]:
        base = "https://www.wdl.org/ru/search/"
        ext = "?qla=ru&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    elif language.lower() in ["zh", "chinese"]:
        base = "https://www.wdl.org/zh/search/"
        ext = "?qla=zh&amp;q=" + str(query)

        r = requests.get(base+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            soup.prettify()
            
            results = {}
            for result in soup.find_all("div", {"class": "result"}):
                data_wdl_id = result["id"]
                thumbnail_url = result.find("img", {"class": "center-block thumbnail"})["src"]
                title = result.find("strong", {"itemprop": "name"}).text
                description = result.find("div", {"itemprop": "description"}).text
                institution = result.find("div", {"class": "institution"}).find("a").text
                hits = []
                for hit in result.find_all("div", {"class": "doc file"}):
                    hit_location = hit.find("a").text
                    hit_areas = hit.find("ul", {"class": "snippet list-unstyled"})
                    for sub_hit in hit_areas.findAll("li"):
                        hit_text = sub_hit.text
                        hits.append({
                            'location': hit_location,
                            'text': hit_text
                        })
                        
                results[data_wdl_id] = {
                    'thumbnail': thumbnail_url,
                    'title': title,
                    'description': description,
                    'institution': institution,
                    'hits': hits
                }
                
                return results
            
    else:
        print("The language provided (%s) is either not valid or not available." % str(language))

#   OpenSearch suggestions.
#
#   See:
#   http://www.opensearch.org/Specifications/OpenSearch/Extensions/Suggestions/1.1
def wdl_opensearch_suggestions(query, language="en", suggestion_prefix=None, suggestion_index=None):
    
    suggestion_list = []
    
    if suggestion_prefix is None:
        suggestion_prefix = ""
    if suggestion_index is None:
        suggestion_index = ""
    
    if language.lower() in ["en", "eng", "english"]:
        
        base = "https://www.wdl.org/en/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["ar", "arabic"]:
        
        base = "https://www.wdl.org/ar/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["es", "spanish"]:
        
        base = "https://www.wdl.org/es/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["fr", "french"]:
        
        base = "https://www.wdl.org/fr/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["pt", "portuguese"]:
        
        base = "https://www.wdl.org/pt/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["ru", "russian"]:
        
        base = "https://www.wdl.org/ru/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    elif language.lower() in ["zh", "chinese"]:
        
        base = "https://www.wdl.org/zh/search/"
        ext = "opensearch-suggestions/?q=" + str(query) + "&prefix=" + str(suggestion_prefix) + "&index=" +  str(suggestion_index)

        r = requests.get(base+ext, headers={"Content-Type": "application/x-suggestions+json"})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            
            for x in r.json():
                if type(x) is list:
                    for y in x:
                        suggestion_list.append(y)
        
    else:
        print("The language provided (%s) is either not valid or not available." % str(language))
        
    return suggestion_list
        
#   UNIT TESTS
def wdl_unit_tests(query, suggest):
    print("Returning suggestions for '%s'..." % suggest)
    for sug in wdl_opensearch_suggestions(suggest):
        print("- %s" % str(sug))

#   MAIN
if __name__ == "__main__": main()