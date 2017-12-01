#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Search for anatomical structures.
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
import gnomics.objects.anatomical_structure

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("Radius", "")

# Return search.
def search(query, user = None, source = "ebi", search_type = "exact", return_id_type = "sourceUi"):
    anat_list = []
    anat_id_array = []
    if source == "ebi" or source == "all":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=aeo,caro,fma,uberon,ceph,ehdaa2,emap,emapa,fbbt,hao,ma,mfmo,plana,tads,tgma,wbbt,xao,zfa,fao"
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        # See here:
        # https://www.ebi.ac.uk/ols/ontologies
        for doc in decoded["response"]["docs"]:
            if "obo_id" in doc:
                # Taxon agnostic.
                if "AEO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "AEO ID", source = "Ontology Lookup Service", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "CARO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "CARO ID", source = "Ontology Lookup Service", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "FAO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "FAO ID", source = "Ontology Lookup Service", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "FMA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "FMA ID", source = "Ontology Lookup Service", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "UBERON" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                
                # Taxon specific.
                elif "CEPH" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "CEPH ID", source = "Ontology Lookup Service", taxon="Cephalopoda", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "EHDAA2" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "EHDAA2 ID", source = "Ontology Lookup Service", taxon="Homo sapiens", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "EMAP" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "EMAP ID", source = "Ontology Lookup Service", taxon="Mus", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "EMAPA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "EMAPA ID", source = "Ontology Lookup Service", taxon="Mus", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "FBbt" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "FBbt ID", source = "Ontology Lookup Service", taxon="Drosophila melanogaster", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "HAO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "HAO ID", source = "Ontology Lookup Service", taxon="Hymenoptera", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "MA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "MA ID", source = "Ontology Lookup Service", taxon="Mus", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "MFMO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "MFMO ID", source = "Ontology Lookup Service", taxon="Mammalia", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "PLANA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "PLANA ID", source = "Ontology Lookup Service", taxon="Schmidtea mediterranea", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "TADS" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "FBbt ID", source = "Ontology Lookup Service", taxon=["Ixodidae", "Argassidae"], name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "TGMA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "TGMA ID", source = "Ontology Lookup Service", taxon="Culicidae", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "WBBT" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "WBBT ID", source = "Ontology Lookup Service", taxon="Caenorhabditis elegans", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "XAO" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "XAO ID", source = "Ontology Lookup Service", taxon="Xenopus laevis", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
                elif "ZFA" in doc["obo_id"]:
                    new_id = doc["obo_id"]
                    if new_id not in anat_id_array:
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "ZFA ID", source = "Ontology Lookup Service", taxon="Danio rerio", name = doc["label"])
                        anat_list.append(anat_temp)
                        anat_id_array.append(new_id)
    if (source == "umls" or source == "all") and user is not None:
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
            # print(r.text)
            items = json.loads(r.text)
            json_data = items["result"]
            for rep in json_data["results"]:
                if rep["ui"] not in anat_id_array and rep["ui"] != "NONE":
                    # Foundational Model of Anatomy.
                    if rep["rootSource"] == "FMA":
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="FMA ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])
                    # Neuronames Brain Hierarchy.
                    elif rep["rootSource"] == "NEU":
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="NEU ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])
                    # Digital Anatomist.
                    elif rep["rootSource"] == "UWDA":
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="UWDA ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])
            if json_data["results"][0]["ui"] == "NONE":
                break
    return anat_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query, umls_api_key):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following identifiers (EBI):" % str(len(basic_search_results)))
    for anat in basic_search_results:
        for iden in anat.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    user = User(umls_api_key = umls_api_key)
    basic_search_results = search(basic_query, source="umls", user = user)
    print("\nSearch returned %s result(s) with the following identifiers (UMLS):" % str(len(basic_search_results)))
    for anat in basic_search_results:
        for iden in anat.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()