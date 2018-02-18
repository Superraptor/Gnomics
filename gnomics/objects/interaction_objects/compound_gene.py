#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#

#
#   Get genes from a compound.
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
import gnomics.objects.compound
import gnomics.objects.gene

#   Other imports.
import pubchempy as pubchem
import json
import requests
import timeit

#   MAIN
def main():
    gene_unit_tests("36462")
    
# Get genes.
#
# http://dgidb.genome.wustl.edu/api
#
# Interaction sources can be TTD, DrugBank, etc.
# But should be an array if possible.
def get_genes(com, source=None, interaction_sources=None, interaction_types=None, gene_categories=None, source_trust_levels=None):
    gen_array = []
    gen_id_array = []
    
    for related_obj in com.related_objects:
        if 'object_type' in related_obj:
            if related_obj['object_type'].lower() == "gene":
                any_in = 0
                for iden in related_obj['object'].identifiers:
                    if iden not in gen_array:
                        gen_id_array.append(iden)
                        gen_array.append(related_obj["object"])
                    else:
                        any_in = any_in + 1
                if any_in == 0:
                    gen_array.append(related_obj["object"])
                        
    for ident in com.identifiers:
        if ident["identifier_type"].lower() in ["pubchem cid", "cid"]:
            
            # Get all sources.
            if source is None or source.lower() in ["all"]:
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v1/interactions.json?drugs=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if gene_categories is not None:
                    ext = ext + (",".join(gene_categories)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                
                for term in decoded["matchedTerms"]:
                    for interact in term["interactions"]:
                        if interact["geneName"] and interact["geneLongName"] not in gen_array:
                            temp_gen = gnomics.objects.gene.Gene(identifier = interact["geneName"], identifier_type = "HGNC Approved Symbol", language = None, taxon = "Homo sapiens", source = interact["source"])
                            temp_gen.add_identifier(identifier = interact["geneLongName"], identifier_type = "HGNC Approved Name", language = "en", taxon = "Homo sapiens", source = interact["source"])
                            
                            com.related_objects.append({
                                "object": temp_gen,
                                "object_type": "Gene",
                                "identifier": interact["interactionId"],
                                "identifier_type": interact["interactionType"],
                                "source": interact["source"]
                            })
                            gen_id_array.append(interact["geneName"])
                            gen_id_array.append(interact["geneLongName"])
                            gen_array.append(temp_gen)
            
            elif source.lower() in ["dgidb"]:
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v1/interactions.json?drugs=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if gene_categories is not None:
                    ext = ext + (",".join(gene_categories)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()

                for term in decoded["matchedTerms"]:
                    for interact in term["interactions"]:
                        if interact["geneName"] and interact["geneLongName"] not in gen_array:
                            temp_gen = gnomics.objects.gene.Gene(identifier = interact["geneName"], identifier_type = "HGNC Approved Symbol", language = None, taxon = "Homo sapiens", source = interact["source"])
                            temp_gen.add_identifier(identifier = interact["geneLongName"], identifier_type = "HGNC Approved Name", language = "en", taxon = "Homo sapiens", source = interact["source"])
                            
                            com.related_objects.append({
                                "object": temp_gen,
                                "object_type": "Gene",
                                "identifier": interact["interactionId"],
                                "identifier_type": interact["interactionType"],
                                "source": interact["source"]
                            })
                            gen_id_array.append(interact["geneName"])
                            gen_id_array.append(interact["geneLongName"])
                            gen_array.append(temp_gen)
                            
        elif ident["identifier_type"].lower() in ["chembl", "chembl id", "chembl identifier"]:
            
            # Get all sources.
            if source is None or source.lower() in ["all"]:
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v1/interactions.json?drugs=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if gene_categories is not None:
                    ext = ext + (",".join(gene_categories)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()
                
                for term in decoded["matchedTerms"]:
                    for interact in term["interactions"]:
                        if interact["geneName"] and interact["geneLongName"] not in gen_array:
                            temp_gen = gnomics.objects.gene.Gene(identifier = interact["geneName"], identifier_type = "HGNC Approved Symbol", language = None, taxon = "Homo sapiens", source = interact["source"])
                            temp_gen.add_identifier(identifier = interact["geneLongName"], identifier_type = "HGNC Approved Name", language = "en", taxon = "Homo sapiens", source = interact["source"])
                            
                            com.related_objects.append({
                                "object": temp_gen,
                                "object_type": "Gene",
                                "identifier": interact["interactionId"],
                                "identifier_type": interact["interactionType"],
                                "source": interact["source"]
                            })
                            gen_id_array.append(interact["geneName"])
                            gen_id_array.append(interact["geneLongName"])
                            gen_array.append(temp_gen)
            
            elif source.lower() in ["dgidb"]:
                server = "http://dgidb.genome.wustl.edu"
                ext = "/api/v1/interactions.json?drugs=" + ident["identifier"]

                if interaction_sources is not None:
                    ext = ext + (",".join(interaction_sources)).replace(" ", "%20")
                if interaction_types is not None:
                    ext = ext + (",".join(interaction_types)).replace(" ", "%20")
                if gene_categories is not None:
                    ext = ext + (",".join(gene_categories)).replace(" ", "%20")
                if source_trust_levels is not None:
                    ext = ext + (",".join(source_trust_levels)).replace(" ", "%20")

                r = requests.get(server+ext, headers={"Content-Type": "application/json"})

                if not r.ok:
                    r.raise_for_status()
                    sys.exit()

                decoded = r.json()

                for term in decoded["matchedTerms"]:
                    for interact in term["interactions"]:
                        if interact["geneName"] and interact["geneLongName"] not in gen_array:
                            temp_gen = gnomics.objects.gene.Gene(identifier = interact["geneName"], identifier_type = "HGNC Approved Symbol", language = None, taxon = "Homo sapiens", source = interact["source"])
                            temp_gen.add_identifier(identifier = interact["geneLongName"], identifier_type = "HGNC Approved Name", language = "en", taxon = "Homo sapiens", source = interact["source"])
                            
                            com.related_objects.append({
                                "object": temp_gen,
                                "object_type": "Gene",
                                "identifier": interact["interactionId"],
                                "identifier_type": interact["interactionType"],
                                "source": interact["source"]
                            })
                            gen_id_array.append(interact["geneName"])
                            gen_id_array.append(interact["geneLongName"])
                            gen_array.append(temp_gen)
    
    return gen_array

#   UNIT TESTS
def gene_unit_tests(pubchem_cid):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting genes from PubChem CID (%s):" % pubchem_cid)
    
    start = timeit.timeit()
    all_genes = get_genes(pubchem_com)
    end = timeit.timeit()
    print("TIME ELAPSED: %s seconds." % str(end - start))
    
    for gen in all_genes:
        for iden in gen.identifiers:
            if iden["identifier_type"].lower() == "hgnc approved symbol":
                print("- %s, %s, %s, %s" % (str(iden["identifier"]), str(iden["identifier_type"]), str(iden["language"]), str(iden["source"])))
    
#   MAIN
if __name__ == "__main__": main()