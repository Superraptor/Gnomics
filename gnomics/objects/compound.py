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
import wikipedia

#   Import sub-methods.
from gnomics.objects.compound_files.beilstein import get_beilstein
from gnomics.objects.compound_files.cas import get_cas
from gnomics.objects.compound_files.chebi import get_chebi_id, get_chebi_entity
from gnomics.objects.compound_files.chembl import get_chembl_id, get_chembl_molecule
from gnomics.objects.compound_files.common_names import get_common_names
from gnomics.objects.compound_files.cs import get_chemspider_id, get_chemspider_compound
from gnomics.objects.compound_files.inchi import get_inchi, get_inchi_key, get_standard_inchi, get_standard_inchi_key
from gnomics.objects.compound_files.iupac import get_iupac_name
from gnomics.objects.compound_files.kegg import get_kegg_compound_id, get_kegg_compound_db_entry
from gnomics.objects.compound_files.lincs import get_lincs_id
from gnomics.objects.compound_files.mesh import get_mesh_uid
from gnomics.objects.compound_files.molecular_formula import get_molecular_formula
from gnomics.objects.compound_files.pdbechem import get_pdbechem_id
from gnomics.objects.compound_files.pubchem import get_cids, get_sids, get_pubchem_compound
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

#   MAIN
def main():
    compound_unit_tests("6918092", "33510", "")

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
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': str(identifier),
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of compound objects.
        self.compound_objects = []
        
        # Initialize related objects.
        self.related_objects = []
        
    # Add an identifier to a compound.
    def add_identifier(compound, identifier = None, identifier_type = None, language = None, source = None, name = None):
        compound.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
        
    # Add an object to a compound.
    def add_object(compound, obj = None, object_type = None):
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
    def chebi_entity(compound, user = None):
        return get_chebi_entity(compound, user = user)
    
    # Returns ChEMBL molecule.
    def chembl_molecule(compound, user = None):
        return get_chembl_molecule(compound, user = user)
    
    # Returns ChemSpider compound.
    def chemspider_compound(compound, user = None):
        return get_chemspider_compound(compound, user = user)
        
    # Returns RxNorm object containing all properties.
    def rxnorm_object(compound):
        return get_rxnorm_obj(compound)
        
    # KEGG database entry (for compound).
    def kegg_compound_db_entry(compound):
        return get_kegg_compound_db_entry(compound)
    
    # Returns PubChem compound from CID.
    def pubchem_compound(compound, user = None):
        return get_pubchem_compound(compound, user = user)
    
    # Returns Wikidata object.
    def wikidata(compound):
        return get_wikidata_object(compound)
    
    """
        Compound identifiers:
        
        ATC codes
        BAN
        Beilstein registry number
        Canonical SMILES
        CAS registry number
        ChEBI identifier
        ChEMBL identifier
        ChemSpider identifier
        Common name
        DrugBank identifier
        FDA drug name
        InChI
        InChI key
        INN
        Isomeric SMILES
        IUPAC name
        JAN
        KEGG compound identifier
        KEGG drug identifier
        LINCS accession
        MeSH UID
        Molecular formula
        Patent accession
        PDBeChem accession
        PubChem CID
        PubChem SIDs
        SCHEMBL ID
        SMILES
        Standard InChI
        Standard InChI key
        Trade names
        USAN
        USP
        Wikipedia accession
    """
    
    # Return all identifiers.
    def all_identifiers(compound, user = None):
        Compound.beilstein(compound)
        Compound.canonical_smiles(compound)
        Compound.chebi_id(compound, user = user)
        Compound.chembl_id(compound, user = user)
        Compound.chemspider_id(compound, user = user)
        Compound.cas(compound, user = user)
        Compound.common_names(compound, user = user)
        Compound.inchi(compound, user = user)
        Compound.inchi_key(compound, user = user)
        Compound.isomeric_smiles(compound)
        Compound.iupac_name(compound)
        Compound.kegg_compound_id(compound)
        Compound.lincs_id(compound)
        Compound.mesh_uid(compound)
        Compound.molecular_formula(compound, user = user)
        Compound.pdbechem_id(compound)
        Compound.pubchem_cid(compound, user = user)
        Compound.pubchem_sids(compound, user = user)
        Compound.smiles(compound, user = user)
        Compound.standard_inchi(compound, user = user)
        Compound.standard_inchi_key(compound, user = user)
        Compound.wikipedia_accession(compound, user = user)
        return compound.identifiers
    
    # Returns Beilstein registry number.
    def beilstein(compound):
        return get_beilstein(compound)
    
    # Returns canonical SMILES.
    def canonical_smiles(compound):
        return get_canonical_smiles(compound)
        
    # Returns ChEBI identifier.
    def chebi_id(compound, user = None):
        return get_chebi_id(compound, user = user)
            
    # Returns ChEMBL identifier.
    def chembl_id(compound, user = None):
        return get_chembl_id(compound, user = user)
    
    # Returns ChemSpider identifier.
    def chemspider_id(compound, user = None):
        return get_chemspider_id(compound, user)
            
    # Returns CAS registry number.
    def cas(compound, user = None):
        return get_cas(compound, user = user)
            
    # Returns common names.
    def common_names(compound, user = None):
        return get_common_names(compound, user)
    
    # Returns InChI (IUPAC International Chemical Identifier).
    def inchi(compound, user = None):
        return get_inchi(compound, user = user)
            
    # Returns InChI key.
    def inchi_key(compound, user = None):
        return get_inchi_key(compound)
    
    # Returns isomeric SMILES.
    def isomeric_smiles(compound):
        return get_isomeric_smiles(compound)
    
    # Returns IUPAC name.
    def iupac_name(compound):
        return get_iupac_name(compound)
    
    # Returns KEGG Compound identifier.
    def kegg_compound_id(compound):
        return get_kegg_compound_id(compound)
    
    # Returns LINCS accession.
    def lincs_id(compound):
        return get_lincs_id(compound)
    
    # Returns MeSH UID.
    def mesh_uid(compound):
        return get_mesh_uid(compound)
    
    # Returns molecular formula.
    def molecular_formula(compound, user = None):
        return get_molecular_formula(compound)
    
    # Returns PDBeChem accession.
    def pdbechem_id(compound):
        return get_pdbechem_id(compound)
    
    # Returns PubChem CID (compound record).
    def pubchem_cid(compound, user = None):
        return get_cids(compound, user)
            
    # Returns PubChem SIDs (substance records).
    def pubchem_sids(compound, user = None):
        return get_sids(compound, user = None)
    
    # Returns SCHEMBL ID.
    def schembl_id(compound, user = None):
        return get_schembl_id(compound)
    
    # Returns SMILES.
    def smiles(compound, user = None):
        return get_smiles(compound, user)
            
    # Returns standard InChI (IUPAC International Chemical Identifier).
    def standard_inchi(compound, user = None):
        return get_standard_inchi(compound, user)
   
    # Returns standard InChI key.
    def standard_inchi_key(compound, user = None):
        return get_standard_inchi_key(compound, user)
            
    # Returns Wikipedia accession.
    def wikipedia_accession(compound, user = None, language = "en"):
        if language == "en":
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
    def all_interaction_objects(compound, user = None):
        interaction_obj = {}
        interaction_obj["Adverse Events"] = Compound.adverse_events(compound)
        interaction_obj["Assays"] = Compound.assays(compound)
        interaction_obj["Diseases"] = Compound.diseases(compound)
        interaction_obj["Drugs"] = Compound.drugs(compound)
        interaction_obj["Genes"] = Compound.genes(compound)
        interaction_obj["Patents"] = Compound.patents(compound)
        interaction_obj["Pathways"] = Compound.pathways(compound, user = user)
        # interaction_obj["References"] = Compound.references(compound)
        return interaction_obj
        
    # Returns adverse event objects.
    def adverse_events(compound, user = None):
        return get_adverse_events(compound, user = user)
        
    # Returns assay objects.
    def assays(compound):
        return get_assays(compound)
    
    # Return disease objects.
    def diseases(compound):
        return get_diseases(compound)
    
    # Return drug objects.
    def drugs(compound):
        return get_drugs(compound)
    
    # Get gene interactions.
    # http://dgidb.genome.wustl.edu/api
    #
    # Interaction sources can be TTD, DrugBank, etc.
    # But should be an array if possible.
    def genes(compound, source = None, interaction_sources = None, interaction_types = None, gene_categories = None, source_trust_levels = None):
        return get_genes(compound, source, interaction_sources, interaction_types, gene_categories, source_trust_levels)
    
    # Returns patent accession.
    def patents(compound):
        return get_patents(compound)
    
    # Get pathways related to compound (KEGG).
    #
    # For pathway associations, either
    # "inferred" or "enriched" may be used.
    def pathways(compound, source = None, pathway_assoc = None, user = None):
        return get_pathways(compound, source = source, pathway_assoc = pathway_assoc, user = user)
    
    # # Returns sources/references.
    # def references(compound):
    #    return get_references(compound)
    
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
    #
    # TODO: Serialize all commented out functions!
    def all_properties(compound, user = None):
        property_dict = {}
        property_dict["AlogP"] = Compound.alogp(compound, user = user)
        property_dict["Atom Stereo Count"] = Compound.atom_stereo_count(compound, user = user)
        # property_dict["Atoms"] = Compound.atoms(compound, user = user)
        property_dict["Average Mass"] = Compound.average_mass(compound, user = user)
        property_dict["Bond Stereo Count"] = Compound.bond_stereo_count(compound, user = user)
        # property_dict["Bonds"] = Compound.bonds(compound, user = user)
        property_dict["Charge"] = Compound.charge(compound, user = user)
        property_dict["2D depiction as binary data in PNG format"] = Compound.chem_2d_struct_binary_png_image(compound, user = user)
        property_dict["URL of 2D depiction as binary data in PNG format"] = Compound.chem_2d_struct_url_png_image(compound, user = user)
        # property_dict["Comments"] = Compound.comments(compound)
        property_dict["Complexity"] = Compound.complexity(compound, user = user)
        property_dict["3D Conformer ID"] = Compound.conformer_id_3d(compound, user = user)
        property_dict["3D RMSD Conformer"] = Compound.conformer_rmsd_3d(compound, user = user)
        property_dict["Coordinate Type"] = Compound.coordinate_type(compound, user = user)
        property_dict["Covalent Unit Count"] = Compound.covalent_unit_count(compound, user = user)
        property_dict["Creator"] = Compound.created_by(compound)
        property_dict["Defined Atom Stereo Count"] = Compound.defined_atom_stereo_count(compound, user = user)
        property_dict["Definition"] = Compound.definition(compound)
        property_dict["Effective Rotor Unit Count"] = Compound.effective_rotor_count(compound, user = user)
        property_dict["Exact Mass"] = Compound.exact_mass(compound, user = user)
        property_dict["Date First Approved"] = Compound.first_approval(compound)
        property_dict["3D Shape Selfoverlap"] = Compound.shape_selfoverlap_3d(compound, user = user)
        property_dict["Fingerprint"] = Compound.fingerprint(compound, user = user)
        property_dict["H Bond Acceptor Count"] = Compound.h_bond_acceptor_count(compound, user = user)
        property_dict["H Bond Donor Count"] = Compound.h_bond_donor_count(compound, user = user)
        property_dict["Indication Class"] = Compound.indication_class(compound)
        property_dict["Isotope Atom Count"] = Compound.isotope_atom_count(compound, user = user)
        property_dict["Mass"] = Compound.mass(compound)
        property_dict["3D mmff94 Energy"] = Compound.mmff94_energy_3d(compound, user = user)
        property_dict["3D mmff94 Partial Charges"] = Compound.mmff94_partial_charges_3d(compound, user = user)
        # property_dict["modified_on"] = Compound.modified_on(compound)
        # property_dict["MOL"] = Compound.mol(compound)
        property_dict["Molecular Weight"] = Compound.molecular_weight(compound, user = user)
        property_dict["Molecule Type"] = Compound.molecule_type(compound)
        property_dict["Monoisotopic Mass"] = Compound.monoisotopic_mass(compound, user = user)
        property_dict["3D Multipoles"] = Compound.multipoles_3d(compound, user = user)
        property_dict["Nominal Mass"] = Compound.nominal_mass(compound, user = user)
        property_dict["Oral"] = Compound.oral(compound)
        property_dict["Parenteral"] = Compound.parenteral(compound)
        property_dict["Prodrug"] = Compound.prodrug(compound)
        property_dict["3D Pharmacophore Features"] = Compound.pharmacophore_features_3d(compound, user = user)
        property_dict["Rotatable Bond Count"] = Compound.rotatable_bond_count(compound, user = user)
        property_dict["3D Shape Fingerprint"] = Compound.shape_fingerprint_3d(compound, user = user)
        property_dict["Spectra"] = Compound.spectra(compound, user = user)
        property_dict["Star"] = Compound.star(compound, user = user)
        property_dict["Topical"] = Compound.topical(compound, user = user)
        property_dict["Topology"] = Compound.topology(compound)
        property_dict["tPSA"] = Compound.tpsa(compound, user = user)
        property_dict["Undefined Atom Stereo Count"] = Compound.undefined_atom_stereo_count(compound, user = user)
        property_dict["3D Volume"] = Compound.volume_3d(compound, user = user)
        # property_dict["Wikipedia Content"] = Compound.wikipedia_content(compound, user = user)
        # property_dict["Wikipedia Links"] = Compound.wikipedia_links(compound, user = user)
        # property_dict["Wikipedia Page"] = Compound.wikipedia_page(compound, user = user)
        
        return property_dict
    
    # Returns AlogP.
    def alogp(compound, user = None, source = "chembl"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).alogp
        elif source == "chemspider" and user is None:
            print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            return Compound.chembl_molecule(compound)[0]["molecule_properties"]["alogp"]
        elif source == "chembl":
            return Compound.chembl_molecule(compound)[0]["molecule_properties"]["alogp"]
        else:
            print("Only ChemSpider and ChEMBL sources are currently supported for this function.")
            return ""
    
    # Returns atom stereo count.
    def atom_stereo_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).atom_stereo_count
    
    # Returns atoms.
    def atoms(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).atoms
    
    # Returns the average mass.
    def average_mass(compound, source = "chemspider", user = None):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).average_mass
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns bond stereo count.
    def bond_stereo_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).bond_stereo_count
    
    # Returns bonds.
    def bonds(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).bonds
    
    # Returns charge.
    def charge(compound, source = "pubchem", user = None):
        if source == "pubchem":
            return Compound.pubchem_compound(compound, user = user).charge
        elif source == "chebi":
            return Compound.chebi_entity(compound).get_charge()
        
    # Returns a 2D depiction as binary data in PNG format.
    def chem_2d_struct_binary_png_image(compound, user = None, source = "chemspider"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).image
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns URL of a PNG image of the 2D chemical structure.
    def chem_2d_struct_url_png_image(compound, user = None, source = "chemspider"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).image_url
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns comments.
    def comments(compound, source = "chebi"):
        if source == "chebi":
            return Compound.chebi_entity(compound).get_comments()
        else:
            print("Currently, only ChEBI comments are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns complexity.
    def complexity(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).complexity
    
    # Returns 3D conformer ID:
    def conformer_id_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).conformer_id_3d
    
    # Returns 3D RMSD conformer.
    def conformer_rmsd_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).conformer_rmsd_3d
    
    # Returns coordinate type.
    def coordinate_type(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).coordinate_type
    
    # Returns covalent unit count.
    def covalent_unit_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).covalent_unit_count
    
    # Returns who the record was created by or the method by which the record was created.
    def created_by(compound, source = "chebi"):
        if source == "chebi":
            return Compound.chebi_entity(compound).get_created_by()
        else:
            print("Currently, only ChEBI creation record types are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns defined atom stereo count.
    def defined_atom_stereo_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).defined_atom_stereo_count
    
    # Returns definition.
    def definition(compound, source = "chebi"):
        if source == "chebi":
            return Compound.chebi_entity(compound).get_definition()
        else:
            print("Currently, only ChEBI definitions are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns effective rotor count.
    def effective_rotor_count(compound, user = None):
        if hasattr(Compound.pubchem_compound(compound, user = user), "effective_rotor_count"):
            return Compound.pubchem_compound(compound, user = user).effective_rotor_count
        else:
            print("The attribute 'effective rotor count' does not exist in this record.")
            return ""
    
    # Returns exact mass.
    def exact_mass(compound, source = "pubchem", user = None):
        if source == "pubchem":
            return Compound.pubchem_compound(compound, user = user).exact_mass
        elif source == "kegg":
            return Compound.kegg_compound_db_entry(compound)["EXACT_MASS"]
        else:
            print("Only PubChem and KEGG sources are currently supported for this function.")
            return ""
    
    # Returns year first approved.
    def first_approval(compound):
        return Compound.chembl_molecule(compound)[0]["first_approval"]
    
    # Returns 3D feature selfoverlap.
    def shape_selfoverlap_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).shape_selfoverlap_3d
    
    # Returns fingerprint.
    def fingerprint(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).fingerprint
    
    # Returns H bond acceptor count.
    def h_bond_acceptor_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).h_bond_acceptor_count
    
    # Returns H bond donor count.
    def h_bond_donor_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).h_bond_donor_count
    
    # Returns heavy atom count.
    def heavy_atom_count(compound, source = "pubchem", user = None):
        if source == "pubchem":
            return Compound.pubchem_compound(compound, user = user).heavy_atom_count
        elif source == "pybel":
            print("PyBel sources are experimental and not currently functional. Only PubChem sources are currently supported for this function.")
            return constitution.CalculateHeavyAtomNumber(Compound.pybel_mol(compound))
        else:
            print("Only PubChem sources are currently supported for this function.")
            return ""
    
    # Returns indication class.
    def indication_class(compound):
        return Compound.chembl_molecule(compound)[0]["indication_class"]
    
    # Returns isotope atom count.
    def isotope_atom_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).isotope_atom_count
    
    # Returns mass.
    def mass(compound):
        return Compound.chebi_entity(compound).get_mass()
    
    # Returns 3D mmff94 energy.
    def mmff94_energy_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).mmff94_energy_3d
    
    # Returns 3D mmff94 partial charges.
    def mmff94_partial_charges_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).mmff94_partial_charges_3d
    
    # Returns date modified as datetime object (for ChEBI).
    def modified_on(compound, source = "chebi"):
        if source == "chebi":
            return Compound.chebi_entity(compound).get_modified_on()
        else:
            print("Currently, only ChEBI modification dates are supported. Please specify 'chebi' as source.")
            return ""
    
    # Returns MOL.
    def mol(compound):
        return Compound.chebi_entity(compound).get_mol()
        
    # Returns the molecular weight.
    def molecular_weight(compound, user = None, source = "pubchem"):
        if source == "chemspider":
            return Compound.chemspider_compound(compound, user = user).molecular_weight
        elif source == "pubchem":
            return Compound.pubchem_compound(compound, user = user).molecular_weight
        elif source == "kegg":
            return Compound.kegg_compound_db_entry(compound)["MOL_WEIGHT"]
        elif source == "pybel":
            print("PyBel sources are experimental and not currently functional. Only PubChem sources, ChemSpider sources, and KEGG sources are currently supported for this function.")
            return constitution.CalculateMolWeight(Compound.pybel_mol(compound))
        else:
            print("Only PubChem sources, ChemSpider sources, and KEGG sources are currently supported for this function.")
            return ""
        
    # Returns molecule type.
    def molecule_type(compound):
        return Compound.chembl_molecule(compound)[0]["molecule_type"]
        
    # Returns the monoisotopic mass.
    def monoisotopic_mass(compound, user = None, source = "chembl"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).monoisotopic_mass
        elif source == "chemspider" and user is None:
            print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            return Compound.chembl_molecule(compound)[0]["molecule_properties"]["mw_monoisotopic"]
        elif source == "pubchem":
            return Compound.pubchem_compound(compound, user = user).monoisotopic_mass
        elif source == "chembl":
            return Compound.chembl_molecule(compound)[0]["molecule_properties"]["mw_monoisotopic"]
        
    # Returns 3D multipoles.
    def multipoles_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).multipoles_3d
    
    # Returns the nominal mass.
    def nominal_mass(compound, user = None, source = "chemspider"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).nominal_mass
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns whether oral (True) or not (False).
    def oral(compound):
        return Compound.chembl_molecule(compound)[0]["oral"]
    
    # Returns whether parenteral (True) or not (False).
    def parenteral(compound):
        return Compound.chembl_molecule(compound)[0]["parenteral"]
    
    # Returns whether prodrug (True) or not (False).
    # According to IUPAC, a prodrug is a "[c]ompound
    # that undergoes biotransformation before
    # exhibiting pharmacological effects."
    def prodrug(compound):
        if Compound.chembl_molecule(compound)[0]["prodrug"] == True:
            return True
        elif Compound.chembl_molecule(compound)[0]["prodrug"] == False:
            return False
    
    # Returns 3D pharmacophore features.
    def pharmacophore_features_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).pharmacophore_features_3d
    
    # Returns rotatable bond count.
    def rotatable_bond_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).rotatable_bond_count
    
    # Returns 3D shape fingerprint.
    def shape_fingerprint_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).shape_fingerprint_3d
    
    # Returns spectra.
    def spectra(compound, user = None, source = "chemspider"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).spectra
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns star.
    def star(compound, user = None):
        return Compound.chebi_entity(compound, user = user).get_star()
    
    # Returns whether topical (True) or not (False).
    def topical(compound, user = None):
        return Compound.chembl_molecule(compound, user = user)[0]["topical"]
    
    # Returns topology.
    def topology(compound):
        print("PyBel sources are experimental and not currently functional. As such, neither is this function.")
        return ""
        # return topology.GetTopology(compound.pybel_mol)
    
    # Returns tPSA (topological polar surface area).
    def tpsa(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).tpsa
    
    # Returns undefined atom stereo count.
    def undefined_atom_stereo_count(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).undefined_atom_stereo_count
    
    # Returns 3D volume.
    def volume_3d(compound, user = None):
        return Compound.pubchem_compound(compound, user = user).volume_3d
        
    # Returns Wikipedia content.
    def wikipedia_content(compound, user = None):
        if Compound.wikipedia_page(compound, user = user) is not None and Compound.wikipedia_page(compound, user = user) != "":
            return Compound.wikipedia_page(compound, user = user).content
    
    # Returns Wikipedia links.
    def wikipedia_links(compound, user = None):
        if Compound.wikipedia_page(compound, user = user) is not None and Compound.wikipedia_page(compound, user = user) != "":
            return Compound.wikipedia_page(compound, user = user).links
        
    # Returns Wikipedia page.
    def wikipedia_page(compound, user = None):
        if Compound.wikipedia_accession(compound, user = user) is not None and Compound.wikipedia_accession(compound, user = user) != "":
            return wikipedia.page(Compound.wikipedia_accession(compound, user = user))
    
    # Returns Wikipedia page title.
    def wikipedia_url(compound, user = None):
        if Compound.wikipedia_page(compound, user = user) is not None and Compound.wikipedia_page(compound, user = user) != "":
            return Compound.wikipedia_page(compound, user = user).title
        
    # Returns XlogP.
    def xlogp(compound, user = None, source = "pubchem"):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound, user = user).xlogp
        elif source == "chemspider" and user is None:
            print("No valid ChemSpider API security token provided, continuing with ChEMBL...")
            return Compound.pubchem_compound(compound).xlogp
        elif source == "pubchem":
            return Compound.pubchem_compound(compound).xlogp
        else:
            print("Only ChemSpider and PubChem sources are currently supported for this function.")
            return ""
        
    """
        URLs:
        
        ChEBI URL
        ChEMBL URL
        ChemSpider URL
        DrugBank URL
        KEGG Compound URL
        KEGG Drug URL
        PDB URL
        PubChem URL
        ChEBI-REACTOME URL
        Wikipedia URL
        
    """
    
    # Return links.
    def links(compound):
        link_dict = {}
    
    # Returns ChEBI URL.
    def chebi_url(compound):
        return "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=" + str(Compound.chebi_id(compound))
    
    # Returns ChEMBL URL.
    def chembl_url(compound):
        return "https://www.ebi.ac.uk/chembldb/index.php/compound/inspect/" + str(Compound.chembl_id(compound))
    
    # Returns ChemSpider URL.
    def chemspider_url(compound, user = None):
        if source == "chemspider" and user is not None:
            return "http://www.chemspider.com/Chemical-Structure." + str(Compound.chemspider_id(compound)) + ".html"
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
    
    # Returns DrugBank URL.
    def drugbank_url(compound):
        return "https://www.drugbank.ca/drugs/" + str(Compound.drugbank_id(compound))
    
    # Returns KEGG Compound URL.
    def kegg_compound_url(compound):
        return "http://www.genome.jp/dbget-bin/www_bget?cpd:" + str(Compound.kegg_compound_id(compound))
    
    # Returns KEGG Drug URL.
    def kegg_drug_url(compound):
        return "http://www.genome.jp/dbget-bin/www_bget?dr:" + str(Compound.kegg_drug_id(compound))
    
    # Returns PDB URL.
    def pdb_url(compound):
        return "https://www.ebi.ac.uk/pdbe/entry/search/index?compound_id:" + str(Compound.pdbechem_id(compound))
    
    # Returns PubChem URL.
    def pubchem_url(compound):
        return "https://pubchem.ncbi.nlm.nih.gov/compound/" + str(Compound.pubchem_cid(compound))
    
    # Returns ChEBI-REACTOME URL.
    def reactome_chebi_url(compound):
        return "http://www.reactome.org/content/query?cluster=true&q=" + str(Compound.chebi_id(compound).rstrip(":")[1])
    
    # Returns Wikipedia URL.
    def wikipedia_url(compound, user = None):
        if Compound.wikipedia_page(compound, user = user) is not None and Compound.wikipedia_page(compound, user = user) != "":
            return Compound.wikipedia_page(compound, user = user).url
    
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
    def search(query, user = None, search_type = None, source = "chemspider", mass_plus_minus = 0.001):
        return search(query, user = user, search_type = search_type, source = source, mass_plus_minus = mass_plus_minus)
    
    """
        External files:
        
        MOL file name
        MOL file with 2D coordinates
        MOL file with 3D coordinates
        Unprocessed MOL file
    """
    
    # Returns MOL file name.
    def mol_filename(compound):
        return Compound.chebi_entity(compound).get_mol_filename()
    
    # Returns MOL file with 2D coordinates.
    def mol_file_2d(compound, user = None):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound).mol_2d
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
    # Returns MOL file with 3D coordinates.
    def mol_file_3d(compound, user = None):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound).mol_3d
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
    # Returns unprocessed MOL file.
    def mol_file_raw(compound, user = None):
        if source == "chemspider" and user is not None:
            return Compound.chemspider_compound(compound).mol_raw
        else:
            print("No valid ChemSpider API security token provided. Cannot return value.")
            return ""
        
