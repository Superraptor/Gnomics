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

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

#   Import modules.
from gnomics.objects.adverse_event import AdverseEvent
from gnomics.objects.anatomical_structure import AnatomicalStructure
from gnomics.objects.assay import Assay
from gnomics.objects.biological_process import BiologicalProcess
from gnomics.objects.cell_line import CellLine
from gnomics.objects.cellular_component import CellularComponent
from gnomics.objects.clinical_trial import ClinicalTrial
from gnomics.objects.compound import Compound
from gnomics.objects.disease import Disease
from gnomics.objects.drug import Drug
from gnomics.objects.gene import Gene
from gnomics.objects.molecular_function import MolecularFunction
from gnomics.objects.pathway import Pathway
from gnomics.objects.phenotype import Phenotype
from gnomics.objects.procedure import Procedure
from gnomics.objects.protein import Protein
from gnomics.objects.protein_domain import ProteinDomain
from gnomics.objects.protein_family import ProteinFamily
from gnomics.objects.reference import Reference
from gnomics.objects.symptom import Symptom
from gnomics.objects.taxon import Taxon
from gnomics.objects.tissue import Tissue
from gnomics.objects.transcript import Transcript
from gnomics.objects.variation import Variation

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
        
        print("Searching for adverse events...")
        
        adverse_event_results = AdverseEvent.search(search_query, user = user)
        adverse_event_identifiers = []
        for adverse_event in adverse_event_results:
            adverse_event_identifiers.append(adverse_event.identifiers)
        all_identifiers["Adverse Events"] = adverse_event_identifiers
        
        print("Searching for anatomical structures...")
        
        anatomical_structure_results = AnatomicalStructure.search(search_query, user = user)
        anatomical_structure_identifiers = []
        for anatomical_structure in anatomical_structure_results:
            anatomical_structure_identifiers.append(anatomical_structure.identifiers)
        all_identifiers["Anatomical Structures"] = anatomical_structure_identifiers
        
        print("Searching for assays...")
        
        assay_results = Assay.search(search_query, user = user)
        assay_identifiers = []
        for assay in assay_results:
            assay_identifiers.append(assay.identifiers)
        all_identifiers["Assays"] = assay_identifiers
        
        print("Searching for biological processes...")
        
        biological_process_results = BiologicalProcess.search(search_query, user = user)
        biological_process_identifiers = []
        for biological_process in biological_process_results:
            biological_process_identifiers.append(biological_process.identifiers)
        all_identifiers["Biological Processes"] = biological_process_identifiers
        
        print("Searching for cell lines...")
        
        cell_line_results = CellLine.search(search_query, user = user)
        cell_line_identifiers = []
        for cell_line in cell_line_results:
            cell_line_identifiers.append(cell_line.identifiers)
        all_identifiers["Cell Lines"] = cell_line_identifiers
        
        print("Searching for cellular components...")
        
        cellular_component_results = CellularComponent.search(search_query, user = user)
        cellular_component_identifiers = []
        for cellular_component in cellular_component_results:
            cellular_component_identifiers.append(cellular_component.identifiers)
        all_identifiers["Cellular Components"] = cellular_component_identifiers
        
        print("Searching for clinical trials...")
        
        clinical_trial_results = ClinicalTrial.search(query=search_query, user = user)
        clinical_trial_identifiers = []
        for clinical_trial in clinical_trial_results:
            clinical_trial_identifiers.append(clinical_trial.identifiers)
        all_identifiers["Clinical Trials"] = clinical_trial_identifiers
        
        print("Searching for compounds...")
        
        compound_results = Compound.search(search_query, user = user)
        compound_identifiers = []
        for compound in compound_results:
            compound_identifiers.append(compound.identifiers)
        all_identifiers["Compounds"] = compound_identifiers
        
        print("Searching for diseases...")
        
        disease_results = Disease.search(search_query, user = user)
        disease_identifiers = []
        for disease in disease_results:
            disease_identifiers.append(disease.identifiers)
        all_identifiers["Diseases"] = disease_identifiers
        
        print("Searching for drugs...")
        
        drug_results = Drug.search(search_query, user = user)
        drug_identifiers = []
        for drug in drug_results:
            drug_identifiers.append(drug.identifiers)
        all_identifiers["Drugs"] = drug_identifiers
        
        print("Searching for genes...")
        
        gene_results = Gene.search(search_query, user = user)
        gene_identifiers = []
        for gene in gene_results:
            gene_identifiers.append(gene.identifiers)
        all_identifiers["Genes"] = gene_identifiers
        
        print("Searching for molecular functions...")
        
        molecular_function_results = MolecularFunction.search(search_query, user = user)
        molecular_function_identifiers = []
        for molecular_function in molecular_function_results:
            molecular_function_identifiers.append(molecular_function.identifiers)
        all_identifiers["Molecular Functions"] = molecular_function_identifiers
        
        print("Searching for pathways...")
        
        pathway_results = Pathway.search(search_query, user = user)
        pathway_identifiers = []
        for pathway in pathway_results:
            pathway_identifiers.append(pathway.identifiers)
        all_identifiers["Pathways"] = pathway_identifiers
        
        print("Searching for phenotypes...")
        
        phenotype_results = Phenotype.search(search_query, user = user)
        phenotype_identifiers = []
        for phenotype in phenotype_results:
            phenotype_identifiers.append(phenotype.identifiers)
        all_identifiers["Phenotypes"] = phenotype_identifiers
        
        print("Searching for procedures...")
        
        procedure_results = Procedure.search(search_query, user = user)
        procedure_identifiers = []
        for procedure in procedure_results:
            procedure_identifiers.append(procedure.identifiers)
        all_identifiers["Procedures"] = procedure_identifiers
        
        print("Searching for proteins...")
        
        protein_results = Protein.search(search_query, user = user)
        protein_identifiers = []
        for protein in protein_results:
            protein_identifiers.append(protein.identifiers)
        all_identifiers["Proteins"] = protein_identifiers
        
        print("Searching for references...")
        
        reference_results = Reference.search(query=search_query, user = user)
        reference_identifiers = []
        for reference in reference_results:
            reference_identifiers.append(reference.identifiers)
        all_identifiers["References"] = reference_identifiers
        
        print("Searching for symptoms...")
        
        symptom_results = Symptom.search(search_query, user = user)
        symptom_identifiers = []
        for symptom in symptom_results:
            symptom_identifiers.append(symptom.identifiers)
        all_identifiers["Symptoms"] = symptom_identifiers
        
        print("Searching for taxa...")
        
        taxon_results = Taxon.search(search_query, user = user)
        taxon_identifiers = []
        for taxon in taxon_results:
            taxon_identifiers.append(taxon.identifiers)
        all_identifiers["Taxa"] = taxon_identifiers
        
        print("Searching for tissues...")
        
        tissue_results = Tissue.search(search_query, user = user)
        tissue_identifiers = []
        for tissue in tissue_results:
            tissue_identifiers.append(tissue.identifiers)
        all_identifiers["Tissues"] = tissue_identifiers
        
        print("Searching for transcripts...")
        
        transcript_results = Transcript.search(search_query, user = user)
        transcript_identifiers = []
        for transcript in transcript_results:
            transcript_identifiers.append(transcript.identifiers)
        all_identifiers["Transcripts"] = transcript_identifiers
        
        print("Searching for variations...")
        
        variation_results = Variation.search(search_query, user = user)
        variation_identifiers = []
        for variation in variation_results:
            variation_identifiers.append(variation.identifiers)
        all_identifiers["Variations"] = variation_identifiers
        
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
    
    elif search_type == "biological_process":
        biological_process_results = BiologicalProcess.search(search_query, user = user)
        biological_process_identifiers = []
        for biological_process in biological_process_results:
            biological_process_identifiers.append(biological_process.identifiers)
        return biological_process_identifiers
    
    elif search_type == "cell_line":
        cell_line_results = CellLine.search(search_query, user = user)
        cell_line_identifiers = []
        for cell_line in cell_line_results:
            cell_line_identifiers.append(cell_line.identifiers)
        return cell_line_identifiers
    
    elif search_type == "cellular_component":
        cellular_component_results = CellularComponent.search(search_query, user = user)
        cellular_component_identifiers = []
        for cellular_component in cellular_component_results:
            cellular_component_identifiers.append(cellular_component.identifiers)
        return cellular_component_identifiers
        
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
        
    elif search_type == "molecular_function":
        molecular_function_results = MolecularFunction.search(search_query, user = user)
        molecular_function_identifiers = []
        for molecular_function in molecular_function_results:
            molecular_function_identifiers.append(molecular_function.identifiers)
        return molecular_function_identifiers
        
    elif search_type == "pathway":
        pathway_results = Pathway.search(search_query, user = user)
        pathway_identifiers = []
        for pathway in pathway_results:
            pathway_identifiers.append(pathway.identifiers)
        return pathway_identifiers
        
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
        protein_results = Protein.search(search_query, user = user)
        protein_identifiers = []
        for protein in protein_results:
            protein_identifiers.append(protein.identifiers)
        return protein_identifiers
        
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
    
    elif search_type == "tissue":
        tissue_results = Tissue.search(search_query, user = user)
        tissue_identifiers = []
        for tissue in tissue_results:
            tissue_identifiers.append(tissue.identifiers)
        return tissue_identifiers
    
    elif search_type == "transcript":
        transcript_results = Transcript.search(search_query, user = user)
        transcript_identifiers = []
        for transcript in transcript_results:
            transcript_identifiers.append(transcript.identifiers)
        return transcript_identifiers
    
    elif search_type == "variation":
        variation_results = Variation.search(search_query, user = user)
        variation_identifiers = []
        for variation in variation_results:
            variation_identifiers.append(variation.identifiers)
        return variation_identifiers
    
    else:
        print("A valid search type (%s) was not chosen" % str(search_type))
        return []
    
