#
#
#
#
#

#
#   IMPORT SOURCES:
#       EOL_PYTHON
#           https://github.com/linbug/eol_python
#       PYTAXIZE
#           http://pytaxize.readthedocs.io/en/latest/
#

#
#   Create instance of a taxon.
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
import gnomics.objects.compound
import gnomics.objects.disease
import gnomics.objects.gene
import gnomics.objects.phenotype

#   Import sub-methods.
from gnomics.objects.taxon_files.col import get_col_id
from gnomics.objects.taxon_files.eol import get_eol_object, get_eol_id, get_eol_traitbank_object
from gnomics.objects.taxon_files.ncbi import get_ncbi_taxonomy_id
from gnomics.objects.taxon_files.search import search
from gnomics.objects.taxon_files.wiki import get_wikidata_object

#   Import further methods.
from gnomics.objects.interaction_objects.taxon_reference import get_references

#   Other imports.
import pytaxize

#   MAIN
def main():
    taxon_unit_tests("Homo sapiens")
    
#   SOURCE CLASS
class Taxon(object):
    """
        Taxon class:
        
        This class usually refers to what is called a "biological species," or more specifically a "Biological Species Concept" (BSC), which the Encyclopedia of Life (EOL) defined as a group
        "of actually or potentially interbreeding natural
        populations which are reproductively isolated from other
        such groups." 
        
        However, in practice, this class contains any taxonomical
        entity, as long as that entity is biological in nature
        (i.e. viruses, etc.).
        
        Note that this class does not cover chemical species.
        
    """
    
    """
        Taxon attributes:
        
        Identifier      = A particular way to identify the
                          species/taxon in question. Usually a
                          database unique identifier, but
                          could also be natural language.
        Identifier Type = Typically, the database or origin or
                          type of identifier being provided.
        Language        = The natural language of the identifier,
                          if applicable.
        Source          = Where the identifier came from,
                          essentially, a short citation.
    """
    
    # Initialize the taxon.
    def __init__(self, identifier = None, identifier_type = None, language = None, source = None, name = None):
        
        # Initialize dictionary of identifiers.
        self.identifiers = [
            {
                'identifier': identifier,
                'language': language,
                'identifier_type': identifier_type,
                'source': source,
                'name': name
            }
        ]
        
        # Initialize dictionary of phenotype objects.
        self.taxon_objects = []
        
    # Add an identifier to a phenotype.
    def add_identifier(taxon, identifier = None, identifier_type = None, language = None, source = None, name = None):
        taxon.identifiers.append({
            'identifier': str(identifier),
            'language': language,
            'identifier_type': identifier_type,
            'source': source,
            'name': name
        })
    
    """
        Taxon objects:
        
        EOL Page
        EOL Traitbank
        Wikidata Object
        
    """
    
    # Get EOL page.
    def eol_page(taxon, batch = False, images_per_page = 1, images_page = 1, videos_per_page = 1, videos_page = 1, sounds_per_page = 1, sounds_page = 1, maps_per_page = 1, maps_page = 1, texts_per_page = 2, texts_page = 1, subjects = "overview", licenses = "all", details = True, common_names = True, synonyms = True, references = True, taxonomy = True, vetted = 0, cache_ttl = None, language = "en", result_format = "JSON"):
        return get_eol_object(taxon, batch = batch, images_per_page = images_per_page, videos_per_page = videos_per_page, videos_page = videos_page, sounds_per_page = sounds_per_page, sounds_page = sounds_page, maps_per_page = maps_per_page, maps_page = maps_page, texts_per_page = texts_per_page, texts_page = texts_page, subjects = subjects, licenses = licenses, details = details, common_names = common_names, synonyms = synonyms, references = references, taxonomy = taxonomy, vetted = vetted, cache_ttl = cache_ttl, language = language, result_format = "JSON")
    
    # Get EOL Traitbank.
    def eol_traitbank(taxon):
        return get_eol_traitbank_object(taxon)
    
    # Returns Wikidata object.
    def wikidata(taxon):
        return get_wikidata_object(taxon)
    
    """
        Taxon identifiers:
        
        COL (Catalogue of Life) identifier
        EOL (Encyclopedia of Life) identifier
        ITIS TSN (Taxonomic Serial Number)
        KEGG species identifier
        NCBI Taxonomy identifier
        Paleobiology Database identifier
        Scientific name
        
    """
    
    # Return all identifiers.
    def all_identifiers(taxon, user = None):
        return taxon.identifiers
    
    # Get COL (Cataologue of Life) identifier.
    def col_id(taxon):
        
        print("NOT FUNCTIONAL.")
    
    # Get EOL (Encyclopedia of Life) identifier.
    def eol_id(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get ITIS Taxonomic Serial number.
    def itis_tsn(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get KEGG species identifier.
    def kegg_species_id(taxon):
        print("NOT FUNCTIONAL.")
        for ident in taxon.identifiers:
            if ident["identifier_type"].lower() == "kegg":
                return ident["identifier"]
            elif ident["identifier_type"].lower() == "scientific name" or ident["identifier_type"].lower() == "binomial name" or ident["identifier_type"].lower() == "binomial nomenclature" or ident["identifier_type"].lower() == "binomen" or ident["identifier_type"].lower() == "latin name":
                return kegg_species_dict().keys()[kegg_species_dict().values().index(ident["identifier"])]
    
    # Get NCBI Taxonomy identifier.
    def ncbi_taxonomy_id(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get Paleobiology Database identifier.
    def paleobiology_db_id(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get scientific name.
    def scientific_name(taxon):
        print("NOT FUNCTIONAL.")
        for ident in taxon.identifiers:
            if ident["identifier_type"].lower() == "scientific name" or ident["identifier_type"].lower() == "binomial name" or ident["identifier_type"].lower() == "binomial nomenclature" or ident["identifier_type"].lower() == "binomen" or ident["identifier_type"].lower() == "latin name":
                return ident["identifier"]
            elif ident["identifier_type"].lower() == "kegg":
                print("NOT FUNCTIONAL.")
                sys.exit()
                
    """
        Other properties:
        
        Actual evapotranspiration rate in geographic range
        Age at eye opening
        Age at first reproduction
        Animal population density
        Associations (?)
        Barcode
        Behavior/Behaviour
        Behavioral circadian rhythm
        Biology
        Body length
        Body mass
        Body temperature
        Brood size
        Citizen Science
        Clutch size
        Conservation
        Conservation status
        Cyclicity
        Cytology
        Description
        Development
        Diagnostic description
        Diet
        Diet breadth
        Diseases
        Dispersal
        Dispersal age
        Distribution
        Ecology
        Education
        Education resources
        Elevation
        Evolution
        Extinction status
        First appearance (upper/lower bounds)
        Fossil history
        Functional adaptations
        General description
        Genetics
        Genome
        Geographic distribution
        Geographic range
        Gestation period duration
        Growth
        Growth rate
        Habitat
        Habitat breadth
        Home range
        Human population density
        Human population density change
        Identification resources
        Inter-birth interval
        Keys
        Last appearance (upper/lower bounds)
        Latitude
        Legislation
        Life cycle
        Life expectancy
        Litter size
        Litters per year
        Look-alikes
        Management
        Mating system
        Metabolic rate
        Migration
        Molecular biology
        Morphology
        Notes
        Nucleotide sequences
        Onset of fertility
        Parental care
        Phylogenetics
        Physiology
        Population biology
        Population trend
        Potential evapotranspiration rate in geographic range
        Precipitation in geographic range
        Prenatal development duration
        Procedures
        Reproduction
        Risk statement
        Social group size
        Social system
        Systematics
        Taxon biology
        Taxonomic classification
        Taxonomy
        Teat number
        Temperature in geographic range
        Terrestriality
        Threats
        Total life span
        Trends
        Trophic level
        Trophic strategy
        Type information
        Uses
        Weaning age
        Weight
        
    """
    
    # Return all properties in this category.
    #
    # TODO: Serialize all commented out functions!
    def all_properties(taxon, user = None):
        property_dict = {}
        #property_dict["Actual Evapotranspiration Rate in Geographic Range"] = Taxon.actual_evapotranspiration_rate_in_geographic_range(taxon)
        property_dict["Age at Eye Opening"] = Taxon.age_at_eye_opening(taxon)
        property_dict["Age at First Reproduction"] = Taxon.age_at_first_reproduction(taxon)
        #property_dict["Animal Population Density"] = Taxon.animal_population_density(taxon)
        #property_dict["Associations"] = Taxon.associations(taxon)
        #property_dict["Barcode"] = Taxon.barcode(taxon)
        property_dict["Basal Metabolic Rate"] = Taxon.basal_metabolic_rate(taxon)
        property_dict["Behavior"] = Taxon.behavior(taxon)
        #property_dict["Behavioral Circadian Rhythm"] = Taxon.behavioral_circadian_rhythm(taxon)
        property_dict["Biology"] = Taxon.biology(taxon)
        property_dict["Body Length"] = Taxon.body_length(taxon)
        property_dict["Body Mass"] = Taxon.body_mass(taxon)
        property_dict["Brood Size"] = Taxon.brood_size(taxon)
        property_dict["Clutch Size"] = Taxon.clutch_size(taxon)
        property_dict["Conservation"] = Taxon.conservation(taxon)
        property_dict["Conservation Status"] = Taxon.conservation_status(taxon)
        property_dict["Description"] = Taxon.description(taxon)
        property_dict["Diet"] = Taxon.diet(taxon)
        property_dict["Diet Breadth"] = Taxon.diet_breadth(taxon)
        property_dict["Dispersal Age"] = Taxon.dispersal_age(taxon)
        property_dict["Distribution"] = Taxon.distribution(taxon)
        property_dict["Ecology"] = Taxon.ecology(taxon)
        property_dict["Elevation"] = Taxon.elevation(taxon)
        property_dict["Evolution"] = Taxon.evolution(taxon)
        property_dict["Extinction Status"] = Taxon.extinction_status(taxon)
        property_dict["Fossil History"] = Taxon.fossil_history(taxon)
        property_dict["Functional Adaptations"] = Taxon.functional_adaptations(taxon)
        property_dict["General Description"] = Taxon.general_description(taxon)
        property_dict["Geographic Distribution"] = Taxon.geographic_distribution(taxon)
        property_dict["Geographic Range"] = Taxon.geographic_range(taxon)
        property_dict["Gestation Period Duration"] = Taxon.gestation_period_duration(taxon)
        property_dict["Habitat"] = Taxon.habitat(taxon)
        property_dict["Habitat Breadth"] = Taxon.habitat_breadth(taxon)
        property_dict["Home Range"] = Taxon.home_range(taxon)
        property_dict["Inter-birth Interval"] = Taxon.interbirth_interval(taxon)
        property_dict["Latitude"] = Taxon.latitude(taxon)
        property_dict["Life Expectancy"] = Taxon.life_expectancy(taxon)
        property_dict["Litter Size"] = Taxon.litter_size(taxon)
        property_dict["Litters Per Year"] = Taxon.litters_per_year(taxon)
        property_dict["Longitude"] = Taxon.longitude(taxon)
        property_dict["Metabolic Rate"] = Taxon.metabolic_rate(taxon)
        property_dict["Management"] = Taxon.management(taxon)
        property_dict["Mating System"] = Taxon.mating_system(taxon)
        property_dict["Molecular Biology"] = Taxon.molecular_biology(taxon)
        property_dict["Morphology"] = Taxon.morphology(taxon)
        property_dict["Onset of Fertility"] = Taxon.onset_of_fertility(taxon)
        property_dict["Parental Care"] = Taxon.parental_care(taxon)
        property_dict["Population Biology"] = Taxon.population_biology(taxon)
        property_dict["Population Trend"] = Taxon.population_trend(taxon)
        property_dict["Reproduction"] = Taxon.reproduction(taxon)
        property_dict["Social System"] = Taxon.social_system(taxon)
        property_dict["Taxon Biology"] = Taxon.taxon_biology(taxon)
        property_dict["Threats"] = Taxon.threats(taxon)
        property_dict["Total Life Span"] = Taxon.total_life_span(taxon)
        property_dict["Trends"] = Taxon.trends(taxon)
        property_dict["Trophic Strategy"] = Taxon.trophic_strategy(taxon)
        property_dict["Type Information"] = Taxon.type_information(taxon)
        property_dict["Uses"] = Taxon.uses(taxon)
        property_dict["Weaning Age"] = Taxon.weaning_age(taxon)
        property_dict["Weight"] = Taxon.weight(taxon)
        #print(property_dict)
        
        proc_prop_dict = {}
        for prop, prop_list in property_dict.items():
            if type(prop_list) is list:
                count = 1
                if prop_list:
                    for sub_prop in prop_list:
                        if "units" in sub_prop and "value" in sub_prop:
                            proc_prop_dict[prop + " (" + str(count) + ")"] = str(sub_prop["value"]) + " " + str(sub_prop["units"])
                            count += 1
                        elif "value" in sub_prop:
                            proc_prop_dict[prop + " (" + str(count) + ")"] = str(sub_prop["value"])
                            count += 1
            else:
                proc_prop_dict[prop] = prop_list
        
        #print(proc_prop_dict)
        return proc_prop_dict
    
    # Get actual evapotranspiration rate in geographic range.
    def actual_evapotranspiration_rate_in_geographic_range(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get age at eye opening.
    def age_at_eye_opening(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "age at eye opening":
                trait_array.append(trait)
        return trait_array
    
    # Get age at first reproduction.
    def age_at_first_reproduction(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "age at first reproduction":
                trait_array.append(trait)
        return trait_array
    
    # Get animal population density.
    def animal_population_density(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get associations.
    def associations():
        assoc_array = []
        for data_subtype in Taxon.eol_page(taxon, subjects = "Associations")["dataObjects"]:
            if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Associations" and data_subtype["dataSubtype"] == "":
                assoc_array.append(data_subtype["description"])
                
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "feeds on":
                trait_array.append(trait)
            elif trait["predicate"] == "interacts with":
                trait_array.append(trait)
            elif trait["predicate"] == "has host":
                trait_array.append(trait)
            elif trait["predicate"] == "pollinates":
                trait_array.append(trait)
                
        return assoc_array
    
    # Get barcode.
    def barcode(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get basal metabolic rate.
    def basal_metabolic_rate(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "basal metabolic rate":
                trait_array.append(trait)
        return trait_array
    
    # Get behavior.
    def behavior(taxon):
        behavior_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Behaviour"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Behaviour")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Behaviour" and data_subtype["dataSubtype"] == "":
                    behavior_array.append(data_subtype["mediaURL"])
        return behavior_array
    
    # Get behavioral circadian rhythm.
    def behavioral_circadian_rhythm(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get behaviour.
    def behaviour(taxon):
        return Taxon.behavior(taxon)
    
    # Get biology.
    def biology(taxon):
        bio_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Biology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Biology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Biology" and data_subtype["dataSubtype"] == "":
                    bio_array.append(data_subtype["description"])
        return bio_array
    
    # Get body length.
    # - Clinical ontology measurement (COM)
    # - Snout-vent (SV)
    # - Vent-to-tail (VT)
    def body_length(taxon, measurement="all"):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "body length (CMO)":
                trait_array.append(trait)
            elif trait["predicate"] == "body length (VT)":
                trait_array.append(trait)
        return trait_array
    
    # Get body mass.
    def body_mass(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "body mass":
                trait_array.append(trait)
        return trait_array
        
    # Get body temperature
    def body_temperature(taxon):
        print("NOT FUNCTIONAL")
    
    # Get brood size.
    def brood_size(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "clutch/brood/litter size":
                trait_array.append(trait)
        return trait_array
    
    # Get Citizen Science.
    def citizen_science(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get clutch size.
    def clutch_size(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "clutch/brood/litter size":
                trait_array.append(trait)
        return trait_array
    
    # Get conservation.
    def conservation(taxon):
        con_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Conservation"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Conservation")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Conservation" and data_subtype["dataSubtype"] == "":
                    con_array.append(data_subtype["description"])
        return con_array
    
    # Get conservation status.
    def conservation_status(taxon):
        con_stat_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "ConservationStatus"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "ConservationStatus")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#ConservationStatus" and data_subtype["dataSubtype"] == "":
                    con_stat_array.append(data_subtype["description"])
                
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "conservation status":
                trait_array.append(trait)
                
        return con_stat_array
    
    # Get cyclicity.
    def cyclicity(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get cytology.
    def cytology(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get description.
    def description(taxon):
        desc_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Description"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Description")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Description" and data_subtype["dataSubtype"] == "":
                    desc_array.append(data_subtype["description"])
        return desc_array
    
    # Get development.
    def development(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get diagnostic description.
    def diagnostic_description(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get diet.
    def diet(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "primary diet":
                trait_array.append(trait)
            elif trait["predicate"] == "diet includes":
                trait_array.append(trait)
        return trait_array
        
    # Get diet breadth.
    def diet_breadth(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "diet breadth":
                trait_array.append(trait)
        return trait_array
    
    # Get diseases.
    def diseases():
        dis_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Diseases"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Diseases")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Diseases" and data_subtype["dataSubtype"] == "":
                    dis_array.append(data_subtype["description"])
        return dis_array
    
    # Get dispersal.
    def dispersal(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get dispersal age.
    def dispersal_age(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "dispersal age":
                trait_array.append(trait)
        return trait_array
    
    # Get distribution.
    def distribution(taxon):
        distribution_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Distribution"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Distribution")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Distribution" and data_subtype["dataSubtype"] == "":
                    distribution_array.append(data_subtype["description"])
        return distribution_array
    
    # Get ecology.
    def ecology(taxon):
        ecology_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Ecology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Ecology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Ecology" and data_subtype["dataSubtype"] == "":
                    ecology_array.append(data_subtype["description"])
        return ecology_array
    
    # Get education.
    def education(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get education resources.
    def education_resources(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get elevation.
    def elevation(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "elevation":
                trait_array.append(trait)
        return trait_array
        
    # Get evolution.
    def evolution(taxon):
        evolution_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Evolution"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Evolution")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Evolution" and data_subtype["dataSubtype"] == "":
                    evolution_array.append(data_subtype["description"])
        return evolution_array
    
    # Get extinction status.
    def extinction_status(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "extinction status":
                trait_array.append(trait)
        return trait_array
    
    # Get first appearance.
    # - older
    # - younger
    def first_appearance(taxon, bound="older"):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "first appearance (older)" and bound == "older":
                trait_array.append(trait)
            elif trait["predicate"] == "first appearance (younger)" and bound == "younger":
                trait_array.append(trait)
        return trait_array
    
    # Get fossil history.
    def fossil_history(taxon):
        fossil_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "FossilHistory"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "FossilHistory")["dataObjects"]:
                if data_subtype["subject"] == "http://www.eol.org/voc/table_of_contents#FossilHistory" and data_subtype["dataSubtype"] == "":
                    fossil_array.append(data_subtype["description"])
        return fossil_array
    
    # Get functional adaptations.
    def functional_adaptations(taxon):
        func_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "FunctionalAdaptations"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "FunctionalAdaptations")["dataObjects"]:
                if data_subtype["subject"] == "http://www.eol.org/voc/table_of_contents#FunctionalAdaptations" and data_subtype["dataSubtype"] == "":
                    func_array.append(data_subtype["description"])
        return func_array
    
    # Get general description.
    def general_description(taxon):
        gen_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "GeneralDescription"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "GeneralDescription")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#GeneralDescription" and data_subtype["dataSubtype"] == "":
                    gen_array.append(data_subtype["description"])
        return gen_array
    
    # Get genetics.
    def genetics(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get genome.
    def genome(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get geographic distribution.
    def geographic_distribution(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "geographic distribution includes":
                trait_array.append(trait)
        return trait_array
    
    # Get geographic range.
    def geographic_range(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "geographic range (size of area)":
                trait_array.append(trait)
        return trait_array
    
    # Get gestation period duration.
    def gestation_period_duration(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "gestation period duration":
                trait_array.append(trait)
        return trait_array
    
    # Get growth.
    def growth(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get growth rate.
    def growth_rate(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get habitat.
    def habitat(taxon):
        habitat_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Habitat"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Habitat")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Behaviour" and data_subtype["dataSubtype"] == "":
                    habitat_array.append(data_subtype["description"])
                
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "habitat":
                trait_array.append(trait)
            elif trait["predicate"] == "habitat includes":
                trait_array.append(trait)
                
        return habitat_array
    
    # Get habitat breadth.
    def habitat_breadth(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "habitat breadth":
                trait_array.append(trait)
        return trait_array
    
    # Get home range.
    def home_range(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "home range":
                trait_array.append(trait)
        return trait_array
        
    # Get human population density.
    def human_population_density(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get human population density change.
    def human_population_density_change(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get identification resources.
    def identification_resources(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get inter-birth interval.
    def interbirth_interval(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "inter-birth interval":
                trait_array.append(trait)
        return trait_array
    
    # Get keys.
    def keys(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get last appearance.
    # - older
    # - younger
    def last_appearance(taxon, bound="older"):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "last appearance (younger bound)" and bound == "younger":
                trait_array.append(trait)
            elif trait["predicate"] == "last appearance (older bound)" and bound == "older":
                trait_array.append(trait)
        return trait_array
    
    # Get latitude.
    def latitude(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "latitude":
                trait_array.append(trait)
        return trait_array
    
    # Get legislation.
    def legislation(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get life cycle.
    def life_cycle(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get life expectancy.
    def life_expectancy(taxon):
        life_expect_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "LifeExpectancy"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "LifeExpectancy")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#LifeExpectancy" and data_subtype["dataSubtype"] == "":
                    life_expect_array.append(data_subtype["description"])
        return life_expect_array
    
    # Get litter size.
    def litter_size(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "clutch/brood/litter size":
                trait_array.append(trait)
        return trait_array
    
    # Get litters per year.
    def litters_per_year(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "litters per year":
                trait_array.append(trait)
        return trait_array
        
    # Get longitude.
    def longitude(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "longitude":
                trait_array.append(trait)
        return trait_array
    
    # Get look-alikes.
    def look_alikes(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get metabolic rate.
    def metabolic_rate(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "metabolic rate":
                trait_array.append(trait)
        return trait_array
    
    # Get migration.
    def migration(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get management.
    def management(taxon):
        manage_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Management"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Management")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Management" and data_subtype["dataSubtype"] == "":
                    manage_array.append(data_subtype["description"])
        return manage_array
        
    # Get mating system.
    def mating_system(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "Mating System":
                trait_array.append(trait)
        return trait_array
        
    # Get molecular biology.
    def molecular_biology(taxon):
        molec_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "MolecularBiology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "MolecularBiology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#MolecularBiology" and data_subtype["dataSubtype"] == "":
                    molec_array.append(data_subtype["description"])
        return molec_array    
        
    # Get morphology.
    def morphology(taxon):
        morph_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Morphology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Morphology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Morphology" and data_subtype["dataSubtype"] == "":
                    morph_array.append(data_subtype["description"])
        return morph_array
    
    # Get notes.
    def notes(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get nucleotide sequences.
    def nucleotide_sequences(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get onset of fertility.
    def onset_of_fertility(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "onset of fertility":
                trait_array.append(trait)
        return trait_array
    
    # Get parental care.
    def parental_care(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "parental care":
                trait_array.append(trait)
        return trait_array
    
    # Get phylogenetics.
    def phylogenetics(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get physiology.
    def physiology(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get population biology.
    def population_biology(taxon):
        pop_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "PopulationBiology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "PopulationBiology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#PopulationBiology" and data_subtype["dataSubtype"] == "":
                    pop_array.append(data_subtype["description"])
        return pop_array
    
    # Get population trend.
    def population_trend(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "population trend":
                trait_array.append(trait)
        return trait_array
        
    # Get potential evapotranspiration rate in geographic range.
    def potential_evapotranspiration_rate_in_geographic_range(taxon):
        print("NOT FUNCTIONAL.")    
    
    # Get precipitation in geographic range.
    def precipitation_in_geographic_range(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get prenatal development duration.
    def prenatal_development_duration(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get procedures.
    def procedures(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get reproduction.
    def reproduction(taxon):
        repro_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "TrophicStrategy"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "TrophicStrategy")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Reproduction" and data_subtype["dataSubtype"] == "":
                    repro_array.append(data_subtype["description"])
        return repro_array
    
    # Get risk statement.
    def risk_statement(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get social group size.
    def social_group_size(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get social system.
    def social_system(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "Social System":
                trait_array.append(trait)
        return trait_array
    
    # Get systematics.
    def systematics(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get taxon biology.
    def taxon_biology(taxon):
        bio_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "TaxonBiology"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "TaxonBiology")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#TaxonBiology" and data_subtype["dataSubtype"] == "":
                    bio_array.append(data_subtype["description"])
        return bio_array
    
    # Get taxonomic classification of taxon node.
    def taxonomic_classification(taxon, source = "ensembl"):
        if source == "ensembl" and taxon.scientific_name:
            server = "http://rest.ensembl.org"
            ext = "/taxonomy/classification/" + taxon.scientific_name + "?"
            
            r = requests.get(server+ext, headers={"Content-Type": "application/json"})
            
            if not r.ok:
                r.raise_for_status()
                sys.exit()
                
            decoded = r.json()
            
            return decoded
    
    # Get taxonomy.
    def taxonomy(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get teat number.
    def teat_number(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get temperature in geographic range.
    def temperature_in_geographic_range(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get terrestriality.
    def terrestriality(taxon):
        print("NOT FUNCTIONAL.")
    
    # Get threats.
    def threats(taxon):
        threat_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Threats"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Threats")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Threats" and data_subtype["dataSubtype"] == "":
                    threat_array.append(data_subtype["description"])
        return threat_array
    
    # Get total life span.
    def total_life_span(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "total life span":
                trait_array.append(trait)
        return trait_array
        
    # Get trends.
    def trends(taxon):
        trend_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Trends"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Trends")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Trends" and data_subtype["dataSubtype"] == "":
                    trend_array.append(data_subtype["description"])
        return trend_array
        
    # Get trophic level.
    def trophic_level(taxon):
        print("NOT FUNCTIONAL.")
        
    # Get trophic strategy.
    def trophic_strategy(taxon):
        trophic_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "TrophicStrategy"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "TrophicStrategy")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#TrophicStrategy" and data_subtype["dataSubtype"] == "":
                    trophic_array.append(data_subtype["description"])
        return trophic_array
    
    # Get type information.
    def type_information(taxon):
        type_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "TypeInformation"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "TypeInformation")["dataObjects"]:
                if data_subtype["subject"] == "http://www.eol.org/voc/table_of_contents#TypeInformation" and data_subtype["dataSubtype"] == "":
                    type_array.append(data_subtype["description"])
        return type_array
    
    # Get uses.
    def uses(taxon):
        use_array = []
        if "dataObjects" in Taxon.eol_page(taxon, subjects = "Uses"):
            for data_subtype in Taxon.eol_page(taxon, subjects = "Uses")["dataObjects"]:
                if data_subtype["subject"] == "http://rs.tdwg.org/ontology/voc/SPMInfoItems#Uses" and data_subtype["dataSubtype"] == "":
                    use_array.append(data_subtype["description"])
        return use_array
    
    # Get weaning age.
    def weaning_age(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "weaning age":
                trait_array.append(trait)
        return trait_array
        
    # Get weight.
    def weight(taxon):
        trait_array = []
        for trait in Taxon.eol_traitbank(taxon)["item"]["traits"]:
            if trait["predicate"] == "weight":
                trait_array.append(trait)
        return trait_array
        
    """
        Auxiliary functions:
        
        Scrape taxonomic names
        Search
        
    """
    
    # Scrape taxonomic names.
    def scrape(url):
        out = pytaxize.scrapenames(url = url)
        return out
    
    # Search for taxa.
    def search(query, source = "eol", page = 1, exact = True, filter_by_taxon_concept_id = "", filter_by_hierarchy_entry_id = "", filter_by_string = "", cache_ttl = "", user = None):
        return search(query, source = source, page = page, exact = exact, filter_by_taxon_concept_id = filter_by_taxon_concept_id, filter_by_hierarchy_entry_id = filter_by_hierarchy_entry_id, filter_by_string = filter_by_string, cache_ttl = cache_ttl)
    
    """
        External files:
        
        Images
        Maps
        Sounds
        Videos
    """
    
    # Return images.
    def images(taxon, source = "eol"):
        image_array = []
        if source == "eol":
            for data_subtype in Taxon.eol_page(taxon)["dataObjects"]:
                if data_subtype["dataType"] == "http://purl.org/dc/dcmitype/StillImage" and data_subtype["dataSubtype"] == "":
                    image_array.append(data_subtype["mediaURL"])
        elif source == "wiki":
            for stuff in AnatomicalStructure.wikidata(anatomical_structure):
                for prop_id, prop_dict in stuff["claims"].items():
                    base = "https://www.wikidata.org/w/api.php"
                    ext = "?action=wbgetentities&ids=" + prop_id + "&format=json"
                    r = requests.get(base+ext, headers={"Content-Type": "application/json"})
                    if not r.ok:
                        r.raise_for_status()
                        sys.exit()
                    decoded = json.loads(r.text)
                    en_prop_name = decoded["entities"][prop_id]["labels"]["en"]["value"]
                    if en_prop_name.lower() == "image":
                        for x in prop_dict:
                            imag_url = "https://commons.wikimedia.org/wiki/File:" + x["mainsnak"]["datavalue"]["value"]
                            image_url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + x["mainsnak"]["datavalue"]["value"]
                            image_array.append(image_url)
        else:
            print("Source not found.")
        return image_array
    
    # Return maps.
    def maps(taxon):
        map_array = []
        for data_subtype in Taxon.eol_page(taxon)["dataObjects"]:
            if data_subtype["dataSubtype"] == "Map":
                map_array.append(data_subtype["mediaURL"])
        return map_array
        
    # Return sounds.
    def sounds(taxon):
        sound_array = []
        for data_subtype in Taxon.eol_page(taxon)["dataObjects"]:
            if data_subtype["dataSubtype"] == "http://purl.org/dc/dcmitype/Sound":
                sound_array.append(data_subtype["mediaURL"])
        return sound_array
    
    # Return videos.
    def videos(taxon):
        video_array = []
        for data_subtype in Taxon.eol_page(taxon)["dataObjects"]:
            if data_subtype["dataSubtype"] == "http://purl.org/dc/dcmitype/MovingImage":
                video_array.append(data_subtype["mediaURL"])
        return video_array

#   UNIT TESTS
def taxon_unit_tests(sci_name):
    print("Creating user...")
    user = User(eol_api_key = eol_api_key)
    print("User created successfully.\n")
    sci_tax = gnomics.objects.taxon.Taxon(identifier = str(sci_name), identifier_type = "Scientific Name", language="Latin", source = "EOL")

#   MAIN
if __name__ == "__main__": main()