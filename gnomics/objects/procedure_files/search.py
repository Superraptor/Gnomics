#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYMEDTERMINO
#           http://pythonhosted.org/PyMedTermino/
#

#
#   Search for drugs.
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
import gnomics.objects.procedure

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("colonoscopy", "")
    
# Return search.
def search(query, user=None, search_type="exact", return_id_type="sourceUi"):
    if search_type == "exact" and user is not None:
        proc_array = []
        proc_obj_array = []

        umls_tgt = User.umls_tgt(user)
        page_num = 0
        base = "https://uts-ws.nlm.nih.gov/rest"
        ext = "/search/current?string=" + query + "&inputType=sourceUi&searchType=words&returnIdType=" + return_id_type

        while True:
            tick = User.umls_st(umls_tgt)
            page_num += 1
            query = {"string": query, "ticket": tick, "pageNumber": page_num}
            r = requests.get(base+ext, params=query)
            r.encoding = 'utf-8'
            #print(r.text)
            items = json.loads(r.text)
            json_data = items["result"]
            for rep in json_data["results"]:
                if rep["ui"] not in proc_array and rep["ui"] != "NONE":
                    
                    # Current Procedural Terminology.
                    if rep["rootSource"] == "CPT":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="CPT ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        proc_obj_array.append(temp_proc)
                    
                    # Current Procedural Terminology (Spanish).
                    elif rep["rootSource"] == "CPTSP":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="CPTSP ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        proc_obj_array.append(temp_proc)
                        
                    # Healthcare Common Procedure Coding System (HCPCS).
                    elif rep["rootSource"] == "HCPCS":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="HCPCS ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        proc_obj_array.append(temp_proc)
                        
                    # CPT in Healthcare Common Procedure Coding System (CPT in HCPCS).
                    elif rep["rootSource"] == "HCPT":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="HCPT ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        proc_obj_array.append(temp_proc)
                        
                    # ICD-10-PCS.
                    elif rep["rootSource"] == "ICD-10-PCS":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="ICD-10-PCS Code", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (English).
                    elif rep["rootSource"] == "LNC":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "en")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Austrian German).
                    elif rep["rootSource"] == "LNC-DE-AT":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "de-AT")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Swiss German).
                    elif rep["rootSource"] == "LNC-DE-CH":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "gsw")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (German).
                    elif rep["rootSource"] == "LNC-DE-DE":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "de")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Greek).
                    elif rep["rootSource"] == "LNC-EL-GR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "el")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Argentinian Spanish).
                    elif rep["rootSource"] == "LNC-ES-AR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "es-AR")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Swiss Spanish).
                    elif rep["rootSource"] == "LNC-ES-CH":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "es-CH")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Spanish).
                    elif rep["rootSource"] == "LNC-ES-ES":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "es")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Estonian).
                    elif rep["rootSource"] == "LNC-ET-EE":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "et")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Belgian French).
                    elif rep["rootSource"] == "LNC-FR-BE":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "fr-BE")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Canadian French).
                    elif rep["rootSource"] == "LNC-FR-CA":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "fr-CA")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Swiss French).
                    elif rep["rootSource"] == "LNC-FR-CH":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "fr-CH")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (French).
                    elif rep["rootSource"] == "LNC-FR-FR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "fr")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Swiss Italian).
                    elif rep["rootSource"] == "LNC-IT-CH":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "it-CH")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Italian).
                    elif rep["rootSource"] == "LNC-IT-IT":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "it")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Korean).
                    elif rep["rootSource"] == "LNC-KO-KR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "ko")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Dutch).
                    elif rep["rootSource"] == "LNC-NL-NL":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "nl")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Brazilian Portuguese).
                    elif rep["rootSource"] == "LNC-PT-BR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "pt-BR")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Russian).
                    elif rep["rootSource"] == "LNC-RU-RU":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "ru")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Turkish).
                    elif rep["rootSource"] == "LNC-TR-TR":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "tr")
                        proc_obj_array.append(temp_proc)
                        
                    # LOINC (Chinese).
                    elif rep["rootSource"] == "LNC-ZH-CN":
                        temp_proc = gnomics.objects.procedure.Procedure(identifier=rep["ui"], identifier_type="LOINC Code", source="UMLS Metathesaurus", name=rep["name"], language = "zh")
                        proc_obj_array.append(temp_proc)

            if json_data["results"][0]["ui"] == "NONE":
                break

        return proc_obj_array
        
    elif search_type == "approximate" and user is not None:
        proc_array = []
        umls_tgt = User.umls_tgt(user)
        page_num = 0
        base = "https://uts-ws.nlm.nih.gov/rest"
        ext = "/search/current?string=" + query + "&searchType=approximate&returnIdType=" + return_id_type

        while True:
            tick = User.umls_st(umls_tgt)
            page_num += 1
            query = {"string": query, "ticket": tick, "pageNumber": page_num}
            r = requests.get(base+ext, params=query)
            r.encoding = 'utf-8'
            print(r.text)
            items = json.loads(r.text)
            json_data = items["result"]
            for rep in json_data["results"]:
                if rep["ui"] not in proc_array and rep["ui"] != "NONE":
                    proc_array.append(rep["ui"])

            if json_data["results"][0]["ui"] == "NONE":
                break

        return proc_array
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query, umls_api_key):
    user = User(umls_api_key = umls_api_key)
    
    print("Beginning basic searches for '%s'..." % basic_query)
    start = timeit.timeit()
    basic_search_results = search(basic_query, user, search_type="exact")
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nSearch returned %s exact result(s) with the following procedure identifiers:" % str(len(basic_search_results)))
    for proc in basic_search_results:
        for iden in proc.identifiers:
            print("- %s (%s)" % (iden["identifier"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()