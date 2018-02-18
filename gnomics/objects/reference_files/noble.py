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
#   Get Noble results.
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
import gnomics.objects.disease
import gnomics.objects.pathway
import gnomics.objects.reference

#   Other imports.
from bioservices import *
import json
import re
import requests
import shutil
import subprocess
import tempfile

#   MAIN
def main():
    noble_unit_tests("28723805")
    
# Return Noble vocabulary from text.
# http://noble-tools.dbmi.pitt.edu/
#
# Usage:
# java -jar NobleCoderTool.jar -terminology <name> -input <dir> -output <dir> [options]
#
# Parameters:
# -terminology :: Terminology to use. All terminologies are located in 
# <user.home>/.terminologies directory.
# -input :: Input directory containing a set of text files with (.txt)
# extension.
# -output :: Output directory where RESULT.csv output will be stored along with
# output HTML files.
# -search :: Search strategy among the following: 
# <best-match|precise-match|all-match|nonoverlap-match|partial-match|custom-match>
# -stripDigits :: Don't try to match stand-alone digits.
# -stripSmallWords :: Don't try to match one letter words.
# -stripCommonWords :: Don't try to match most common English words.
# -selectBestCandidates :: For each match only select the best candidate.
# -semanticTypes :: <list of semantic types> only include matches from given
# semantic types.
# -sources :: <list of sources> only include matches from a given list of sources.
# -slidingWindow :: <N> don't consider words that are N words apart to be
# part of the same concept.
# -abbreviations :: <whitelist text file> a custom text file that suppresses all
# abbreviations except the ones in a list.
# -ignoreUsedWords :: Speed up search by not considering words that are already part
# of some concept.
# -subsumptionMode :: Subsume more general concepts if more specific concept is found.
# -overlapMode :: Overlapping concepts are allowed.
# -contiguousMode :: Matched terms must be contiguous in text.
# -orderedMode :: Matched terms must use the same word order in text.
# -partialMode :: Match a term if more than 50% of its words are found in text.
# -acronymExpansion :: If acronym is found in its expanded form, use its meaning
# to tag all other mentions of it.
# -negationDetection :: invoke ConText algorithm to detect negated concepts
# and other modifiers.
def noble(pubmed_ref = None, pmid = None, input_terminology = "NCI_Thesaurus"): # ADD ALL OF THE ABOVE AS PARAMS
    if pmid is not None:
        pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
        abstract_text = gnomics.objects.reference.Reference.abstract(pubmed_ref)
        
        # Save abstract text to a temp file.
        commandname = "cat"
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(bytes(abstract_text, "UTF-8"))
        f.close()

        # Run subprocess.
        subprocess.call(['java', '-jar', '../../NobleCoder-1.0.jar', '-terminology', input_terminology, '-input', f.name, '-output', './noble_output']) # , '<options>'])
        
        # java -jar NobleCoderTool.jar -terminology <name> -input <dir> -output <dir> [options]
        
        # Read info from output files.
        code_dict = {}
        with open("./noble_output/RESULTS.tsv") as f:
            for line in f:
                line_array = line.split("\t")
                document_title = line_array[0]
                matched_term = line_array[1]
                code = line_array[2]
                concept_name = line_array[3]
                semantic_type = line_array[4]
                annotations = line_array[5]
                certainty = line_array[6]
                contextual_aspect = line_array[7]
                contextual_modality = line_array[8]
                degree = line_array[9]
                experiencer = line_array[10]
                permanence = line_array[11]
                polarity = line_array[12]
                temporality = line_array[13]
                
                code_dict[code] = concept_name
        
        # Delete abstract text file.
        os.unlink(f.name)
        
        # Delete results directory.
        shutil.rmtree("./noble_output")
        
        # Return dictionary.
        return code_dict
        
    elif pubmed_ref is not None:
        print("NOT FUNCTIONAL.")
        
        for ident in pubmed_ref.identifiers:
            if ident["identifier_type"].lower() in ["pmid", "pubmed", "pubmed id", "pubmed identifier"]:
                abstract_text = gnomics.objects.reference.Reference.abstract(pubmed_ref)
        
                # Save abstract text to a temp file.
                commandname = "cat"
                f = tempfile.NamedTemporaryFile(delete=False)
                f.write(bytes(abstract_text, "UTF-8"))
                f.close()

                # Run subprocess.
                subprocess.call(['java', '-jar', '../../NobleCoder-1.0.jar', '-terminology', input_terminology, '-input', f.name, '-output', './noble_output']) # , '<options>'])

                # java -jar NobleCoderTool.jar -terminology <name> -input <dir> -output <dir> [options]

                # Read info from output files.
                code_dict = {}
                with open("./noble_output/RESULTS.tsv") as f:
                    for line in f:
                        line_array = line.split("\t")
                        document_title = line_array[0]
                        matched_term = line_array[1]
                        code = line_array[2]
                        concept_name = line_array[3]
                        semantic_type = line_array[4]
                        annotations = line_array[5]
                        certainty = line_array[6]
                        contextual_aspect = line_array[7]
                        contextual_modality = line_array[8]
                        degree = line_array[9]
                        experiencer = line_array[10]
                        permanence = line_array[11]
                        polarity = line_array[12]
                        temporality = line_array[13]

                        code_dict[code] = concept_name

                # Delete abstract text file.
                os.unlink(f.name)

                # Delete results directory.
                shutil.rmtree("./noble_output")

                # Return dictionary.
                return code_dict
            
    elif pubmed_ref is None and pmid is None:
        print("A PubMed reference object or a PMID must be provided in order to use PubTator.")
        return ""
    else:
        print("An unknown error occurred.")
        return ""
        
#   UNIT TESTS
def noble_unit_tests(pmid):
    print("Getting Noble results from raw PMID...")
    for code, term in noble(pmid = pmid).items():
        print("- %s, %s" % (code, term))
    
    print("\nGetting Noble results from PubMed reference...")
    pubmed_ref = gnomics.objects.reference.Reference(identifier = pmid, identifier_type = "PMID", language = None, source = "PubMed")
    for code, term in noble(pubmed_ref = pubmed_ref).items():
        print("- %s, %s" % (code, term))
    

#   MAIN
if __name__ == "__main__": main()