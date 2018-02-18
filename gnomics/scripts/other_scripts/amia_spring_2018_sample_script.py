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
#	Sample script for AMIA 2018 presentation.
#	
#
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
from gnomics.objects.anatomical_structure import AnatomicalStructure
from gnomics.objects.drug import Drug
from gnomics.objects.gene import Gene
from gnomics.objects.phenotype import Phenotype
from gnomics.objects.reference import Reference

#   MAIN
def main():

	# Get drug-gene interactions.
	gene_object = Gene(identifier="MS4A1", identifier_type="HGNC Symbol")
	drug_interactions = Gene.drug_interactions(gene_object)
	for drug in drug_interactions:
		for identifier in drug.identifiers:
			print("- %s (%s)" % (identifier["identifier"], identifier["identifier_type"]))
			
	# Get variations associated with a phenotype.
	phenotype_object = Phenotype(identifier="Glaucoma", identifier_type="Human Phenotype Ontology Term")
	variations_associated_with_phenotype = Phenotype.variations(phenotype_object)
	for variation in variations_associated_with_phenotype:
		for identifier in variation.identifiers:
			print("- %s (%s)" % (identifier["identifier"], identifier["identifier_type"]))
			
	# Get PDF document from PubMed ID.
	reference_object = Reference(identifier="13054692", identifier_type="PubMed ID")
	Reference.download_pdf(reference_object)
	
	# Get German term for "pancreas".
	anatomical_structure_object = AnatomicalStructure(identifier="Pancreas", identifier_type="Wikipedia Accession")
	AnatomicalStructure.wikipedia_accession(anatomical_structure_object, language="German")
	
#   MAIN
if __name__ == "__main__": main()