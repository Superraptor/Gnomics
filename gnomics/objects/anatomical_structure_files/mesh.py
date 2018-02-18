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
#   Get MeSH.
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
import gnomics.objects.auxiliary_files.umls
import gnomics.objects.auxiliary_files.wiki

#   Other imports.
import json
import requests
import timeit

#   MAIN
def main():
    mesh_unit_tests("21", "50801", "Q199507", "")

# Return MeSH UID.
def get_mesh_uid(anat, user=None, source="umls"):
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["mesh", "mesh uid", "mesh unique id", "mesh unique identifier", "msh", "msh uid", "msh unique id", "msh unique identifier"]):
        if iden["identifier"] not in mesh_array:
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSH", iden["identifier"])
            
            for x in found_array:
                if x not in mesh_array:
                    mesh_array.append(x)
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH UID", language = None, source = "UMLS")
                        
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSH", iden["identifier"])
            
            for x in found_array:
                if x not in mesh_array:
                    mesh_array.append(x)
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH UID", language = None, source = "UMLS")
            
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
        
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh id", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH UID", language = None, source = "Wikidata")
                        
    if mesh_array:
        return mesh_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in ids_completed and iden["language"] == "en":
            ids_completed.append(iden["identifier"])
        
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh id", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH UID", language = None, source = "Wikidata")
                                
    if mesh_array:
        return mesh_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh id", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH UID", language = None, source = "Wikidata")

    return mesh_array
            
# Get English MeSH term (MSH).
def get_mesh_term_english(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "en":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSH", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="en", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSH", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="en", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
            
# Get MeSH tree number.
def get_mesh_tree_number(anat, user=None):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["mesh tn", "mesh tree number", "msh tn", "msh tree number"]):
        if iden["identifier"] not in mesh_array:
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikidata", "wikidata accession", "wikidata id", "wikidata identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
        
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh code", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")
    
    if mesh_array:
        return mesh_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["wikipedia", "wikipedia accession", "wikipedia article"]):
        if iden["identifier"] not in ids_completed and iden["language"] == "en":
            ids_completed.append(iden["identifier"])
        
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh code", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")
                                
    if mesh_array:
        return mesh_array
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uberon", "uberon id", "uberon identifier"]):
        if iden["identifier"] not in ids_completed:
            ids_completed.append(iden["identifier"])
            gnomics.objects.anatomical_structure.AnatomicalStructure.wikipedia_accession(anat, language = "en")
            
            for wikidata_object in gnomics.objects.anatomical_structure.AnatomicalStructure.wikidata(anat):

                found_array = gnomics.objects.auxiliary_files.wiki.wikidata_property_check(wikidata_object, "mesh code", wikidata_property_language = "en")

                for x in found_array:
                    if x not in mesh_array:
                        mesh_array.append(x)
                        gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier = x, identifier_type = "MeSH Tree Number", language = None, source = "Wikidata")

    return mesh_array
    
# Get Czech MeSH term (MSHCZE).
def get_mesh_term_czech(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshcze", "mshcze label", "mshcze name", "mshcze term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "cs":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHCZE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="cs", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHCZE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="cs", source="UMLS Metathesaurus", name=x[1])

    return mesh_array

