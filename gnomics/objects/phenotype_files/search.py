#
#
#
#
#

#
#   IMPORT SOURCES:
#


#
#   Search for phenotype.
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
import gnomics.objects.phenotype

#   Other imports.
import json
import requests

#   MAIN
def main():
    basic_search_unit_tests("curly hair")
    
# Return search.
def search(query, source = "ebi"):
    if source == "ebi":
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=hp,fbcv,flopo,fypo,mp,omp,wbphenotype,atol,oba,to"
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            print("Something went wrong.")
        else:
            decoded = r.json()
            phen_list = []
            phen_id_array = []
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:
                    if "ATOL" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "ATOL ID", source = "Ontology Lookup Service", taxon = "Homo sapiens", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "HP" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "Human Phenotype Ontology ID", source = "Ontology Lookup Service", taxon = "Homo sapiens", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "FBcv" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "FBcv ID", source = "Ontology Lookup Service", taxon = "Drosophila", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "FLOPO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "FLOPO ID", source = "Ontology Lookup Service", taxon = "Angiosperms", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "FYPO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "FYPO ID", source = "Ontology Lookup Service", taxon = "Schizosaccharomyces pombe", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "MP" in doc["obo_id"] and doc["ontology_prefix"] == "MP":
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "MP ID", source = "Ontology Lookup Service", taxon = "Mammalia", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "OBA" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "OBA ID", source = "Ontology Lookup Service", taxon=None, name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    # Note, this ontology includes all microbes, of
                    # which these exist in all domains of life.
                    # Because bacteria and achaea are mostly, if not
                    # completely microbial in nature, they are
                    # currently included in the taxon field here,
                    # although this may change in the future.
                    elif "OMP" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "OMP ID", source = "Ontology Lookup Service", taxon=["Archaea", "Bacteria"], name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "TO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "TO ID", source = "Ontology Lookup Service", taxon="Plantae", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "UPHENO" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "UPHENO ID", source = "Ontology Lookup Service", taxon = None, name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "VT" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "VT ID", source = "Ontology Lookup Service", taxon = "Vertebrata", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
                    elif "WBPHENOTYPE" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in phen_id_array:
                            phen_temp = gnomics.objects.phenotype.Phenotype(identifier = new_id, identifier_type = "WBPHENOTYPE ID", source = "Ontology Lookup Service", taxon = "Caenorhabditis elegans", name = doc["label"])
                            phen_list.append(phen_temp)
                            phen_id_array.append(new_id)
        return phen_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query):
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query)
    print("\nSearch returned %s result(s) with the following phenotype IDs:" % str(len(basic_search_results)))
    for phen in basic_search_results:
        for iden in phen.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()