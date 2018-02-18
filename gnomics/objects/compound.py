#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#       CHEMBL
#           https://github.com/chembl/chembl_webresource_client
#       CHEMOPY
#           https://www.researchgate.net/publication/235919352_UserGuide_for_chemopy
#       CHEMSPIPY
#           http://chemspipy.readthedocs.io/en/latest/
#       LIBCHEBIPY
#           https://github.com/libChEBI/libChEBIpy
#       PUBCHEMPY
#           https://pypi.python.org/pypi/PubChemPy/1.0
#       WIKIPEDIA
#           https://pypi.python.org/pypi/wikipedia
#

#
#   Create instance of a compound.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS

#   Imports for recognizing modules.
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

#   Import modules.
from gnomics.objects.user import User
import gnomics.objects.pathway

#   Other imports.
from bioservices import *
from chembl_webresource_client.new_client import new_client
from chemspipy import ChemSpider as chemspider
from libchebipy import ChebiEntity, ChebiException, Comment, CompoundOrigin, DatabaseAccession, Formula, Name, Reference, Relation, Structure
import json
import pubchempy as pubchem
import re
import requests
import signal
import timeit
import wikipedia

#   Import sub-methods.
from gnomics.objects.compound_files.beilstein import get_beilstein_rn
from gnomics.objects.compound_files.cas import get_cas
from gnomics.objects.compound_files.chebi import get_chebi_id, get_chebi_entity
from gnomics.objects.compound_files.chembl import get_chembl_id, get_chembl_molecule
from gnomics.objects.compound_files.common_names import get_common_names
from gnomics.objects.compound_files.conceptwiki import get_conceptwiki_id
from gnomics.objects.compound_files.cs import get_chemspider_id, get_chemspider_compound
from gnomics.objects.compound_files.inchi import get_inchi, get_inchi_key, get_standard_inchi, get_standard_inchi_key
from gnomics.objects.compound_files.iupac import get_iupac_name
from gnomics.objects.compound_files.kegg import get_kegg_compound_id, get_kegg_compound_db_entry
from gnomics.objects.compound_files.lincs import get_lincs_id
from gnomics.objects.compound_files.mesh import get_mesh_uid, get_mesh_rn, get_mesh_term_english
from gnomics.objects.compound_files.molecular_formula import get_molecular_formula
from gnomics.objects.compound_files.pdbechem import get_pdbechem_id
from gnomics.objects.compound_files.pubchem import get_pubchem_cids, get_pubchem_sids, get_pubchem_compound
from gnomics.objects.compound_files.registry import get_registry_id
from gnomics.objects.compound_files.schembl import get_schembl_id
from gnomics.objects.compound_files.search import search
from gnomics.objects.compound_files.smiles import get_smiles, get_canonical_smiles, get_isomeric_smiles
from gnomics.objects.compound_files.wiki import get_english_wikipedia_accession, get_wikidata_object

#   Import further methods.
from gnomics.objects.interaction_objects.compound_adverse_event import get_adverse_events
from gnomics.objects.interaction_objects.compound_assay import get_assays
from gnomics.objects.interaction_objects.compound_disease import get_diseases
from gnomics.objects.interaction_objects.compound_drug import get_drugs
from gnomics.objects.interaction_objects.compound_gene import get_genes
from gnomics.objects.interaction_objects.compound_patent import get_patents
from gnomics.objects.interaction_objects.compound_pathway import get_pathways
from gnomics.objects.interaction_objects.compound_protein import get_protein
from gnomics.objects.interaction_objects.compound_reference import get_references

#   Imports that may be added in future versions.
# from pychem import bcut, connectivity, constitution, getmol, pychem, kappa, topology
# from pychem.pychem import Chem, pybel, PyChem2d, PyChem3d

#   MAIN
def main():
    compound_unit_tests("6918092", "33510", "fd4ce40f-23e5-44be-91f5-a40b92ab1580")

