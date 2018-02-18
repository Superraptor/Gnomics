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
import gnomics.objects.auxiliary_files.identifier

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    basic_search_unit_tests("Radius", "", "")

# Return search.
def search(query, user=None, source="ebi", search_type="exact", return_id_type="sourceUi"):
    anat_list = []
    anat_id_array = []
    
    if source.lower() in ["ebi", "all"]:
        
        url = "http://www.ebi.ac.uk/ols/api/"
        ext = "search?q=" + str(query) + "&ontology=aeo,caro,fma,uberon,ceph,ehdaa2,emap,emapa,fbbt,hao,ma,mfmo,plana,tads,tgma,wbbt,xao,zfa,fao"
            
        r = requests.get(url+ext, headers={"Content-Type": "application/json"})

        if not r.ok:
            print("An error occurred in the EBI OLS API.")
            
        else:
            decoded = r.json()

            # See here:
            # https://www.ebi.ac.uk/ols/ontologies
            for doc in decoded["response"]["docs"]:
                if "obo_id" in doc:

                    # Taxon agnostic (I think)
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
                    elif "UBERON" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in anat_id_array:
                            anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "UBERON ID", source = "Ontology Lookup Service", name = doc["label"])
                            anat_list.append(anat_temp)
                            anat_id_array.append(new_id)

                    # Taxon specific (I think)
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
                    elif "FMA" in doc["obo_id"]:
                        new_id = doc["obo_id"]
                        if new_id not in anat_id_array:
                            anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = new_id, identifier_type = "FMA ID", source = "Ontology Lookup Service", name = doc["label"], taxon="Homo sapiens")
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
    
    if source.lower() in ["umls", "all"] and user is not None:

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
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="FMA ID", language=None, source="UMLS Metathesaurus", name=rep["name"], taxon="Homo sapiens")
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])
                        
                    # Neuronames Brain Hierarchy.
                    elif rep["rootSource"] == "NEU":
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="NEU ID", language=None, source="UMLS Metathesaurus", name=rep["name"])
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])
                        
                    # Digital Anatomist.
                    elif rep["rootSource"] == "UWDA":
                        temp_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=rep["ui"], identifier_type="UWDA ID", language=None, source="UMLS Metathesaurus", name=rep["name"], taxon="Homo sapiens")
                        anat_list.append(temp_anat)
                        anat_id_array.append(rep["ui"])

            if json_data["results"][0]["ui"] == "NONE":
                break
                
    if source.lower() in ["ncbo", "all"] and user.ncbo_api_key is not None:
            
        base = "http://data.bioontology.org/search"
        ext = "?q=" + str(query) + "&ontologies=FMA,PAE,XAO,UBERON,ZEA,FB-BT,FAO,WB-BT,ZFA,HAO,TGMA,ICD11-BODYSYSTEM,DDANAT,SPD,TADS,VHOG,CARO,MA,MOOCCUADO,EMAPA,CTENO,MOOCCIADO,AAO,PHMAMMADO,CEPH,PHFUMIADO,HAROREADO,CISAVIADO,MAT,EHDA,MFMO,CIINTEADO,EHDAA,EMAP,BSAO,PLANA,MFO,EHDAA2,AEO,PORO,MOOCULADO,TAO,VSAO&roots_only=true/?apikey=" + user.ncbo_api_key

        r = requests.get(base+ext, headers={"Content-Type": "application/json", "Authorization": "apikey token="+ user.ncbo_api_key})

        if not r.ok:
            r.raise_for_status()
            sys.exit()
        else:
            decoded = json.loads(r.text)
            
            for result in decoded["collection"]:
                
                # Foundational Model of Anatomy
                if "FMA" in result["@id"]:
                    fma_id = result["@id"].split("/obo/")[1]
                    if fma_id not in anat_id_array:
                        anat_id_array.append(fma_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=fma_id, identifier_type="FMA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Homo sapiens")
                        anat_list.append(anat_temp)
                        
                # Vertebrate Skeletal Anatomy Ontology
                elif "VSAO" in result["@id"]:
                    vsao_id = result["@id"].split("/obo/")[1]
                    if vsao_id not in anat_id_array:
                        anat_id_array.append(vsao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=vsao_id, identifier_type="VSAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Vertebrata")
                        anat_list.append(anat_temp)
                        
                # Teleost Anatomy Ontology
                elif "TAO" in result["@id"]:
                    tao_id = result["@id"].split("/obo/")[1]
                    if tao_id not in anat_id_array:
                        anat_id_array.append(tao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=tao_id, identifier_type="TAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Teleostei")
                        anat_list.append(anat_temp)
                        
                # Molgula oculata Anatomy and Development Ontology
                elif "MOOCULADO" in result["@id"]:
                    mooculado_id = result["@id"].split("/obo/")[1]
                    if mooculado_id not in anat_id_array:
                        anat_id_array.append(mooculado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=mooculado_id, identifier_type="MOOCULADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Molgula oculata")
                        anat_list.append(anat_temp)
                        
                # Porifera Ontology
                elif "PORO" in result["@id"]:
                    poro_id = result["@id"].split("/obo/")[1]
                    if poro_id not in anat_id_array:
                        anat_id_array.append(poro_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=poro_id, identifier_type="PORO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Porifera")
                        anat_list.append(anat_temp)
                        
                # Anatomical Entity Ontology
                elif "AEO" in result["@id"]:
                    aeo_id = result["@id"].split("/obo/")[1]
                    if aeo_id not in anat_id_array:
                        anat_id_array.append(aeo_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=aeo_id, identifier_type="AEO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        anat_list.append(anat_temp)
                        
                # Human Developmental Anatomy Ontology, abstract version 2
                elif "EHDAA2" in result["@id"]:
                    ehdaa2_id = result["@id"].split("/obo/")[1]
                    if ehdaa2_id not in anat_id_array:
                        anat_id_array.append(ehdaa2_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ehdaa2_id, identifier_type="EHDAA2 ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Homo sapiens")
                        anat_list.append(anat_temp)
                        
                # Medaka Fish Anatomy and Development Ontology
                elif "MFO" in result["@id"]:
                    mfo_id = result["@id"].split("/obo/")[1]
                    if mfo_id not in anat_id_array:
                        anat_id_array.append(mfo_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=mfo_id, identifier_type="MFO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Oryzias latipes")
                        anat_list.append(anat_temp)
                        
                # Planarian Anatomy and Developmental Stage Ontology
                elif "PLANA" in result["@id"]:
                    plana_id = result["@id"].split("/obo/")[1]
                    if plana_id not in anat_id_array:
                        anat_id_array.append(plana_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=plana_id, identifier_type="PLANA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Schmidtea mediterranea")
                        anat_list.append(anat_temp)
                        
                # Botryllus schlosseri anatomy and development Ontology
                elif "BSAO" in result["@id"]:
                    bsao_id = result["@id"].split("/obo/")[1]
                    if bsao_id not in anat_id_array:
                        anat_id_array.append(bsao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=bsao_id, identifier_type="BSAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Botryllus schlosseri")
                        anat_list.append(anat_temp)
                        
                # Mouse Gross Anatomy and Development Ontology
                elif "EMAP" in result["@id"]:
                    emap_id = result["@id"].split("/obo/")[1]
                    if emap_id not in anat_id_array:
                        anat_id_array.append(emap_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=emap_id, identifier_type="EMAP ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Mus")
                        anat_list.append(anat_temp)
                        
                # Human Developmental Anatomy Ontology, abstract version 1
                elif "EHDAA" in result["@id"]:
                    ehdaa_id = result["@id"].split("/obo/")[1]
                    if ehdaa_id not in anat_id_array:
                        anat_id_array.append(ehdaa_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ehdaa_id, identifier_type="EHDAA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Homo sapiens")
                        anat_list.append(anat_temp)
                        
                # Ciona intestinalis Anatomy and Development Ontology
                elif "CIINTEADO" in result["@id"]:
                    ciinteado_id = result["@id"].split("/obo/")[1]
                    if ciinteado_id not in anat_id_array:
                        anat_id_array.append(ciinteado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ciinteado_id, identifier_type="CIINTEADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Ciona intestinalis")
                        anat_list.append(anat_temp)
                        
                # Mammalian Feeding Muscle Ontology
                elif "MFMO" in result["@id"]:
                    mfmo_id = result["@id"].split("/obo/")[1]
                    if mfmo_id not in anat_id_array:
                        anat_id_array.append(mfmo_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=mfmo_id, identifier_type="MFMO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Mammalia")
                        anat_list.append(anat_temp)
                        
                # Human Developmental Anatomy Ontology, timed version
                elif "EHDA" in result["@id"]:
                    ehda_id = result["@id"].split("/obo/")[1]
                    if ehda_id not in anat_id_array:
                        anat_id_array.append(ehda_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ehda_id, identifier_type="EHDA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Homo sapiens")
                        anat_list.append(anat_temp)
                        
                # Minimal Anatomical Terminology
                elif "MAT" in result["@id"]:
                    mat_id = result["@id"].split("/obo/")[1]
                    if mat_id not in anat_id_array:
                        anat_id_array.append(mat_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=mat_id, identifier_type="MAT ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        anat_list.append(anat_temp)
                        
                # Ciona savignyi Anatomy and Development Ontology
                elif "CISAVIADO" in result["@id"]:
                    cisaviado_id = result["@id"].split("/obo/")[1]
                    if cisaviado_id not in anat_id_array:
                        anat_id_array.append(cisaviado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=cisaviado_id, identifier_type="CISAVIADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Ciona savignyi")
                        anat_list.append(anat_temp)
                        
                # Halocynthia roretzi Anatomy and Development Ontology
                elif "HAROREADO" in result["@id"]:
                    haroreado_id = result["@id"].split("/obo/")[1]
                    if haroreado_id not in anat_id_array:
                        anat_id_array.append(haroreado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=haroreado_id, identifier_type="HAROREADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Halocynthia roretzi")
                        anat_list.append(anat_temp)
                        
                # Phallusia fumigata Anatomy and Development Ontology
                elif "PHFUMIADO" in result["@id"]:
                    phfumiado_id = result["@id"].split("/obo/")[1]
                    if phfumiado_id not in anat_id_array:
                        anat_id_array.append(phfumiado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=caro_id, identifier_type="PHFUMIADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Phallusia fumigata")
                        anat_list.append(anat_temp)
                        
                # Cephalopod Ontology
                elif "CEPH" in result["@id"]:
                    ceph_id = result["@id"].split("/obo/")[1]
                    if ceph_id not in anat_id_array:
                        anat_id_array.append(ceph_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ceph_id, identifier_type="CEPH ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        anat_list.append(anat_temp)
                        
                # Anatomy Gross Anatomy Ontology
                elif "AAO" in result["@id"]:
                    aao_id = result["@id"].split("/obo/")[1]
                    if aao_id not in anat_id_array:
                        anat_id_array.append(aao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=aao_id, identifier_type="AAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Amphibia")
                        anat_list.append(anat_temp)
                        
                # Phallusia mammillata Anatomy and Development Ontology
                elif "PHMAMMADO" in result["@id"]:
                    phmammado_id = result["@id"].split("/obo/")[1]
                    if phmammado_id not in anat_id_array:
                        anat_id_array.append(phmammado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=phmammado_id, identifier_type="PHMAMMADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Phallusia mammillata")
                        anat_list.append(anat_temp)
                        
                # Molgula occidentalis Anatomy and Development Ontology
                elif "MOOCCIADO" in result["@id"]:
                    moocciado_id = result["@id"].split("/obo/")[1]
                    if moocciado_id not in anat_id_array:
                        anat_id_array.append(moocciado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=moocciado_id, identifier_type="MOOCCIADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Molgula occidentalis")
                        anat_list.append(anat_temp)
                        
                # Ctenophore Ontology
                elif "CTENO" in result["@id"]:
                    cteno_id = result["@id"].split("/obo/")[1]
                    if cteno_id not in anat_id_array:
                        anat_id_array.append(cteno_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=cteno_id, identifier_type="CTENO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Ctenophora")
                        anat_list.append(anat_temp)
                        
                # Mouse gross anatomy and development, timed
                elif "EMAPA" in result["@id"]:
                    emapa_id = result["@id"].split("/obo/")[1]
                    if emapa_id not in anat_id_array:
                        anat_id_array.append(emapa_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=emapa_id, identifier_type="EMAPA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Mus musculus")
                        anat_list.append(anat_temp)
                        
                # Molgula occulta Anatomy and Development Ontology
                elif "MOOCCUADO" in result["@id"]:
                    mooccuado_id = result["@id"].split("/obo/")[1]
                    if mooccuado_id not in anat_id_array:
                        anat_id_array.append(mooccuado_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=mooccuado_id, identifier_type="MOOCCUADO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Molgula occulta")
                        anat_list.append(anat_temp)
                        
                # Common Anatomy Reference Ontology
                elif "CARO" in result["@id"]:
                    caro_id = result["@id"].split("/obo/")[1]
                    if caro_id not in anat_id_array:
                        anat_id_array.append(caro_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=caro_id, identifier_type="CARO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        anat_list.append(anat_temp)
                
                # Vertebrate Homologous Organ Group Ontology
                elif "VHOG" in result["@id"]:
                    vhog_id = result["@id"].split("/obo/")[1]
                    if vhog_id not in anat_id_array:
                        anat_id_array.append(vhog_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=vhog_id, identifier_type="VHOG ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Vertebrata")
                        anat_list.append(anat_temp)
                
                # Tick Gross Anatomy Ontology
                elif "TADS" in result["@id"]:
                    tads_id = result["@id"].split("/obo/")[1]
                    if tads_id not in anat_id_array:
                        anat_id_array.append(tads_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=tads_id, identifier_type="TADS ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=["Ixodidae", "Argassidae"])
                        anat_list.append(anat_temp)
                
                # Spider Ontology
                elif "SPD" in result["@id"]:
                    spd_id = result["@id"].split("/obo/")[1]
                    if spd_id not in anat_id_array:
                        anat_id_array.append(spd_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=spd_id, identifier_type="SPD ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Araneae")
                        anat_list.append(anat_temp)
                        
                # Dictyostelium Discoideum Anatomy Ontology
                elif "DDANAT" in result["@id"]:
                    ddanat_id = result["@id"].split("/obo/")[1]
                    if ddanat_id not in anat_id_array:
                        anat_id_array.append(ddanat_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ddanat_id, identifier_type="DDANAT ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Dictyostelium discoideum")
                        anat_list.append(anat_temp)
                        
                # Body System Terms from ICD-11
                elif "ICD11-BODYSYSTEM" in result["@id"]:
                    icd11_id = result["@id"].split("/obo/")[1]
                    if icd11_id not in anat_id_array:
                        anat_id_array.append(icd11_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=icd11_id, identifier_type="ICD11-BODYSYSTEM Code", source="NCBO BioPortal", name=result["prefLabel"])
                        anat_list.append(anat_temp)
                        
                # Mosquito Gross Anatomy Ontology
                elif "TGMA" in result["@id"]:
                    tgma_id = result["@id"].split("/obo/")[1]
                    if tgma_id not in anat_id_array:
                        anat_id_array.append(tgma_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=tgma_id, identifier_type="TGMA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Culicidae")
                        anat_list.append(anat_temp)
                        
                # Mouse Adult Gross Anatomy Ontology
                elif "MA" in result["@id"]:
                    ma_id = result["@id"].split("/obo/")[1]
                    if ma_id not in anat_id_array:
                        anat_id_array.append(ma_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=ma_id, identifier_type="MA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Mus")
                        anat_list.append(anat_temp)
                        
                # Hymenoptera Anatomy Ontology
                elif "HAO" in result["@id"]:
                    hao_id = result["@id"].split("/obo/")[1]
                    if hao_id not in anat_id_array:
                        anat_id_array.append(hao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=hao_id, identifier_type="HAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Hymenoptera")
                        anat_list.append(anat_temp)

                # Zebrafish Anatomy and Development Ontology
                elif "ZFA" in result["@id"]:
                    zfa_id = result["@id"].split("/obo/")[1]
                    if zfa_id not in anat_id_array:
                        anat_id_array.append(zfa_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=zfa_id, identifier_type="ZFA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Danio rerio")
                        anat_list.append(anat_temp)
                
                # Plant Anatomy
                elif "PAE" in result["@id"]:
                    pae_id = result["@id"].split("/obo/")[1]
                    if pae_id not in anat_id_array:
                        anat_id_array.append(pae_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=pae_id, identifier_type="PAE ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Plantae")
                        anat_list.append(anat_temp)
                        
                # Xenopus Anatomy and Development Ontology
                elif "XAO" in result["@id"]:
                    xao_id = result["@id"].split("/obo/")[1]
                    if xao_id not in anat_id_array:
                        anat_id_array.append(xao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=xao_id, identifier_type="XAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Xenopus laevis")
                        anat_list.append(anat_temp)
                        
                # Uber Anatomy Ontology
                elif "UBERON" in result["@id"]:
                    uberon_id = result["@id"].split("/obo/")[1]
                    if uberon_id not in anat_id_array:
                        anat_id_array.append(uberon_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=uberon_id, identifier_type="UBERON ID", source="NCBO BioPortal", name=result["prefLabel"], taxon=None)
                        anat_list.append(anat_temp)
                        
                # Maize Gross Anatomy Ontology
                elif "ZEA" in result["@id"]:
                    zea_id = result["@id"].split("/obo/")[1]
                    if zea_id not in anat_id_array:
                        anat_id_array.append(zea_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=zea_id, identifier_type="ZEA ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Zea mays")
                        anat_list.append(anat_temp)

                # Drosophila Gross Anatomy Ontology
                elif "FB-BT" in result["@id"]:
                    fbbt_id = result["@id"].split("/obo/")[1]
                    if fbbt_id not in anat_id_array:
                        anat_id_array.append(fbbt_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=fbbt_id, identifier_type="FB-BT ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Drosophila melanogaster")
                        anat_list.append(anat_temp)
                        
                # Fungal Gross Anatomy Ontology
                elif "FAO" in result["@id"]:
                    fao_id = result["@id"].split("/obo/")[1]
                    if fao_id not in anat_id_array:
                        anat_id_array.append(fao_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=fao_id, identifier_type="FAO ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Fungi")
                        anat_list.append(anat_temp)
                        
                # C. elegans Gross Anatomy Ontology
                elif "WB-BT" in result["@id"]:
                    wbbt_id = result["@id"].split("/obo/")[1]
                    if wbbt_id not in anat_id_array:
                        anat_id_array.append(wbbt_id)
                        anat_temp = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier=wbbt_id, identifier_type="WB-BT ID", source="NCBO BioPortal", name=result["prefLabel"], taxon="Caenorhabditis elegans")
                        anat_list.append(anat_temp)
                        
    return anat_list
    
#   UNIT TESTS
def basic_search_unit_tests(basic_query, umls_api_key, ncbo_api_key):
    
    print("Beginning basic search for '%s'..." % basic_query)
    basic_search_results = search(basic_query, source="ebi")
        
    print("\nSearch returned %s result(s) with the following identifiers (EBI):" % str(len(basic_search_results)))
    for anat in basic_search_results:
        for iden in anat.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
            
    user = User(umls_api_key = umls_api_key)
            
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="umls", user=user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nSearch returned %s result(s) with the following identifiers (UMLS):" % str(len(basic_search_results)))
    for anat in basic_search_results:
        for iden in anat.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
            
    user = User(ncbo_api_key = ncbo_api_key)
    
    start = timeit.timeit()
    basic_search_results = search(basic_query, source="ncbo", user=user)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    print("\nSearch returned %s result(s) with the following identifiers (NCBO):" % str(len(basic_search_results)))
    for anat in basic_search_results:
        for iden in anat.identifiers:
            print("- %s: %s (%s)" % (iden["identifier"], iden["name"], iden["identifier_type"]))
    
#   MAIN
if __name__ == "__main__": main()