# Get Dutch MeSH term (MSHDUT).
def get_mesh_term_dutch(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshdut", "mshdut label", "mshdut name", "mshdut term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "nl":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHDUT", iden["identifier"], other="name", verbose=False)
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="nl", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHDUT", iden["identifier"], other="name", verbose=False)
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="nl", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Finnish MeSH term (MSHFIN).
def get_mesh_term_finnish(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshdut", "mshdut label", "mshdut name", "mshdut term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "fi":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHFIN", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="fi", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHFIN", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="fi", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get French MeSH term (MSHFRE).
def get_mesh_term_french(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshfre", "mshfre label", "mshfre name", "mshfre term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "fr":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHFRE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="fr", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHFRE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="fr", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get German MeSH term (MSHGER).
def get_mesh_term_german(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshger", "mshger label", "mshger name", "mshger term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "de":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHGER", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="de", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHGER", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="de", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Italian MeSH term (MSHITA).
def get_mesh_term_italian(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshita", "mshita label", "mshita name", "mshita term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "it":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHITA", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="it", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHITA", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="it", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Japanese MeSH term (MSHJPN).
def get_mesh_term_japanese(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshjpn", "mshjpn label", "mshjpn name", "mshjpn term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "fi":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHJPN", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="ja", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHJPN", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="ja", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Latvian MeSH term (MSHLAV).
def get_mesh_term_latvian(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshlav", "mshlav label", "mshlav name", "mshlav term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "lv":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHLAV", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="lv", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHLAV", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="lv", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Norwegian MeSH term (MSHNOR).
def get_mesh_term_norwegian(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshnor", "mshnor label", "mshnor name", "mshnor term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "no":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHNOR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="no", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHNOR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="no", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Polish MeSH term (MSHPOL).
def get_mesh_term_polish(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshpol", "mshpol label", "mshpol name", "mshpol term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "pl":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHPOL", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="pl", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHPOL", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="pl", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Portuguese MeSH term (MSHPOR).
def get_mesh_term_portuguese(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshpor", "mshpor label", "mshpor name", "mshpor term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "pt":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHPOR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="pt", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHPOR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="pt", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Russian MeSH term (MSHRUS).
def get_mesh_term_russian(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshrus", "mshrus label", "mshrus name", "mshrus term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "ru":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHRUS", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="ru", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHRUS", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="ru", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Croatian MeSH term (MSHSCR).
def get_mesh_term_croatian(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshscr", "mshscr label", "mshscr name", "mshscr term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "hr":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHSCR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="hr", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHSCR", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="hr", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Spanish MeSH term (MSHSPA).
def get_mesh_term_spanish(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshspa", "mshspa label", "mshspa name", "mshspa term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "es":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHSPA", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="es", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHSPA", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="es", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
# Get Swedish MeSH term (MSHSWE).
def get_mesh_term_swedish(anat, user=None, source="umls"):
    
    mesh_array = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["medical subject headings label", "medical subject headings name", "medical subject headings term", "mesh label", "mesh name", "mesh term", "msh label", "msh name", "msh term", "mshswe", "mshswe label", "mshswe name", "mshswe term"]):
        if iden["identifier"] not in mesh_array and iden["language"] == "sv":
            mesh_array.append(iden["identifier"])
            
    if mesh_array:
        return mesh_array
    
    ids_completed = []
    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["neu", "neu id", "neu identifier", "neuronames brain hierarchy id", "neuronames brain hierarchy identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "NEU", "MSHSWE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="sv", source="UMLS Metathesaurus", name=x[1])
                    
    for iden in gnomics.objects.auxiliary_files.identifier.filter_identifiers(anat.identifiers, ["uwda", "uwda id", "uwda identifier"]):
        if iden["identifier"] not in ids_completed and source == "umls":
            ids_completed.append(iden["identifier"])
            
            found_array = gnomics.objects.auxiliary_files.umls.umls_crosswalk(user, "UWDA", "MSHSWE", iden["identifier"], other="name")
            
            for x in found_array:
                if x[1] not in mesh_array:
                    mesh_array.append(x[1])
                    gnomics.objects.anatomical_structure.AnatomicalStructure.add_identifier(anat, identifier=x[0], identifier_type="MeSH Term", language="sv", source="UMLS Metathesaurus", name=x[1])

    return mesh_array
    
#   UNIT TESTS
def mesh_unit_tests(neu_id, uwda_id, wikidata_accession, umls_api_key):
    
    wikidata_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = wikidata_accession, identifier_type = "Wikidata Accession", source = "Wikidata")
    
    print("\nGetting MeSH UID from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    mesh_array = get_mesh_uid(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting MeSH tree number from Wikidata Accession (%s):" % wikidata_accession)
    start = timeit.timeit()
    mesh_array = get_mesh_tree_number(wikidata_anat)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    user = User(umls_api_key = umls_api_key)
            
    neu_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = neu_id, identifier_type = "NEU ID", source = "UMLS")
        
    print("\nGetting MeSH ID from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_uid(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting English MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_english(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Czech MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_czech(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Dutch MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_dutch(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Finnish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_finnish(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting French MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_french(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting German MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_german(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Italian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_italian(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting Latvian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_latvian(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Norwegian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_norwegian(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Polish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_polish(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Portuguese MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_portuguese(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Croatian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_croatian(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Spanish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_spanish(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Swedish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_swedish(neu_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    uwda_anat = gnomics.objects.anatomical_structure.AnatomicalStructure(identifier = uwda_id, identifier_type = "UWDA ID", source = "UMLS")
        
    print("\nGetting MeSH ID from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_uid(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting English MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_english(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Czech MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_czech(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Dutch MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_dutch(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Finnish MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_finnish(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting French MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_french(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting German MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_german(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Italian MeSH term from UWDA ID (%s):" % uwda_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_italian(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
    print("\nGetting Latvian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_latvian(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Norwegian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_norwegian(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Polish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_polish(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Portuguese MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_portuguese(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Croatian MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_croatian(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Spanish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_spanish(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
        
    print("\nGetting Swedish MeSH term from NEU ID (%s):" % neu_id)
    start = timeit.timeit()
    mesh_array = get_mesh_term_swedish(uwda_anat, user = user)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for mesh in mesh_array:
        print("\t- " + str(mesh))
    
#   MAIN
if __name__ == "__main__": main()