#   UNIT TESTS
def compound_unit_tests(pubchem_cid, chemspider_id, chemspider_security_token = None):
    pubchem_com = gnomics.objects.compound.Compound(identifier = str(pubchem_cid), identifier_type = "PubChem CID", source = "PubChem")
    print("Getting compound properties from PubChem CID (%s)..." % pubchem_cid)
    
    print("AlogP: %s" % Compound.alogp(pubchem_com))
    print("Atom Stereo Count: %s" % Compound.atom_stereo_count(pubchem_com))
    print("Average Mass: %s" % Compound.average_mass(pubchem_com))
    print("Bond Stereo Count: %s" % Compound.bond_stereo_count(pubchem_com))
    print("Bonds: %s" % Compound.bonds(pubchem_com))
    print("Charge: %s" % Compound.charge(pubchem_com))
    print("2D Chemical Structure PNG Image URL: %s" % Compound.chem_2d_struct_url_png_image(pubchem_com))
    print("Comments: %s" % Compound.comments(pubchem_com))
    print("Complexity: %s" % Compound.complexity(pubchem_com))
    print("3D Conformer ID: %s" % Compound.conformer_id_3d(pubchem_com))
    print("3D RMSD Conformer: %s" % Compound.conformer_rmsd_3d(pubchem_com))
    print("Coordinate Type: %s" % Compound.coordinate_type(pubchem_com))
    print("Covalent Unit Count: %s" % Compound.covalent_unit_count(pubchem_com))
    print("Created By: %s" % Compound.created_by(pubchem_com))
    print("Defined Atom Stereo Count: %s" % Compound.defined_atom_stereo_count(pubchem_com))
    print("Definition: %s" % Compound.definition(pubchem_com))
    print("Effective Rotor Count: %s" % Compound.effective_rotor_count(pubchem_com))
    print("Exact Mass: %s" % Compound.exact_mass(pubchem_com))
    print("First Approval: %s" % Compound.first_approval(pubchem_com))
    print("3D Feature Selfoverlap: %s" % Compound.shape_selfoverlap_3d(pubchem_com))
    print("Fingerprint: %s" % Compound.fingerprint(pubchem_com))
    print("H Bond Acceptor Count: %s" % Compound.h_bond_acceptor_count(pubchem_com))
    print("H Bond Donor Count: %s" % Compound.h_bond_donor_count(pubchem_com))
    print("Heavy Atom Count: %s" % Compound.heavy_atom_count(pubchem_com))
    print("Indication Class: %s" % Compound.indication_class(pubchem_com))
    print("Isotope Atom Count: %s" % Compound.isotope_atom_count(pubchem_com))
    print("Mass: %s" % Compound.mass(pubchem_com))
    print("3D mmff94 Energy: %s" % Compound.mmff94_energy_3d(pubchem_com))
    print("Modified on: %s" % Compound.modified_on(pubchem_com))
    print("MOL: %s" % Compound.mol(pubchem_com))
    print("Molecular Weight: %s" % Compound.molecular_weight(pubchem_com))
    print("Molecule Type: %s" % Compound.molecule_type(pubchem_com))
    print("Monoisotopic Mass: %s" % Compound.monoisotopic_mass(pubchem_com))
    print("3D Multipoles: %s" % Compound.multipoles_3d(pubchem_com))
    print("Nominal Mass: %s" % Compound.nominal_mass(pubchem_com))
    print("Oral: %s" % Compound.oral(pubchem_com))
    print("Parenteral: %s" % Compound.parenteral(pubchem_com))
    print("Prodrug: %s" % Compound.prodrug(pubchem_com))
    print("3D Pharmacophore Features: %s" % Compound.pharmacophore_features_3d(pubchem_com))
    print("Rotatable Bond Count: %s" % Compound.rotatable_bond_count(pubchem_com))
    print("3D Shape Fingerprint: %s" % Compound.shape_fingerprint_3d(pubchem_com))
    print("Spectra: %s" % Compound.spectra(pubchem_com))
    print("Star: %s" % Compound.star(pubchem_com))
    print("Topical: %s" % Compound.topical(pubchem_com))
    print("tPSA: %s" % Compound.tpsa(pubchem_com))
    print("Undefined Atom Stereo Count: %s" % Compound.undefined_atom_stereo_count(pubchem_com))
    print("3D Volume: %s" % Compound.volume_3d(pubchem_com))
    print("Wikipedia Content: %s" % Compound.wikipedia_content(pubchem_com))
    print("Wikipedia Links: %s" % Compound.wikipedia_links(pubchem_com))
    print("Wikipedia Page: %s" % Compound.wikipedia_page(pubchem_com))
    print("Wikipedia URL: %s" % Compound.wikipedia_url(pubchem_com))
    print("XlogP: %s" % Compound.xlogp(pubchem_com))
    
    if chemspider_security_token is not None:
        print("Creating user...")
        user = User(chemspider_security_token = chemspider_security_token)
        print("User created successfully.\n")
    
        chemspider_com = gnomics.objects.compound.Compound(identifier = str(chemspider_id), identifier_type = "ChemSpider ID", source = "ChemSpider")
        print("Getting compound properties from ChemSpider ID (%s)..." % chemspider_id)

        print("AlogP: %s" % Compound.alogp(chemspider_com, user = user, source = "chemspider"))
        print("Atom Stereo Count: %s" % Compound.atom_stereo_count(chemspider_com, user = user))
        print("Average Mass: %s" % Compound.average_mass(chemspider_com, user = user, source = "chemspider"))
        print("Bond Stereo Count: %s" % Compound.bond_stereo_count(chemspider_com, user = user))
        print("Bonds: %s" % Compound.bonds(chemspider_com, user = user))
        print("Charge: %s" % Compound.charge(chemspider_com, user = user))
        print("2D Chemical Structure PNG Image URL: %s" % Compound.chem_2d_struct_url_png_image(chemspider_com, user = user, source = "chemspider"))
        print("Comments: %s" % Compound.comments(chemspider_com))
        print("Complexity: %s" % Compound.complexity(chemspider_com, user = user))
        print("3D Conformer ID: %s" % Compound.conformer_id_3d(chemspider_com, user = user))
        print("3D RMSD Conformer: %s" % Compound.conformer_rmsd_3d(chemspider_com, user = user))
        print("Coordinate Type: %s" % Compound.coordinate_type(chemspider_com, user = user))
        print("Covalent Unit Count: %s" % Compound.covalent_unit_count(chemspider_com, user = user))
        print("Created By: %s" % Compound.created_by(chemspider_com))
        print("Defined Atom Stereo Count: %s" % Compound.defined_atom_stereo_count(chemspider_com, user = user))
        print("Definition: %s" % Compound.definition(chemspider_com))
        print("Effective Rotor Count: %s" % Compound.effective_rotor_count(chemspider_com, user = user))
        print("Exact Mass: %s" % Compound.exact_mass(chemspider_com, user = user))
        print("First Approval: %s" % Compound.first_approval(chemspider_com))
        print("3D Feature Selfoverlap: %s" % Compound.shape_selfoverlap_3d(chemspider_com, user = user))
        print("Fingerprint: %s" % Compound.fingerprint(chemspider_com, user = user))
        print("H Bond Acceptor Count: %s" % Compound.h_bond_acceptor_count(chemspider_com, user = user))
        print("H Bond Donor Count: %s" % Compound.h_bond_donor_count(chemspider_com, user = user))
        print("Heavy Atom Count: %s" % Compound.heavy_atom_count(chemspider_com, user = user))
        print("Indication Class: %s" % Compound.indication_class(chemspider_com))
        print("Isotope Atom Count: %s" % Compound.isotope_atom_count(chemspider_com, user = user))
        print("Mass: %s" % Compound.mass(chemspider_com))
        print("3D mmff94 Energy: %s" % Compound.mmff94_energy_3d(chemspider_com, user = user))
        print("Modified on: %s" % Compound.modified_on(chemspider_com))
        print("MOL: %s" % Compound.mol(chemspider_com))
        print("Molecular Weight: %s" % Compound.molecular_weight(chemspider_com, user = user, source = "chemspider"))
        print("Molecule Type: %s" % Compound.molecule_type(chemspider_com))
        print("Monoisotopic Mass: %s" % Compound.monoisotopic_mass(chemspider_com, user = user, source = "chemspider"))
        print("3D Multipoles: %s" % Compound.multipoles_3d(chemspider_com, user = user))
        print("Nominal Mass: %s" % Compound.nominal_mass(chemspider_com, user = user, source = "chemspider"))
        print("Oral: %s" % Compound.oral(chemspider_com))
        print("Parenteral: %s" % Compound.parenteral(chemspider_com))
        print("Prodrug: %s" % Compound.prodrug(chemspider_com))
        print("3D Pharmacophore Features: %s" % Compound.pharmacophore_features_3d(chemspider_com, user = user))
        print("Rotatable Bond Count: %s" % Compound.rotatable_bond_count(chemspider_com, user = user))
        print("3D Shape Fingerprint: %s" % Compound.shape_fingerprint_3d(chemspider_com, user = user))
        print("Spectra: %s" % Compound.spectra(chemspider_com, user = user, source = "chemspider"))
        print("Star: %s" % Compound.star(chemspider_com, user = user))
        print("Topical: %s" % Compound.topical(chemspider_com, user = user))
        print("tPSA: %s" % Compound.tpsa(chemspider_com, user = user))
        print("Undefined Atom Stereo Count: %s" % Compound.undefined_atom_stereo_count(chemspider_com, user = user))
        print("3D Volume: %s" % Compound.volume_3d(chemspider_com, user = user))
        print("Wikipedia Content: %s" % Compound.wikipedia_content(chemspider_com, user = user))
        print("Wikipedia Links: %s" % Compound.wikipedia_links(chemspider_com, user = user))
        print("Wikipedia Page: %s" % Compound.wikipedia_page(chemspider_com, user = user))
        print("Wikipedia URL: %s" % Compound.wikipedia_url(chemspider_com, user = user))
        print("XlogP: %s" % Compound.xlogp(chemspider_com, user = user))

#   MAIN
if __name__ == "__main__": main()