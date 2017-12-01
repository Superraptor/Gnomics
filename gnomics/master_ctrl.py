#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

#   Import modules.
from gnomics.objects.adverse_event import AdverseEvent
from gnomics.objects.anatomical_structure import AnatomicalStructure
from gnomics.objects.assay import Assay
from gnomics.objects.clinical_trial import ClinicalTrial
from gnomics.objects.compound import Compound
from gnomics.objects.disease import Disease
from gnomics.objects.drug import Drug
from gnomics.objects.gene import Gene
from gnomics.objects.pathway import Pathway
from gnomics.objects.phenotype import Phenotype
from gnomics.objects.procedure import Procedure
from gnomics.objects.protein import Protein
from gnomics.objects.reference import Reference
from gnomics.objects.symptom import Symptom
from gnomics.objects.taxon import Taxon
from gnomics.objects.user import User

#   Other imports.
import json

#   MAIN
def main():
    print("This file is working. API functionality established.")

#   SEARCH
def search(search_query, search_type, user = None):
    if user is not None:
        user = User(email = user["user_email"], eol_api_key = user["eol_api_key"], umls_api_key = user["umls_api_key"], umls_password = user["umls_password"], umls_user = user["umls_username"], chemspider_security_token = user["chemspider_api_key"], omim_api_key = user["omim_api_key"], openphacts_app_id = user["openphacts_app_id"], openphacts_app_key = user["openphacts_app_key"], dpla_api_key = user["dpla_api_key"], springer_api_key = user["springer_api_key"], elsevier_api_key = user["elsevier_api_key"], isbndb_api_key = user["isbndb_api_key"], ncbo_api_key = user["ncbo_api_key"], fda_api_key = user["fda_api_key"])
    
    if search_type == "all":
        all_identifiers = {}
        
        anatomical_structure_results = AnatomicalStructure.search(search_query, user = user)
        anatomical_structure_identifiers = []
        for anatomical_structure in anatomical_structure_results:
            anatomical_structure_identifiers.append(anatomical_structure.identifiers)
        all_identifiers["Anatomical Structures"] = anatomical_structure_identifiers
        
        adverse_event_results = AdverseEvent.search(search_query, user = user)
        adverse_event_identifiers = []
        for adverse_event in adverse_event_results:
            adverse_event_identifiers.append(adverse_event.identifiers)
        all_identifiers["Adverse Events"] = adverse_event_identifiers
        
        assay_results = Assay.search(search_query, user = user)
        assay_identifiers = []
        for assay in assay_results:
            assay_identifiers.append(assay.identifiers)
        all_identifiers["Assays"] = assay_identifiers
        
        clinical_trial_results = ClinicalTrial.search(query=search_query, user = user)
        clinical_trial_identifiers = []
        for clinical_trial in clinical_trial_results:
            clinical_trial_identifiers.append(clinical_trial.identifiers)
        all_identifiers["Clinical Trials"] = clinical_trial_identifiers
        
        compound_results = Compound.search(search_query, user = user)
        compound_identifiers = []
        for compound in compound_results:
            compound_identifiers.append(compound.identifiers)
        all_identifiers["Compounds"] = compound_identifiers
        
        disease_results = Disease.search(search_query, user = user)
        disease_identifiers = []
        for disease in disease_results:
            disease_identifiers.append(disease.identifiers)
        all_identifiers["Diseases"] = disease_identifiers
        
        drug_results = Drug.search(search_query, user = user)
        drug_identifiers = []
        for drug in drug_results:
            drug_identifiers.append(drug.identifiers)
        all_identifiers["Drugs"] = drug_identifiers
        
        gene_results = Gene.search(search_query, user = user)
        gene_identifiers = []
        for gene in gene_results:
            gene_identifiers.append(gene.identifiers)
        all_identifiers["Genes"] = gene_identifiers
        
        phenotype_results = Phenotype.search(search_query, user = user)
        phenotype_identifiers = []
        for phenotype in phenotype_results:
            phenotype_identifiers.append(phenotype.identifiers)
        all_identifiers["Phenotypes"] = phenotype_identifiers
        
        procedure_results = Procedure.search(search_query, user = user)
        procedure_identifiers = []
        for procedure in procedure_results:
            procedure_identifiers.append(procedure.identifiers)
        all_identifiers["Procedures"] = procedure_identifiers
        
        reference_results = Reference.search(query=search_query, user = user)
        reference_identifiers = []
        for reference in reference_results:
            reference_identifiers.append(reference.identifiers)
        all_identifiers["References"] = reference_identifiers
        
        symptom_results = Symptom.search(search_query, user = user)
        symptom_identifiers = []
        for symptom in symptom_results:
            symptom_identifiers.append(symptom.identifiers)
        all_identifiers["Symptoms"] = symptom_identifiers
        
        taxon_results = Taxon.search(search_query, user = user)
        taxon_identifiers = []
        for taxon in taxon_results:
            taxon_identifiers.append(taxon.identifiers)
        all_identifiers["Taxa"] = taxon_identifiers
        
        return all_identifiers
    
    elif search_type == "adverse_event":
        adverse_event_results = AdverseEvent.search(search_query, user = user)
        adverse_event_identifiers = []
        for adverse_event in adverse_event_results:
            adverse_event_identifiers.append(adverse_event.identifiers)
        return adverse_event_identifiers
        
    elif search_type == "anatomical_structure":
        anatomical_structure_results = AnatomicalStructure.search(search_query, user = user)
        anatomical_structure_identifiers = []
        for anatomical_structure in anatomical_structure_results:
            anatomical_structure_identifiers.append(anatomical_structure.identifiers)
        return anatomical_structure_identifiers
    
    elif search_type == "assay":
        assay_results = Assay.search(search_query, user = user)
        assay_identifiers = []
        for assay in assay_results:
            assay_identifiers.append(assay.identifiers)
        return assay_identifiers
        
    elif search_type == "clinical_trial":
        clinical_trial_results = ClinicalTrial.search(query=search_query, user = user)
        clinical_trial_identifiers = []
        for clinical_trial in clinical_trial_results:
            clinical_trial_identifiers.append(clinical_trial.identifiers)
        return clinical_trial_identifiers
        
    elif search_type == "compound":
        compound_results = Compound.search(search_query, user = user)
        compound_identifiers = []
        for compound in compound_results:
            compound_identifiers.append(compound.identifiers)
        return compound_identifiers
    
    elif search_type == "disease":
        disease_results = Disease.search(search_query, user = user)
        disease_identifiers = []
        for disease in disease_results:
            disease_identifiers.append(disease.identifiers)
        return disease_identifiers
    
    elif search_type == "drug":
        drug_results = Drug.search(search_query, user = user)
        drug_identifiers = []
        for drug in drug_results:
            drug_identifiers.append(drug.identifiers)
        return drug_identifiers
    
    elif search_type == "enzyme":
        print("NOT FUNCTIONAL.")
        
    elif search_type == "gene":
        gene_results = Gene.search(search_query, user = user)
        gene_identifiers = []
        for gene in gene_results:
            gene_identifiers.append(gene.identifiers)
        return gene_identifiers
    
    elif search_type == "genotype":
        print("NOT FUNCTIONAL.")
        
    elif search_type == "pathway":
        print("NOT FUNCTIONAL.")
        
    elif search_type == "phenotype":
        phenotype_results = Phenotype.search(search_query, user = user)
        phenotype_identifiers = []
        for phenotype in phenotype_results:
            phenotype_identifiers.append(phenotype.identifiers)
        return phenotype_identifiers
    
    elif search_type == "procedure":
        procedure_results = Procedure.search(search_query, user = user)
        procedure_identifiers = []
        for procedure in procedure_results:
            procedure_identifiers.append(procedure.identifiers)
        return procedure_identifiers
        
    elif search_type == "protein":
        print("NOT FUNCTIONAL.")
        
    elif search_type == "reference":
        reference_results = Reference.search(query=search_query, user = user)
        reference_identifiers = []
        for reference in reference_results:
            reference_identifiers.append(reference.identifiers)
        return reference_identifiers
        
    elif search_type == "symptom":
        symptom_results = Symptom.search(search_query, user = user)
        symptom_identifiers = []
        for symptom in symptom_results:
            symptom_identifiers.append(symptom.identifiers)
        return symptom_identifiers
        
    elif search_type == "taxon":
        taxon_results = Taxon.search(search_query, user = user)
        taxon_identifiers = []
        for taxon in taxon_results:
            taxon_identifiers.append(taxon.identifiers)
        return taxon_identifiers
    
    elif search_type == "variation":
        print("NOT FUNCTIONAL.")
    
    else:
        print("A valid search type was not chosen")
        return []
    