#   IDENTIFIERS
def identifiers(identifier, identifier_type, object_type, language = None, source = None, taxon = None, user = None):
    if object_type == "Adverse Events" or object_type == "Adverse%20Events" or object_type == "adverse_event" or object_type == "adverse event":
        temp_adverse = AdverseEvent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return AdverseEvent.all_identifiers(temp_adverse)
    elif object_type == "Anatomical Structures" or object_type == "Anatomical%20Structures" or object_type == "anatomical_structure" or object_type == "anatomical structure":
        temp_anat = AnatomicalStructure(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return AnatomicalStructure.all_identifiers(temp_anat)
    elif object_type == "Assays" or object_type == "assays" or object_type == "assay":
        temp_assay = Assay(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Assay.all_identifiers(temp_assay)
    elif object_type == "Biological Processes" or object_type == "Biological%20Processes" or object_type == "biological_process" or object_type == "biological process":
        temp_bioproc = BiologicalProcess(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return BiologicalProcess.all_identifiers(temp_bioproc)
    elif object_type == "Cell Lines" or object_type == "Cell%20Lines" or object_type == "cell_line" or object_type == "cell line":
        temp_cellline = CellLine(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return CellLine.all_identifiers(temp_cellline)
    elif object_type == "Cellular Components" or object_type == "Cellular%20Components" or object_type == "cellular_component" or object_type == "cellular component":
        temp_cellcomp = CellularComponent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return CellularComponent.all_identifiers(temp_cellcomp)
    elif object_type == "Clinical Trials" or object_type == "Clinical%20Trials" or object_type == "clinical_trial" or object_type == "clinical trial":
        temp_trial = ClinicalTrial(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return ClinicalTrial.all_identifiers(temp_trial)
    elif object_type == "Compounds" or object_type == "compound":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Compound.all_identifiers(temp_com)
    elif object_type == "Diseases" or object_type == "disease":
        temp_dis = Disease(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Disease.all_identifiers(temp_dis)
    elif object_type == "Drugs" or object_type == "drug":
        temp_drug = Drug(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Drug.all_identifiers(temp_drug)
    elif object_type == "Genes" or object_type == "gene" or object_type == "Gene":
        temp_gene = Gene(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Gene.all_identifiers(temp_gene)
    elif object_type == "Molecular Functions" or object_type == "Molecular%20Functions" or object_type == "molecular_function" or object_type == "molecular function":
        temp_molecftn = MolecularFunction(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return MolecularFunction.all_identifiers(temp_molecftn)
    elif object_type == "Pathways" or object_type == "pathway":
        temp_path = Pathway(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Pathway.all_identifiers(temp_path)
    elif object_type == "Phenotypes" or object_type == "phenotype":
        temp_phen = Phenotype(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Phenotype.all_identifiers(temp_phen)
    elif object_type == "Procedures" or object_type == "procedure":
        temp_proced = Procedure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Procedure.all_identifiers(temp_proced)
    elif object_type == "Protein" or object_type == "Proteins" or object_type == "protein":
        temp_prot = Protein(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Protein.all_identifiers(temp_prot)
    elif object_type == "References" or object_type == "reference":
        temp_ref = Reference(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Reference.all_identifiers(temp_ref)
    elif object_type == "Symptoms" or object_type == "symptom":
        temp_symp = Symptom(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Symptom.all_identifiers(temp_symp)
    elif object_type == "Taxa" or object_type == "taxon":
        temp_tax = Taxon(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Taxon.all_identifiers(temp_tax)
    elif object_type == "Tissue" or object_type == "Tissues" or object_type == "tissue":
        temp_tiss = Tissue(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Tissue.all_identifiers(temp_tiss)
    elif  object_type == "Transcript" or object_type == "Transcripts" or object_type == "transcript":
        temp_trans = Transcript(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Transcript.all_identifiers(temp_trans)
    elif object_type == "Variations" or object_type == "variation":
        temp_var = Variation(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Variation.all_identifiers(temp_var)
    else:
        print("A valid object type (%s) was not provided." % str(object_type))
        return []

#   PROPERTIES
def properties(identifier, identifier_type, object_type, language = None, source = None, taxon = None, user = None):
    if object_type == "Adverse Events" or object_type == "adverse event":
        temp_ae = AdverseEvent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return AdverseEvent.all_properties(temp_ae)
    elif object_type == "Anatomical Structures" or object_type == "anatomical structure":
        temp_anat = AnatomicalStructure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return AnatomicalStructure.all_properties(temp_anat)
    elif object_type == "Assays" or object_type == "assay":
        temp_assay = Assay(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Assay.all_properties(temp_assay)
    elif object_type == "Biological Processes" or object_type == "biological process":
        temp_bioproc = BiologicalProcess(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return BiologicalProcess.all_properties(temp_bioproc)
    elif object_type == "Cell Lines" or object_type == "cell line":
        temp_cell_line = CellLine(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return CellLine.all_properties(temp_cell_line)
    elif object_type == "Cellular Components" or object_type == "cellular component":
        temp_cellcomp = CellularComponent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return CellularComponent.all_properties(temp_cellcomp)
    elif object_type == "Clinical Trials" or object_type == "clinical trial":
        temp_clin = ClinicalTrial(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return ClinicalTrial.all_properties(temp_clin)
    elif object_type == "Compounds" or object_type == "compound":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Compound.all_properties(temp_com)
    elif object_type == "Diseases" or object_type == "disease":
        temp_dis = Disease(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Disease.all_properties(temp_dis)
    elif object_type == "Drugs" or object_type == "drug":
        temp_drug = Drug(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Drug.all_properties(temp_drug)
    elif object_type == "Genes" or object_type == "gene" or object_type == "Gene":
        temp_gene = Gene(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Gene.all_properties(temp_gene)
    elif object_type == "Molecular Functions" or object_type == "molecular function":
        temp_molec_ftn = MolecularFunction(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return MolecularFunction.all_properties(temp_molec_ftn)
    elif object_type == "Pathways" or object_type == "pathway":
        temp_path = Pathway(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Pathway.all_properties(temp_path)
    elif object_type == "Phenotypes" or object_type == "phenotype":
        temp_phen = Phenotype(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Phenotype.all_properties(temp_phen)
    elif object_type == "Procedures" or object_type == "procedure":
        temp_proc = Procedure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Procedure.all_properties(temp_proc)
    elif object_type == "Protein" or object_type == "Proteins" or object_type == "protein":
        temp_prot = Protein(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Protein.all_properties(temp_prot)
    elif object_type == "References" or object_type == "reference":
        temp_ref = Reference(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Reference.all_properties(temp_ref)
    elif object_type == "Symptoms" or object_type == "symptom":
        temp_symp = Symptom(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Symptom.all_properties(temp_symp)
    elif object_type == "Taxa" or object_type == "taxon":
        temp_tax = Taxon(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Taxon.all_properties(temp_tax)
    elif object_type == "Tissue" or object_type == "Tissues" or object_type == "tissue":
        temp_tiss = Tissue(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        return Tissue.all_properties(temp_tiss)
    elif object_type == "Transcript" or object_type == "Transcripts" or object_type == "transcript":
        temp_trans = Transcript(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Transcript.all_properties(temp_trans)
    elif object_type == "Variations" or object_type == "variation":
        temp_var = Variation(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        return Variation.all_properties(temp_var)
    else:
        print("A valid object type (%s) was not provided." % str(object_type))
        return []
    
#   INTERACTION OBJECTS
def interaction_objects(identifier, identifier_type, object_type, language = None, source = None, taxon = None, user = None):
    if object_type == "Adverse Events" or object_type == "adverse event":
        temp_ae = AdverseEvent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in AdverseEvent.all_interaction_objects(temp_ae, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Anatomical Structures" or object_type == "anatomical structure":
        temp_anat = AnatomicalStructure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in AnatomicalStructure.all_interaction_objects(temp_anat, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Assays" or object_type == "assay":
        temp_assay = Assay(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Assay.all_interaction_objects(temp_assay, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Biological Processes" or object_type == "biological process":
        temp_bioproc = BiologicalProcess(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in BiologicalProcess.all_interaction_objects(temp_bioproc, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Cell Lines" or object_type == "cell line":
        temp_cell_line = CellLine(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in CellLine.all_interaction_objects(temp_cell_line, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Cellular Components" or object_type == "cellular component":
        temp_cellcomp = CellularComponent(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in CellularComponent.all_interaction_objects(temp_cellcomp, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Clinical Trials" or object_type == "clinical trial":
        temp_clin = ClinicalTrial(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in ClinicalTrial.all_interaction_objects(temp_clin, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Compounds" or object_type == "compound":
        temp_com = Compound(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Compound.all_interaction_objects(temp_com, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Diseases" or object_type == "disease":
        temp_dis = Disease(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Disease.all_interaction_objects(temp_dis, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Drugs" or object_type == "drug":
        temp_drug = Drug(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Drug.all_interaction_objects(temp_drug, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Genes" or object_type == "gene" or object_type == "Gene":
        temp_gene = Gene(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        interaction_obj = {}
        for key, value in Gene.all_interaction_objects(temp_gene, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Molecular Functions" or object_type == "molecular function":
        temp_molec_ftn = MolecularFunction(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in MolecularFunction.all_interaction_objects(temp_molec_ftn, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Pathways" or object_type == "pathway":
        temp_path = Pathway(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Pathway.all_interaction_objects(temp_path, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Phenotypes" or object_type == "phenotype":
        temp_phen = Phenotype(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Phenotype.all_interaction_objects(temp_phen, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Procedures" or object_type == "procedure":
        temp_proced = Procedure(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Procedure.all_interaction_objects(temp_proced, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Protein" or object_type == "Proteins" or object_type == "protein":
        temp_prot = Protein(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        interaction_obj = {}
        for key, value in Protein.all_interaction_objects(temp_prot, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "References" or object_type == "reference":
        temp_ref = Reference(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Reference.all_interaction_objects(temp_ref, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Symptoms" or object_type == "symptom":
        temp_symp = Symptom(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Symptom.all_interaction_objects(temp_symp, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Taxa" or object_type == "taxon":
        temp_tax = Taxon(identifier = identifier, identifier_type = identifier_type, language = language, source = source)
        interaction_obj = {}
        for key, value in Taxon.all_interaction_objects(temp_tax, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Tissues" or object_type == "tissue":
        temp_tiss = Tissue(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        interaction_obj = {}
        for key, value in Tissue.all_interaction_objects(temp_tiss, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Transcript" or object_type == "Transcripts" or object_type == "transcript":
        temp_trans = Transcript(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        interaction_obj = {}
        for key, value in Transcript.all_interaction_objects(temp_trans, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    elif object_type == "Variations" or object_type == "variation":
        temp_var = Variation(identifier = identifier, identifier_type = identifier_type, language = language, source = source, taxon = taxon)
        interaction_obj = {}
        for key, value in Variation.all_interaction_objects(temp_var, user = user).items():
            interaction_obj[key] = []
            for obj in value:
                interaction_obj[key].append(obj.identifiers)
        return interaction_obj
    else:
        print("A valid object type (%s) was not provided." % str(object_type))
        return []
    
#   MAIN
if __name__ == "__main__": main()