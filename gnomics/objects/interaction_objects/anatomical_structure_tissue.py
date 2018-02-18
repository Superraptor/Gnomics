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
#   Get tissues from anatomical structures.
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
import gnomics.objects.tissue

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    anatomical_structure_tissue_unit_tests("UBERON:0002185", "UBERON_0000117", "UBERON_0000065")
     
#   Get tissues.
def get_tissues(anatomical_structure, children=False, descendants=False, hierarchical_descendants=False, user=None):
    tiss_array = []
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anatomical_structure.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            proc_id = iden["identifier"]
            if ":" in proc_id:
                proc_id = proc_id.replace(":", "_")
    
            if children == False and descendants == False and hierarchical_descendants == False:
                base = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/uberon/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + str(proc_id)
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                
                temp_tiss = gnomics.objects.tissue.Tissue()
                for xref in decoded["annotation"]["database_cross_reference"]:
                    if "BTO" in xref:
                        gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = xref, identifier_type = "BTO ID", source = "Ontology Lookup Service")
                    elif "CALOHA" in xref:
                        gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = xref.split(":")[1], identifier_type = "CALOHA ID", source = "Ontology Lookup Service")
                
                if temp_tiss.identifiers:
                    tiss_array.append(temp_tiss)
                    
            elif children == True and descendants == False and hierarchical_descendants == False:
                base = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/uberon/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + str(proc_id) + "/children"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                
                for term in decoded["_embedded"]["terms"]:
                    temp_tiss = gnomics.objects.tissue.Tissue()
                    
                    for xref in term["annotation"]:
                        if "database_cross_reference" in xref:
                            for cross_ref in term["annotation"]["database_cross_reference"]:
                                if "BTO" in cross_ref:
                                    gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref, identifier_type = "BTO ID", source = "Ontology Lookup Service")
                                elif "CALOHA" in cross_ref:
                                    gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref.split(":")[1], identifier_type = "CALOHA ID", source = "Ontology Lookup Service")

                    if temp_tiss.identifiers:
                        tiss_array.append(temp_tiss)
            elif children == False and descendants == True and hierarchical_descendants == False:
                
                base = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/uberon/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + str(proc_id) + "/descendants"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    r.raise_for_status()
                    sys.exit()
                decoded = json.loads(r.text)
                
                if "_embedded" in decoded:
                    for term in decoded["_embedded"]["terms"]:
                        temp_tiss = gnomics.objects.tissue.Tissue()

                        for xref in term["annotation"]:
                            if "database_cross_reference" in xref:
                                for cross_ref in term["annotation"]["database_cross_reference"]:

                                    if "BTO" in cross_ref:
                                        gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref, identifier_type = "BTO ID", source = "Ontology Lookup Service")
                                    elif "CALOHA" in cross_ref:
                                        gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref.split(":")[1], identifier_type = "CALOHA ID", source = "Ontology Lookup Service")

                        if temp_tiss.identifiers:
                            tiss_array.append(temp_tiss)
                            
            elif children == False and descendants == False and hierarchical_descendants == True:
                
                base = "https://www.ebi.ac.uk/ols/api/ontologies"
                ext = "/uberon/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F" + str(proc_id) + "/hierarchicalDescendants"
                r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                if not r.ok:
                    continue
                else:
                    decoded = json.loads(r.text)

                    if "_embedded" in decoded:
                        for term in decoded["_embedded"]["terms"]:
                            temp_tiss = gnomics.objects.tissue.Tissue()

                            for xref in term["annotation"]:
                                if "database_cross_reference" in xref:
                                    for cross_ref in term["annotation"]["database_cross_reference"]:
                                        if "BTO" in cross_ref:
                                            gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref, identifier_type = "BTO ID", source = "Ontology Lookup Service")
                                        elif "CALOHA" in cross_ref:
                                            gnomics.objects.tissue.Tissue.add_identifier(temp_tiss, identifier = cross_ref.split(":")[1], identifier_type = "CALOHA ID", source = "Ontology Lookup Service")

                            if temp_tiss.identifiers:
                                tiss_array.append(temp_tiss)
                   
    return tiss_array
    
#   UNIT TESTS
def anatomical_structure_tissue_unit_tests(uberon_id, uberon_id_2, uberon_id_3):
    
    uberon_anat = gnomics.objects.phenotype.Phenotype(identifier = uberon_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    print("\nGetting tissue identifiers from anatomical structures (%s):" % uberon_id)
    start = timeit.timeit()
    tissues = get_tissues(uberon_anat)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for tiss in tissues:
        for iden in tiss.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
            
    uberon_anat = gnomics.objects.phenotype.Phenotype(identifier = uberon_id_2, identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    print("\nGetting child tissue identifiers from anatomical structures (%s):" % uberon_id_2)
    start = timeit.timeit()
    children = get_tissues(uberon_anat, children = True)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for tiss in children:
        for iden in tiss.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))
        
    uberon_anat = gnomics.objects.phenotype.Phenotype(identifier = uberon_id_3, identifier_type = "UBERON ID", source = "Ontology Lookup Service")
    print("\nGetting hierarchical descendant tissue identifiers from anatomical structures (%s):" % uberon_id_3)
    start = timeit.timeit()
    hierarchical_descendants = get_tissues(uberon_anat, hierarchical_descendants = True)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    for tiss in hierarchical_descendants:
        for iden in tiss.identifiers:
            print("- %s (%s)" % (str(iden["identifier"]), iden["identifier_type"]))

#   MAIN
if __name__ == "__main__": main()