#   IDENTIFIERS
def identifiers(identifier, identifier_type, object_type, language = None, source = None, taxon = None, user = None):
    if object_type == "Anatomical Structures" or object_type == "Anatomical%20Structures":
        temp_anat = AnatomicalStructure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return AnatomicalStructure.all_identifiers(temp_anat)
    elif object_type == "Assays" or object_type == "assays":
        temp_assay = Assay(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Assay.all_identifiers(temp_assay)
    elif object_type == "Compounds" or object_type == "compound":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Compound.all_identifiers(temp_com)
    elif object_type == "Diseases" or object_type == "disease":
        temp_dis = Disease(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Disease.all_identifiers(temp_dis)
    elif object_type == "Drugs" or object_type == "drug":
        temp_drug = Drug(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Drug.all_identifiers(temp_drug)
    elif object_type == "Genes" or object_type == "gene":
        temp_gene = Gene(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Gene.all_identifiers(temp_gene)
    elif object_type == "Phenotypes" or object_type == "phenotype":
        temp_phen = Phenotype(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Phenotype.all_identifiers(temp_phen)
    elif object_type == "References" or object_type == "reference":
        temp_ref = Reference(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Reference.all_identifiers(temp_ref)
    elif object_type == "Taxa" or object_type == "taxon":
        temp_tax = Taxon(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Taxon.all_identifiers(temp_tax)
    else:
        print("A valid object type (%s) was not provided." % str(object_type))
        return []

#   PROPERTIES
def properties(identifier, identifier_type, object_type, language = None, source = None, species = None, user = None):
    print("Not functional.")
    if object_type == "Compounds" or object_type == "compound":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Compound.all_properties(temp_com)
    elif object_type == "Taxa" or object_type == "taxon":
        temp_tax = Taxon(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Taxon.all_properties(temp_tax)
    else:
        print("A valid object type was not provided.")
        return []
    
#   INTERACTION OBJECTS
def interaction_objects(identifier, identifier_type, object_type, language = None, source = None, species = None, user = None):
    print("Not functional.")
    if object_type == "Compounds":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Compound.all_interaction_objects(temp_com, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Diseases":
        temp_dis = Disease(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Disease.all_interaction_objects(temp_dis, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Drugs":
        temp_drug = Drug(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Drug.all_interaction_objects(temp_drug, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Genes":
        temp_gene = Gene(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Gene.all_interaction_objects(temp_gene, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    else:
        print("A valid object type was not provided.")
        return []
    
#   MAIN
if __name__ == "__main__": main()