#   COMPOUND CLASS
class Compound(object):
    """
        Compound class:
    
        Representing chemical compounds, which 
        (according to the Encyclopedia Britannica) are 
        "substance[s] composed of identical molecules
        consisting of atoms of two or more chemical
        elements."
    
    """
    
    # CHEBI BioPortal PURL.
    chebi_bioportal_purl = "http://purl.bioontology.org/ontology/CHEBI"
    
    # MESH BioPortal PURL.
    mesh_bioportal_purl = "http://purl.bioontology.org/ontology/MESH"
    
    """
        Compound attributes:
        
        Identifier      = A particular way to identify the
                          compound in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the compound.
    def __init__(self, identifier=None, identifier_type=None, language=None, source=None, name=None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = []
        if identifier is not None:
            self.identifiers = [{
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }]
        
        # Initialize dictionary of compound objects.
        self.compound_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a compound.
    def add_identifier(compound, identifier=None, identifier_type=None, language=None, source=None, name=None):
        compound.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a compound.
    def add_object(compound, obj=None, object_type=None):
        compound.compound_objects.append({
            'object': obj,
            'object_type': object_type
        })
        
    """
        Compound objects:
        
        ChEBI Entity
        ChEMBL Molecule
        ChemSpider Compound
        KEGG Compound
        PubChem Compound
        Pybel MOL
        Wikidata Object
        
    """
    
    # Return ChEBI entity.
    def chebi_entity(compound, user=None):
        return get_chebi_entity(compound, user=user)
    
    # Returns ChEMBL molecule.
    def chembl_molecule(compound, user=None):
        return get_chembl_molecule(compound, user=user)
    
    # Returns ChemSpider compound.
    def chemspider_compound(compound, user=None):
        return get_chemspider_compound(compound, user=user)
        
    # Returns RxNorm object containing all properties.
    def rxnorm_object(compound, user=None):
        return get_rxnorm_obj(compound)
        
    # KEGG database entry (for compound).
    def kegg_compound_db_entry(compound, user=None):
        return get_kegg_compound_db_entry(compound)
    
    # Returns PubChem compound from CID.
    def pubchem_compound(compound, user=None):
        return get_pubchem_compound(compound, user=user)
    
    # Returns Wikidata object.
    def wikidata(compound, user=None):
        return get_wikidata_object(compound)
    
    """
        Compound identifiers:
        
        BAN
        Beilstein registry number
        Canonical SMILES
        CAS registry number
        ChEBI identifier
        ChEMBL identifier
        ChemSpider identifier
        Common name
        ConceptWiki identifier
        InChI
        InChI key
        Isomeric SMILES
        IUPAC name
        KEGG COMPOUND identifier
        LINCS accession
        MeSH registry number
        MeSH Term
        MeSH UID
        Molecular formula
        PDBeChem accession
        PubChem CID
        PubChem SIDs
        SCHEMBL ID
        SMILES
        Standard InChI
        Standard InChI key
        Wikipedia accession
    """
    
    # Return all identifiers.
    def all_identifiers(compound, user=None):
        Compound.beilstein_rn(compound, user=user)
        Compound.canonical_smiles(compound, user=user)
        Compound.chebi_id(compound, user=user)
        Compound.chembl_id(compound, user=user)
        Compound.chemspider_id(compound, user=user)
        Compound.cas(compound, user=user)
        Compound.common_names(compound, user=user)
        Compound.conceptwiki_id(compound, user=user)
        Compound.inchi(compound, user=user)
        Compound.inchi_key(compound, user=user)
        Compound.isomeric_smiles(compound, user=user)
        Compound.iupac_name(compound, user=user)
        Compound.kegg_compound_id(compound, user=user)
        Compound.lincs_id(compound, user=user)
        Compound.mesh_uid(compound, user=user)
        Compound.molecular_formula(compound, user=user)
        Compound.pdbechem_id(compound, user=user)
        Compound.pubchem_cid(compound, user=user)
        Compound.pubchem_sids(compound, user=user)
        Compound.smiles(compound, user=user)
        Compound.standard_inchi(compound, user=user)
        Compound.standard_inchi_key(compound, user=user)
        Compound.wikipedia_accession(compound, user=user)
        return compound.identifiers
    
    # Returns Beilstein registry number.
    def beilstein_rn(compound, user=None):
        return get_beilstein_rn(compound)
    
    # Returns canonical SMILES.
    def canonical_smiles(compound, user=None):
        return get_canonical_smiles(compound)
        
    # Returns ChEBI identifier.
    def chebi_id(compound, user=None):
        return get_chebi_id(compound, user=user)
            
    # Returns ChEMBL identifier.
    def chembl_id(compound, user=None):
        return get_chembl_id(compound, user=user)
    
    # Returns ChemSpider identifier.
    def chemspider_id(compound, user=None):
        return get_chemspider_id(compound, user=user)
            
    # Returns CAS registry number.
    def cas(compound, user=None):
        return get_cas(compound, user=user)
            
    # Returns common names.
    def common_names(compound, user=None):
        return get_common_names(compound, user=user)
    
    # Returns ConceptWiki identifier.
    def conceptwiki_id(compound, user=None):
        return get_conceptwiki_id(compound, user=user)
    
    # Returns InChI (IUPAC International Chemical Identifier).
    def inchi(compound, user=None):
        return get_inchi(compound, user=user)
            
    # Returns InChI key.
    def inchi_key(compound, user=None):
        return get_inchi_key(compound, user=user)
    
    # Returns isomeric SMILES.
    def isomeric_smiles(compound, user=None):
        return get_isomeric_smiles(compound, user=user)
    
    # Returns IUPAC name.
    def iupac_name(compound, user=None):
        return get_iupac_name(compound, user=user)
    
    # Returns KEGG Compound identifier.
    def kegg_compound_id(compound, user=None):
        return get_kegg_compound_id(compound, user=user)
    
    # Returns LINCS accession.
    def lincs_id(compound, user=None):
        return get_lincs_id(compound, user=user)
    
    # Returns MeSH RN.
    def mesh_rn(compound, user=None):
        return get_mesh_rn(compound, user=user) 
    
    # Returns MeSH Term.
    def mesh_term(compound, language="en", user=None):
        if language.lower() in ["eng", "en", "english", "all"]:
            return get_mesh_term_english(compound, user = user)
        else:
             print("The given language is not currently supported.")
    
    # Returns MeSH UID.
    def mesh_uid(compound, user=None):
        return get_mesh_uid(compound)
    
    # Returns molecular formula.
    def molecular_formula(compound, user=None):
        return get_molecular_formula(compound)
    
    # Returns PDBeChem accession.
    def pdbechem_id(compound, user=None):
        return get_pdbechem_id(compound)
    
    # Returns PubChem CID (compound record).
    def pubchem_cid(compound, user=None):
        return get_pubchem_cids(compound, user)
            
    # Returns PubChem SIDs (substance records).
    def pubchem_sids(compound, user=None):
        return get_pubchem_sids(compound, user=None)
    
    # Returns SCHEMBL ID.
    def schembl_id(compound, user=None):
        return get_schembl_id(compound)
    
    # Returns SMILES.
    def smiles(compound, user=None):
        return get_smiles(compound, user)
            
    # Returns standard InChI (IUPAC International Chemical Identifier).
    def standard_inchi(compound, user=None):
        return get_standard_inchi(compound, user=user)
   
    # Returns standard InChI key.
    def standard_inchi_key(compound, user=None):
        return get_standard_inchi_key(compound, user=user)
            
    # Returns Wikipedia accession.
    def wikipedia_accession(compound, user=None, language="en"):
        if language.lower() in ["en", "eng", "english", "all"]:
            return get_english_wikipedia_accession(compound, user = user)
        else:
            print("The given language is not currently supported.")
    
    """
        Interaction objects:
        
        Adverse events
        Assays
        Diseases
        Genes
        Patents
        Pathways
        References
        
    """
    
    # Return interaction objects.
    def all_interaction_objects(compound, user=None):
        interaction_obj = {}
        interaction_obj["Adverse_Events"] = Compound.adverse_events(compound, user=user)
        interaction_obj["Assays"] = Compound.assays(compound, user=user)
        interaction_obj["Diseases"] = Compound.diseases(compound, user=user)
        interaction_obj["Drugs"] = Compound.drugs(compound, user=user)
        interaction_obj["Genes"] = Compound.genes(compound, user=user)
        interaction_obj["Patents"] = Compound.patents(compound, user=user)
        interaction_obj["Pathways"] = Compound.pathways(compound, user=user)
        interaction_obj["References"] = Compound.references(compound, user=user)
        return interaction_obj
        
    # Returns adverse event objects.
    def adverse_events(compound, user=None):
        return get_adverse_events(compound, user=user)
        
    # Returns assay objects.
    def assays(compound, user=None):
        return get_assays(compound, user=user)
    
    # Return disease objects.
    def diseases(compound, user=None):
        return get_diseases(compound, user=user)
    
    # Return drug objects.
    def drugs(compound, user=None):
        return get_drugs(compound, user=user)
    
    # Get gene interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def genes(compound, source=None, interaction_sources=None, interaction_types=None, gene_categories=None, source_trust_levels=None, user=None):
        return get_genes(compound, source, interaction_sources, interaction_types, gene_categories, source_trust_levels)
    
    # Returns patent accession.
    def patents(compound, user=None):
        return get_patents(compound)
    
    # Get pathways related to compound (KEGG).
    #
    # For pathway associations, either
    # "inferred" or "enriched" may be used.
    def pathways(compound, source=None, pathway_assoc=None, user=None):
        return get_pathways(compound, source=source, pathway_assoc=pathway_assoc, user=user)
    
    # Returns protein cross-references.
    def protein(compound, user=None):
        return get_protein(compound)
    
    # Returns sources/references.
    def references(compound, user=None):
        return get_references(compound)
    
    """
        Other properties:
        
        2D depiction as binary data in PNG format
        3D conformer identifier
        3D mmff94 energy
        3D mmff94 partial charges
        3D multipoles
        3D pharmacophore features
        3D RMSD conformer
        3D shape fingerprint
        3D shape self-overlap
        3D volume
        Adverse events
        AlogP
        Atom stereo count
        Atoms
        Average mass
        Bond stereo count
        Bonds
        Charge
        Comments
        Complexity
        Coordinate type
        Covalent unit count
        Created by
        Defined atom stereo count
        Definition
        Effective rotor count
        Exact mass
        Fingerprint
        H bond acceptor count
        H bond donor count
        Heavy atom count
        Indication class
        Isotope atom count
        Mass
        Modified on
        MOL
        Molecular weight
        Molecule type
        Monoisotopic mass
        Nominal mass
        Oral
        Prodrug
        Rotatable bond count
        Spectra
        Star
        Topical
        Topology
        tPSA
        Undefined atom stereo count
        URL of PNG image of 2D chemical structure
        Wikipedia content
        Wikipedia links
        Wikipedia page
        Wikipedia page title
        XlogP
        Year approved
        
    """
    
    # Return all properties in this category.
    def all_properties(compound, user=None):
        property_dict = {}
        property_dict["AlogP"] = Compound.alogp(compound, user=user)
        property_dict["Atom Stereo Count"] = Compound.atom_stereo_count(compound, user=user)
        property_dict["Average Mass"] = Compound.average_mass(compound, user=user)
        property_dict["Bond Stereo Count"] = Compound.bond_stereo_count(compound, user=user)
        property_dict["Charge"] = Compound.charge(compound, user=user)
        property_dict["2D depiction as binary data in PNG format"] = Compound.chem_2d_struct_binary_png_image(compound, user=user)
        property_dict["URL of 2D depiction as binary data in PNG format"] = Compound.chem_2d_struct_url_png_image(compound, user=user)
        property_dict["Complexity"] = Compound.complexity(compound, user=user)
        property_dict["3D Conformer ID"] = Compound.conformer_id_3d(compound, user=user)
        property_dict["3D RMSD Conformer"] = Compound.conformer_rmsd_3d(compound, user=user)
        property_dict["Coordinate Type"] = Compound.coordinate_type(compound, user=user)
        property_dict["Covalent Unit Count"] = Compound.covalent_unit_count(compound, user=user)
        property_dict["Creator"] = Compound.created_by(compound, user=user)
        property_dict["Defined Atom Stereo Count"] = Compound.defined_atom_stereo_count(compound, user=user)
        property_dict["Definition"] = Compound.definition(compound, user=user)
        property_dict["Effective Rotor Unit Count"] = Compound.effective_rotor_count(compound, user=user)
        property_dict["Exact Mass"] = Compound.exact_mass(compound, user=user)
        property_dict["Date First Approved"] = Compound.first_approval(compound, user=user)
        property_dict["3D Shape Selfoverlap"] = Compound.shape_selfoverlap_3d(compound, user=user)
        property_dict["Fingerprint"] = Compound.fingerprint(compound, user=user)
        property_dict["H Bond Acceptor Count"] = Compound.h_bond_acceptor_count(compound, user=user)
        property_dict["H Bond Donor Count"] = Compound.h_bond_donor_count(compound, user=user)
        property_dict["Indication Class"] = Compound.indication_class(compound, user=user)
        property_dict["Isotope Atom Count"] = Compound.isotope_atom_count(compound, user=user)
        property_dict["Mass"] = Compound.mass(compound)
        property_dict["3D mmff94 Energy"] = Compound.mmff94_energy_3d(compound, user=user)
        property_dict["3D mmff94 Partial Charges"] = Compound.mmff94_partial_charges_3d(compound, user=user)
        property_dict["Molecular Weight"] = Compound.molecular_weight(compound, user=user)
        property_dict["Molecule Type"] = Compound.molecule_type(compound, user=user)
        property_dict["Monoisotopic Mass"] = Compound.monoisotopic_mass(compound, user=user)
        property_dict["3D Multipoles"] = Compound.multipoles_3d(compound, user=user)
        property_dict["Nominal Mass"] = Compound.nominal_mass(compound, user=user)
        property_dict["Oral"] = Compound.oral(compound)
        property_dict["Parenteral"] = Compound.parenteral(compound, user=user)
        property_dict["Prodrug"] = Compound.prodrug(compound, user=user)
        property_dict["3D Pharmacophore Features"] = Compound.pharmacophore_features_3d(compound, user=user)
        property_dict["Rotatable Bond Count"] = Compound.rotatable_bond_count(compound, user=user)
        property_dict["3D Shape Fingerprint"] = Compound.shape_fingerprint_3d(compound, user=user)
        property_dict["Spectra"] = Compound.spectra(compound, user=user)
        property_dict["Star"] = Compound.star(compound, user=user)
        property_dict["Topical"] = Compound.topical(compound, user=user)
        property_dict["Topology"] = Compound.topology(compound)
        property_dict["tPSA"] = Compound.tpsa(compound, user=user)
        property_dict["Undefined Atom Stereo Count"] = Compound.undefined_atom_stereo_count(compound, user=user)
        property_dict["3D Volume"] = Compound.volume_3d(compound, user=user)
        
        return property_dict
    
    # Returns AlogP.
    def alogp(compound, user=None, source="chembl", verbose=False):
        if source == "chemspider" and user is not None:
            alogp_array = []
            for sub_com in Compound.chemspider_compound(compound, user = user):
                alogp_array.append(sub_com.alogp)
            return alogp_array
        elif source == "chemspider" and user is None:
            if verbose:
                print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            alogp_array = []
            for sub_com in Compound.chembl_molecule(compound):
                alogp_array.append(sub_com["molecule_properties"]["alogp"])
            return alogp_array
        elif source == "chembl":
            alogp_array = []
            for sub_com in Compound.chembl_molecule(compound):
                alogp_array.append(sub_com["molecule_properties"]["alogp"])
            return alogp_array
        else:
            print("Only ChemSpider and ChEMBL sources are currently supported for this function.")
            return ""
    
    # Returns atom stereo count.
    def atom_stereo_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.atom_stereo_count)
        return prop_array
    
    # Returns atoms.
    def atoms(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.atoms)
        return prop_array
    
    # Returns the average mass.
    def average_mass(compound, source="chemspider", user=None, verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.average_mass)
            return prop_array
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
            return []
    
    # Returns bond stereo count.
    def bond_stereo_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.bond_stereo_count)
        return prop_array
    
    # Returns bonds.
    def bonds(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.bonds)
        return prop_array
    
    # Returns charge.
    def charge(compound, source="pubchem", user=None):
        if source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.charge)
            return prop_array
        elif source.lower() in ["chebi", "all"]:
            prop_array = []
            for sub_com in Compound.chebi_entity(compound):
                prop_array.append(sub_com.get_charge())
            return prop_array
        
    # Returns a 2D depiction as binary data in PNG format.
    def chem_2d_struct_binary_png_image(compound, user=None, source="chemspider", verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.image)
            return prop_array
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
            return []
    
    # Returns URL of a PNG image of the 2D chemical structure.
    def chem_2d_struct_url_png_image(compound, user=None, source="chemspider", verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.image_url)
            return prop_array
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
            return []
    
    # Returns comments.
    def comments(compound, source="chebi", user=None):
        if source.lower() in ["chebi", "all"]:
            prop_array = []
            for sub_com in Compound.chebi_entity(compound):
                prop_array.append(sub_com.get_comments())
            return prop_array
        else:
            print("Currently, only ChEBI comments are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns complexity.
    def complexity(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.complexity)
        return prop_array
    
    # Returns 3D conformer ID:
    def conformer_id_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.conformer_id_3d)
        return prop_array
    
    # Returns 3D RMSD conformer.
    def conformer_rmsd_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.conformer_rmsd_3d)
        return prop_array
    
    # Returns coordinate type.
    def coordinate_type(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.coordinate_type)
        return prop_array
    
    # Returns covalent unit count.
    def covalent_unit_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.covalent_unit_count)
        return prop_array
    
    # Returns who the record was created by or the method by which the record was created.
    def created_by(compound, source="chebi", user=None):
        if source.lower() in ["chebi", "all"]:
            prop_array = []
            for sub_com in Compound.chebi_entity(compound):
                prop_array.append(sub_com.get_created_by())
            return prop_array
        else:
            print("Currently, only ChEBI creation record types are supported. Please specify 'chebi' as source.")
            return []
    
    # Returns defined atom stereo count.
    def defined_atom_stereo_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.defined_atom_stereo_count)
        return prop_array
    
    # Returns definition.
    def definition(compound, source="chebi", user=None):
        if source.lower() in ["chebi", "all"]:
            prop_array = []
            for sub_com in Compound.chebi_entity(compound):
                if sub_com.get_definition() not in prop_array:
                    prop_array.append(sub_com.get_definition())
            return prop_array
        else:
            print("Currently, only ChEBI definitions are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns effective rotor count.
    def effective_rotor_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            if hasattr(sub_com, "effective_rotor_count"):
                prop_array.append(sub_com.effective_rotor_count)
        return prop_array
    
    # Returns exact mass.
    def exact_mass(compound, source="pubchem", user=None):
        if source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.exact_mass)
            return prop_array
        elif source.lower() in ["kegg", "all"]:
            prop_array = []
            for sub_com in Compound.kegg_compound_db_entry(compound):
                prop_array.append(sub_com["EXACT_MASS"])
            return prop_array
        else:
            print("Only PubChem and KEGG sources are currently supported for this function.")
            return []
    
    # Returns year first approved.
    def first_approval(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["first_approval"])
        return prop_array
    
    # Returns 3D feature selfoverlap.
    def shape_selfoverlap_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.shape_selfoverlap_3d)
        return prop_array
    
    # Returns fingerprint.
    def fingerprint(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.fingerprint)
        return prop_array
    
    # Returns H bond acceptor count.
    def h_bond_acceptor_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.h_bond_acceptor_count)
        return prop_array
    
    # Returns H bond donor count.
    def h_bond_donor_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.h_bond_donor_count)
        return prop_array
    
    # Returns heavy atom count.
    def heavy_atom_count(compound, source="pubchem", user=None):
        if source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.heavy_atom_count)
            return prop_array
        else:
            print("Only PubChem sources are currently supported for this function.")
            return []
    
    # Returns indication class.
    def indication_class(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["indication_class"])
        return prop_array
    
    # Returns isotope atom count.
    def isotope_atom_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.isotope_atom_count)
        return prop_array
    
    # Returns mass.
    def mass(compound, user=None):
        prop_array = []
        for sub_com in Compound.chebi_entity(compound):
            if sub_com.get_mass() not in prop_array:
                prop_array.append(sub_com.get_mass())
        return prop_array
    
    # Returns 3D mmff94 energy.
    def mmff94_energy_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.mmff94_energy_3d)
        return prop_array
    
    # Returns 3D mmff94 partial charges.
    def mmff94_partial_charges_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.mmff94_partial_charges_3d)
        return prop_array
    
    # Returns date modified as datetime object (for ChEBI).
    def modified_on(compound, source="chebi", user=None):
        if source.lower() in ["chebi", "all"]:
            prop_array = []
            for sub_com in Compound.chebi_entity(compound):
                prop_array.append(sub_com.get_modified_on())
            return prop_array
        else:
            print("Currently, only ChEBI modification dates are supported. Please specify 'chebi' as source.")
            return []
    
    # Returns MOL.
    def mol(compound, user=None):
        prop_array = []
        for sub_com in Compound.chebi_entity(compound):
            prop_array.append(sub_com.get_mol())
        return prop_array
        
    # Returns the molecular weight.
    def molecular_weight(compound, user=None, source="pubchem"):
        if source.lower() in ["chemspider", "all"]:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user = user):
                prop_array.append(sub_com.molecular_weight)
            return prop_array       
        elif source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user = user):
                prop_array.append(sub_com.molecular_weight)
            return prop_array
        elif source.lower() in ["kegg", "all"]:
            prop_array = []
            for sub_com in Compound.kegg_compound_db_entry(compound):
                prop_array.append(sub_com["MOL_WEIGHT"])
            return prop_array
        else:
            print("Only PubChem sources, ChemSpider sources, and KEGG sources are currently supported for this function.")
            return ""
        
    # Returns molecule type.
    def molecule_type(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["molecule_type"])
        return prop_array
        
    # Returns the monoisotopic mass.
    def monoisotopic_mass(compound, user=None, source="chembl", verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.monoisotopic_mass)
            return prop_array
        elif source.lower() in ["chemspider", "all"] and user is None:
            if verbose:
                print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            prop_array = []
            for sub_com in Compound.chembl_molecule(compound):
                prop_array.append(sub_com["molecule_properties"]["mw_monoisotopic"])
            return prop_array
        elif source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.monoisotopic_mass)
            return prop_array
        elif source.lower() in ["chembl", "all"]:
            prop_array = []
            for sub_com in Compound.chembl_molecule(compound):
                prop_array.append(sub_com["molecule_properties"]["mw_monoisotopic"])
            return prop_array
        
    # Returns 3D multipoles.
    def multipoles_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.multipoles_3d)
        return prop_array
    
    # Returns the nominal mass.
    def nominal_mass(compound, user=None, source="chemspider", verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.nominal_mass)
            return prop_array
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
            return []
    
    # Returns whether oral (True) or not (False).
    def oral(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["oral"])
        return prop_array
    
    # Returns whether parenteral (True) or not (False).
    def parenteral(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["parenteral"])
        return prop_array
    
    # Returns whether prodrug (True) or not (False).
    # According to IUPAC, a prodrug is a "[c]ompound
    # that undergoes biotransformation before
    # exhibiting pharmacological effects."
    def prodrug(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound):
            prop_array.append(sub_com["prodrug"])
        return prop_array
    
    # Returns 3D pharmacophore features.
    def pharmacophore_features_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.pharmacophore_features_3d)
        return prop_array
    
    # Returns rotatable bond count.
    def rotatable_bond_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.rotatable_bond_count)
        return prop_array
    
    # Returns 3D shape fingerprint.
    def shape_fingerprint_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.shape_fingerprint_3d)
        return prop_array
    
    # Returns spectra.
    def spectra(compound, user=None, source="chemspider", verbose=False):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.spectra)
            return prop_array
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
            return []
    
    # Returns star.
    def star(compound, user=None):
        prop_array = []
        for sub_com in Compound.chebi_entity(compound, user=user):
            if sub_com.get_star() not in prop_array:
                prop_array.append(sub_com.get_star())
        return prop_array
    
    # Returns whether topical (True) or not (False).
    def topical(compound, user=None):
        prop_array = []
        for sub_com in Compound.chembl_molecule(compound, user=user):
            prop_array.append(sub_com["topical"])
        return prop_array
    
    # Returns topology.
    def topology(compound, verbose=False, user=None):
        if verbose:
            print("PyBel sources are experimental and not currently functional. As such, neither is this function.")
        return []
    
    # Returns tPSA (topological polar surface area).
    def tpsa(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.tpsa)
        return prop_array
    
    # Returns undefined atom stereo count.
    def undefined_atom_stereo_count(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.undefined_atom_stereo_count)
        return prop_array
    
    # Returns 3D volume.
    def volume_3d(compound, user=None):
        prop_array = []
        for sub_com in Compound.pubchem_compound(compound, user=user):
            prop_array.append(sub_com.volume_3d)
        return prop_array
        
    # Returns Wikipedia content.
    def wikipedia_content(compound, user=None):
        if Compound.wikipedia_page(compound, user=user) is not None and Compound.wikipedia_page(compound, user=user) != "":
            prop_array = []
            for sub_com in Compound.wikipedia_page(compound, user=user):
                prop_array.append(sub_com.content)
            return prop_array
    
    # Returns Wikipedia links.
    def wikipedia_links(compound, user=None):
        if Compound.wikipedia_page(compound, user=user) is not None and Compound.wikipedia_page(compound, user=user) != "":
            prop_array = []
            for sub_com in Compound.wikipedia_page(compound, user=user):
                prop_array.append(sub_com.links)
            return prop_array
        
    # Returns Wikipedia page.
    def wikipedia_page(compound, user=None):
        if Compound.wikipedia_accession(compound, user=user) is not None and Compound.wikipedia_accession(compound, user=user) != "":
            prop_array = []
            for acc in Compound.wikipedia_accession(compound, user=user):
                prop_array.append(wikipedia.page(acc))
            return prop_array
    
    # Returns Wikipedia page title.
    def wikipedia_url(compound, user=None):
        if Compound.wikipedia_page(compound, user=user) is not None and Compound.wikipedia_page(compound, user=user) != "":
            prop_array = []
            for sub_com in Compound.wikipedia_page(compound, user=user):
                prop_array.append(sub_com.title)
            return prop_array
        
    # Returns XlogP.
    def xlogp(compound, user=None, source="pubchem"):
        if source.lower() in ["chemspider", "all"] and user is not None:
            prop_array = []
            for sub_com in Compound.chemspider_compound(compound, user=user):
                prop_array.append(sub_com.xlogp)
            return prop_array
        elif source.lower() in ["chemspider", "all"] and user is None:
            print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.xlogp)
            return prop_array
        elif source.lower() in ["pubchem", "all"]:
            prop_array = []
            for sub_com in Compound.pubchem_compound(compound, user=user):
                prop_array.append(sub_com.xlogp)
            return prop_array
        else:
            print("Only ChemSpider and PubChem sources are currently supported for this function.")
            return ""
        
    """
        URLs:
        
        ChEBI URL
        ChEMBL URL
        ChemSpider URL
        KEGG COMPOUND URL
        PDB URL
        PubChem URL
        ChEBI-REACTOME URL
        Wikipedia URL
        
    """
    
    # Return links.
    def all_urls(compound, user=None):
        url_dict = {}
        url_dict["ChEBI"] = Compound.chebi_url(compound, user=user)
        url_dict["ChEMBL"] = Compound.chembl_url(compound, user=user)
        url_dict["ChemSpider"] = Compound.chemspider_url(compound, user=user)
        url_dict["KEGG COMPOUND"] = Compound.kegg_compound_url(compound, user=user)
        url_dict["PDB"] = Compound.pdb_url(compound, user=user)
        url_dict["PubChem"] = Compound.pubchem_url(compound, user=user)
        url_dict["ChEBI-REACTOME"] = Compound.reactome_chebi_url(compound, user=user)
        url_dict["Wikipedia"] = Compound.wikipedia_url(compound, user=user)
        return url_dict
    
    # Returns ChEBI URL.
    def chebi_url(compound, user=None):
        url_array = []
        for chebi_id in Compound.chebi_id(compound, user=user):
            url_array.append("https://www.ebi.ac.uk/chebi/searchId.do?chebiId=" + str(chebi_id))
        return url_array
    
    # Returns ChEMBL URL.
    def chembl_url(compound, user=None):
        url_array = []
        for chembl_id in Compound.chembl_id(compound, user=user):
            url_array.append("https://www.ebi.ac.uk/chembldb/index.php/compound/inspect/" + str(chembl_id))
        return url_array
    
    # Returns ChemSpider URL.
    def chemspider_url(compound, user=None, verbose=False):
        url_array = []
        if user is not None:
            for csid in Compound.chemspider_id(compound, user=user):
                url_array.append("http://www.chemspider.com/Chemical-Structure." + str(csid) + ".html")
        else:
            if verbose:
                print("No valid ChemSpider API security token provided. Cannot return value.")
        return url_array
    
    # Returns KEGG Compound URL.
    def kegg_compound_url(compound, user=None):
        url_array = []
        for kegg_compound_id in Compound.kegg_compound_id(compound, user=user):
            url_array.append("http://www.genome.jp/dbget-bin/www_bget?cpd:" + str(kegg_compound_id))
        return url_array
    
    # Returns PDB URL.
    def pdb_url(compound, user=None):
        url_array = []
        for pdb_id in Compound.pdbechem_id(compound, user=user):
            url_array.append("https://www.ebi.ac.uk/pdbe/entry/search/index?compound_id:" + str(Compound.pdbechem_id(compound)))
        return url_array
    
    # Returns PubChem URL.
    def pubchem_url(compound, user=None):
        url_array = []
        for pubchem_cid in Compound.pubchem_cid(compound, user=user):
            url_array.append("https://pubchem.ncbi.nlm.nih.gov/compound/" + str(pubchem_cid))
        return url_array
    
    # Returns ChEBI-REACTOME URL.
    def reactome_chebi_url(compound, user=None):
        url_array = []
        for chebi_id in Compound.chebi_id(compound, user=user):
            url_array.append("http://www.reactome.org/content/query?cluster=true&q=" + str(chebi_id.rstrip(":")[1]))
        return url_array
    
    # Returns Wikipedia URL.
    def wikipedia_url(compound, user=None):
        url_array = []
        if Compound.wikipedia_page(compound, user = user) is not None and Compound.wikipedia_page(compound, user = user) != "":
            for wiki_page in Compound.wikipedia_page(compound, user = user):
                url_array.append(Compound.wikipedia_page(compound, user = user).url)
        return url_array
    
    """
        Auxiliary functions:
        
        Search
        
    """
    
    # Returns compounds by search.
    # http://chemspipy.readthedocs.io/en/latest/guide/searching.html
    #
    # Can use SMILES, common name, or ChemSpider identifier.
    # May return many results.
    #
    # Note that searching by mass has a default range of +/- 0.001.
    #
    # PubChem search is also included, but is not currently
    # fully documented.
    def search(query, user=None, search_type=None, source="chemspider", mass_plus_minus=0.001):
        return search(query, user=user, search_type=search_type, source=source, mass_plus_minus=mass_plus_minus)
    
    """
        External files:
        
        MOL file name
        MOL file with 2D coordinates
        MOL file with 3D coordinates
        Unprocessed MOL file
    """
    
    # Returns MOL file name.
    def mol_filename(compound, user=None):
        return Compound.chebi_entity(compound).get_mol_filename()
    
    # Returns MOL file with 2D coordinates.
    def mol_file_2d(compound, user=None, source="chemspider"):
        if source.lower() in ["chemspider", "all"] and user is not None:
            return Compound.chemspider_compound(compound).mol_2d
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
    # Returns MOL file with 3D coordinates.
    def mol_file_3d(compound, user=None):
        if source.lower() in ["chemspider", "all"] and user is not None:
            return Compound.chemspider_compound(compound).mol_3d
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
    # Returns unprocessed MOL file.
    def mol_file_raw(compound, user=None):
        if source.lower() in ["chemspider", "all"] and user is not None:
            return Compound.chemspider_compound(compound).mol_raw
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
#   UNIT TESTS
def compound_unit_tests(pubchem_cid, chemspider_id, chemspider_security_token=None):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    
    # Get all identifiers.
    print("Getting compound identifiers from PubChem CID (%s)..." % pubchem_cid)
    start = timeit.timeit()
    results_array = Compound.all_identifiers(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for iden in results_array:
        print("\t- %s: %s (%s)" % (iden["identifier_type"], iden["identifier"], iden["source"]))
    
    # Get all properties.
    print("\nGetting compound properties from PubChem CID (%s)..." % pubchem_cid)
    start = timeit.timeit()
    results_dict = Compound.all_properties(pubchem_com)
    end = timeit.timeit()
    print("\tTIME ELAPSED: %s seconds." % str(end - start))
    print("\tRESULTS:")
    for prop_type, prop in results_dict.items():
        print("\t- %s: %s" % (prop_type, prop))
    
    if chemspider_security_token is not None:
        print("\nCreating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
    
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")

        # Get all identifiers.
        print("Getting compound identifiers from ChemSpider ID (%s)..." % chemspider_id)
        start = timeit.timeit()
        results_array = Compound.all_identifiers(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for iden in results_array:
            print("\t- %s: %s (%s)" % (iden["identifier_type"], iden["identifier"], iden["source"]))
        
        # Get all properties.
        print("\nGetting compound properties from ChemSpider ID (%s)..." % chemspider_id)
        start = timeit.timeit()
        results_dict = Compound.all_properties(chemspider_com, user = user)
        end = timeit.timeit()
        print("\tTIME ELAPSED: %s seconds." % str(end - start))
        print("\tRESULTS:")
        for prop_type, prop in results_dict.items():
            print("\t- %s: %s" % (prop_type, prop))

#   MAIN
if __name__ == "__main__": main()