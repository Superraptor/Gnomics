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
#   Get RxCUI.
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
import gnomics.objects.drug

#   Other imports.
import json
import pubchempy as pubchem
import requests

#   MAIN
def main():
    rxcui_type_unit_tests("5640")
    rxcui_unit_tests("D000212", "DB00773", "1039008", "L01CB01", "23080", "ANDA007581", "26", "009172", "108077", "98350030002800", "14375", "004489", "CD1001", "NDA021400", "00904629161", "N0000148200", "1C5BC1DD-E9EC-44C1-9281-67AD482315D9", "C0000266", "4021359")
    
#   Get RxNorm object.
def get_rxnorm_obj(drug):
    for drug_obj in drug.drug_objects:
        if 'object_type' in drug_obj:
            if drug_obj['object_type'].lower() == 'rxnorm' or drug_obj['object_type'].lower() == 'rxcui':
                return drug_obj['object']
    for rx in gnomics.objects.drug.Drug.rxcui(drug):
        base = "https://rxnav.nlm.nih.gov/REST/"
        ext = "rxcui/" + rx + "/allProperties.json?prop=all"
        r = requests.get(base+ext, headers={"Content-Type": "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = json.loads(r.text)
        rx_obj = {}
        for properties in decoded["propConceptGroup"]["propConcept"]:
            if properties["propName"] == "AVAILABLE_STRENGTH":
                rx_obj["available_strength"] = properties["propValue"]
            elif properties["propName"] == "GENERAL_CARDINALITY":
                rx_obj["general_cardinality"] = properties["propValue"]
            elif properties["propName"] == "NUI":
                if "nui" in rx_obj:
                    rx_obj["nui"].append(properties["propValue"])
                else:
                    rx_obj["nui"] = [properties["propValue"]]
            elif properties["propName"] == "VUID":
                if "vuid" in rx_obj:
                    rx_obj["vuid"].append(properties["propValue"])
                else:
                    rx_obj["vuid"] = [properties["propValue"]]
            elif properties["propName"] == "ATC":
                if "atc" in rx_obj:
                    rx_obj["atc"].append(properties["propValue"])
                else:
                    rx_obj["atc"] = [properties["propValue"]]
            elif properties["propName"] == "DRUGBANK":
                if "drugbank" in rx_obj:
                    rx_obj["drugbank"].append(properties["propValue"])
                else:
                    rx_obj["drugbank"] = [properties["propValue"]]
            elif properties["propName"] == "MESH":
                if "mesh" in rx_obj:
                    rx_obj["mesh"].append(properties["propValue"])
                else:
                    rx_obj["mesh"] = [properties["propValue"]]
            elif properties["propName"] == "RxCUI":
                if "rxcui" in rx_obj:
                    rx_obj["rxcui"].append(properties["propValue"])
                else:
                    rx_obj["rxcui"] = [properties["propValue"]]
            elif properties["propName"] == "MMSL_CODE":
                if "mmsl_code" in rx_obj:
                    rx_obj["mmsl_code"].append(properties["propValue"])
                else:
                    rx_obj["mmsl_code"] = [properties["propValue"]]
            elif properties["propName"] == "UNII_CODE":
                if "unii_code" in rx_obj:
                    rx_obj["unii_code"].append(properties["propValue"])
                else:
                    rx_obj["unii_code"] = [properties["propValue"]]
            elif properties["propName"] == "SPL_SET_ID":
                if "spl_set_id" in rx_obj:
                    rx_obj["spl_set_id"].append(properties["propValue"])
                else:
                    rx_obj["spl_set_id"] = [properties["propValue"]]
            elif properties["propName"] == "UMLSCUI":
                if "umls_cui" in rx_obj:
                    rx_obj["umls_cui"].append(properties["propValue"])
                else:
                    rx_obj["umls_cui"] = [properties["propValue"]]
            elif properties["propName"] == "SNOMEDCT":
                if "snomed_ct" in rx_obj:
                    rx_obj["snomed_ct"].append(properties["propValue"])
                else:
                    rx_obj["snomed_ct"] = [properties["propValue"]]
            elif properties["propName"] == "RxNorm Name":
                if "rxnorm_name" in rx_obj:
                    rx_obj["rxnorm_name"].append(properties["propValue"])
                else:
                    rx_obj["rxnorm_name"] = [properties["propValue"]]
            elif properties["propName"] == "Prescribable Synonym":
                rx_obj["prescribable_synonym"] = properties["propValue"]
        drug.drug_objects.append({
            'object': rx_obj,
            'object_type': "RxNorm"
        })
        return rx_obj
    
#   Get RxCUI.
def get_rxcui(drug):
    rxcui_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            rxcui_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "mesh uid" or ident["identifier_type"].lower() == "mesh unique identifier":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=MESH&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "idGroup" in decoded:
                if "rxnormId" in decoded["idGroup"]:
                    for x in decoded["idGroup"]["rxnormId"]:
                        if x not in rxcui_array:
                            rxcui_array.append(x)
                            drug.identifiers.append({
                                'identifier': x,
                                'language': None,
                                'identifier_type': "RxCUI",
                                'source': "RxNorm"
                            })  
        elif ident["identifier_type"].lower() == "drugbank id" or ident["identifier_type"].lower() == "drugbank" or ident["identifier_type"].lower() == "drugbank identifier" or ident["identifier_type"].lower() == "drugbank accession":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=DrugBank&allSourcesFlag=1&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
                    drug.identifiers.append({
                        'identifier': x,
                        'language': None,
                        'identifier_type': "RxCUI",
                        'source': "RxNorm"
                    })
        elif ident["identifier_type"].lower() == "snomed" or ident["identifier_type"].lower() == "snomed-ct":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=SNOMEDCT&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "atc" or ident["identifier_type"].lower() == "atc code":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=ATC&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "ampid":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=AMPID&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "anda" or ident["identifier_type"].lower() == "fda anda" or ident["identifier_type"].lower() == "fda abbreviated new drug application identifier" or ident["identifier_type"].lower() == "fda abbreviated new drug application id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=ANDA&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "cvx" or ident["identifier_type"].lower() == "vaccine code":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=CVX&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "generic code sequence number" or ident["identifier_type"].lower() == "gcn":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=GCN_SEQNO&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "generic formula code" or ident["identifier_type"].lower() == "gfc":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=GFC&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "rxnormId" in decoded["idGroup"]:
                for rx in decoded["idGroup"]["rxnormId"]:
                    if rx not in rxcui_array:
                        rxcui_array.append(rx)
        elif ident["identifier_type"].lower() == "generic product identifier" or ident["identifier_type"].lower() == "gpi":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=GPI&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "rxnormId" in decoded["idGroup"]:
                for rx in decoded["idGroup"]["rxnormId"]:
                    if rx not in rxcui_array:
                        rxcui_array.append(rx)
        elif ident["identifier_type"].lower() == "generic product packaging code" or ident["identifier_type"].lower() == "gppc":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=GPPC&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "rxnormId" in decoded["idGroup"]:
                for rx in decoded["idGroup"]["rxnormId"]:
                    if rx not in rxcui_array:
                        rxcui_array.append(rx)
        elif ident["identifier_type"].lower() == "fdb hierarchical ingredient code sequence number" or ident["identifier_type"].lower() == "hierarchical ingredient code sequence number" or ident["identifier_type"].lower() == "hic_seqn":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=HIC_SEQN&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "mmsl code" or ident["identifier_type"].lower() == "multum mediasource lexicon code":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=MMSL_CODE&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "fda nda" or ident["identifier_type"].lower() == "nda" or ident["identifier_type"].lower() == "fda new drug application id" or ident["identifier_type"].lower() == "fda new drug application identifier":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=NDA&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "ndc" or ident["identifier_type"].lower() == "national drug code":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=NDC&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "nui" or ident["identifier_type"].lower() == "national drug file reference terminology unique identifier" or ident["identifier_type"].lower() == "national drug file reference terminology unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=NUI&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "spl set id" or ident["identifier_type"].lower() == "spl set identifier" or ident["identifier_type"].lower() == "fda structured product label set identifier" or ident["identifier_type"].lower() == "structured product label set identifier":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=SPL_SET_ID&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "umls id" or ident["identifier_type"].lower() == "umls cui" or ident["identifier_type"].lower() == "umls concept id" or ident["identifier_type"].lower() == "umls concept unique identifier" or ident["identifier_type"].lower() == "umls concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=UMLSCUI&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
        elif ident["identifier_type"].lower() == "vuid" or ident["identifier_type"].lower() == "veterans health administration unique identifier" or ident["identifier_type"].lower() == "veterans health administration unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui.json?idtype=VUID&id=" + ident["identifier"]
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for x in decoded["idGroup"]["rxnormId"]:
                if x not in rxcui_array:
                    rxcui_array.append(x)
    return rxcui_array

def get_related_rxcuis(drug):
    rxcui_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            bn = get_rxcui_bn(drug)
            bpck = get_rxcui_bpck(drug)
            df = get_rxcui_df(drug)
            dfg = get_rxcui_dfg(drug)
            ins = get_rxcui_in(drug)
            mins = get_rxcui_min(drug)
            pins = get_rxcui_pin(drug)
            sbd = get_rxcui_sbd(drug)
            sbdc = get_rxcui_sbdc(drug)
            sbdf = get_rxcui_sbdf(drug)
            sbdg = get_rxcui_sbdg(drug)
            scd = get_rxcui_scd(drug)
            scdc = get_rxcui_scdc(drug)
            scdf = get_rxcui_scdf(drug)
            scdg = get_rxcui_scdg(drug)
            rxcui_array.append(ident["identifier"])
            rxcui_array.extend(bn)
            rxcui_array.extend(bpck)
            rxcui_array.extend(df)
            rxcui_array.extend(dfg)
            rxcui_array.extend(ins)
            rxcui_array.extend(mins)
            rxcui_array.extend(pins)
            rxcui_array.extend(sbd)
            rxcui_array.extend(sbdc)
            rxcui_array.extend(sbdf)
            rxcui_array.extend(sbdg)
            rxcui_array.extend(scd)
            rxcui_array.extend(scdc)
            rxcui_array.extend(scdf)
            rxcui_array.extend(scdg)
            rxcui_array = list(set(rxcui_array))
    return rxcui_array

#   Get RxCUI BNs (brand names).
def get_rxcui_bn(drug):
    rxcui_bn_array = []
    rxcui_bn_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui bn" or ident["identifier_type"].lower() == "rxcui brand name":
            rxcui_bn_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "bn"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                if iden["rxcui"] not in rxcui_bn_array:
                    temp_drug = gnomics.objects.drug.Drug( identifier = iden["rxcui"], identifier_type = "RxCUI BN", source = "RxNorm")
                    if "umlscui" in iden:
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                    if "name" in iden and "language" in iden:
                        if iden["language"] == "ENG":
                            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Brand Name", source = "RxNorm", language = "en")
                    rxcui_bn_obj_array.append(temp_drug)
                    rxcui_bn_array.append(iden["rxcui"])
    return rxcui_bn_array
    
#   Get RxCUI BPCKs (branded packs).
def get_rxcui_bpck(drug):
    rxcui_bpck_array = []
    rxcui_bpck_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui bpck" or ident["identifier_type"].lower() == "rxcui branded pack":
            rxcui_bpck_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "bpck"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "conceptProperties" in decoded["relatedGroup"]["conceptGroup"][0]:
                for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                    temp_drug = gnomics.objects.drug.Drug( identifier = iden["rxcui"], identifier_type = "RxCUI BPCK", source = "RxNorm")
                    if "umlscui" in iden:
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                    if "name" in iden and "language" in iden:
                        if iden["language"] == "ENG":
                            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Branded Pack", source = "RxNorm", language = "en")
                    rxcui_bpck_obj_array.append(temp_drug)
                    rxcui_bpck_array.append(iden["rxcui"])
    return rxcui_bpck_array

#   Get RxCUI DFs (dose forms).
def get_rxcui_df(drug):
    rxcui_df_array = []
    rxcui_df_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui df" or ident["identifier_type"].lower() == "rxcui dose form":
            rxcui_df_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "df"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI DF", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Dose Form", source = "RxNorm", language = "en")
                rxcui_df_obj_array.append(temp_drug)
                rxcui_df_array.append(iden["rxcui"])
    return rxcui_df_array

#   Get RxCUI DFGs (dose form groups).
def get_rxcui_dfg(drug):
    rxcui_dfg_array = []
    rxcui_dfg_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui dfg" or ident["identifier_type"].lower() == "rxcui dose form group":
            rxcui_dfg_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "dfg"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI DFG", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Dose Form Group", source = "RxNorm", language = "en")
                rxcui_dfg_obj_array.append(temp_drug)
                rxcui_dfg_array.append(iden["rxcui"])
    return rxcui_dfg_array

#   Get RxCUI INs (ingredients).
def get_rxcui_in(drug):
    rxcui_in_array = []
    rxcui_in_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui in" or ident["identifier_type"].lower() == "rxcui ingredient":
            rxcui_in_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "in"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI IN", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Ingredient", source = "RxNorm", language = "en")
                rxcui_in_obj_array.append(temp_drug)
                rxcui_in_array.append(iden["rxcui"])
    return rxcui_in_array
    
#   Get RxCUI MINs (multiple ingredients).
def get_rxcui_min(drug):
    rxcui_min_array = []
    rxcui_min_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui min" or ident["identifier_type"].lower() == "rxcui multiple ingredient":
            rxcui_min_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "min"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "conceptProperties" in decoded["relatedGroup"]["conceptGroup"][0]:
                for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                    temp_drug =  gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI MIN", source = "RxNorm")
                    if "umlscui" in iden:
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                    if "name" in iden and "language" in iden:
                        if "language" == "ENG":
                            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Multiple Ingredient", source = "RxNorm", language = "en")
                    rxcui_min_obj_array.append(temp_drug)
                    rxcui_min_array.append(iden["rxcui"])
    return rxcui_min_array
    
#   Get RxCUI PINs (precise ingredients).
def get_rxcui_pin(drug):
    rxcui_pin_array = []
    rxcui_pin_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui pin" or ident["identifier_type"].lower() == "rxcui precise ingredient":
            rxcui_pin_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "pin"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            if "conceptProperties" in decoded["relatedGroup"]["conceptGroup"][0]:
                for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                    temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI PIN", source = "RxNorm")
                    if "umlscui" in iden:
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                    if "name" in iden and "language" in iden:
                        if "language" == "ENG":
                            gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Precise Ingredient", source = "RxNorm", language = "en")
                    rxcui_pin_obj_array.append(temp_drug)
                    rxcui_pin_array.append(iden["rxcui"])
    return rxcui_pin_array
    
#   Get RxCUI SBDs (branded drugs).
def get_rxcui_sbd(drug):
    rxcui_sbd_array = []
    rxcui_sbd_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui sbd" or ident["identifier_type"].lower() == "rxcui branded drug":
            rxcui_sbd_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "sbd"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SBD", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Branded Drug", source = "RxNorm", language = "en")
                rxcui_sbd_obj_array.append(temp_drug)
                rxcui_sbd_array.append(iden["rxcui"])
    return rxcui_sbd_array
    
#   Get RxCUI SBDC (branded drug components).
def get_rxcui_sbdc(drug):
    rxcui_sbdc_array = []
    rxcui_sbdc_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui sbdc" or ident["identifier_type"].lower() == "rxcui branded drug component":
            rxcui_sbdc_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "sbdc"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SBDC", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Branded Drug Component", source = "RxNorm", language = "en")
                rxcui_sbdc_obj_array.append(temp_drug)
                rxcui_sbdc_array.append(iden["rxcui"])
    return rxcui_sbdc_array
    
#   Get RxCUI SBDF (branded dose forms).
def get_rxcui_sbdf(drug):
    rxcui_sbdf_array = []
    rxcui_sbdf_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui sbdf" or ident["identifier_type"].lower() == "rxcui branded dose form":
            rxcui_sbdf_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "sbdf"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SBDF", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Branded Dose Form", source = "RxNorm", language = "en")
                rxcui_sbdf_obj_array.append(temp_drug)
                rxcui_sbdf_array.append(iden["rxcui"])
    return rxcui_sbdf_array
    
#   Get RxCUI SBDG (branded dose form groups).
def get_rxcui_sbdg(drug):
    rxcui_sbdg_array = []
    rxcui_sbdg_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui sbdg" or ident["identifier_type"].lower() == "rxcui branded dose form group":
            rxcui_sbdg_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "sbdg"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SBDG", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Branded Dose Form Group", source = "RxNorm", language = "en")
                rxcui_sbdg_obj_array.append(temp_drug)
                rxcui_sbdg_array.append(iden["rxcui"])
    return rxcui_sbdg_array
    
#   Get RxCUI SCD (clinical drugs).
def get_rxcui_scd(drug):
    rxcui_scd_array = []
    rxcui_scd_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui scd" or ident["identifier_type"].lower() == "rxcui clinical drug":
            rxcui_scd_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "scd"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SCD", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Clinical Drug", source = "RxNorm", language = "en")
                rxcui_scd_obj_array.append(temp_drug)
                rxcui_scd_array.append(iden["rxcui"])
    return rxcui_scd_array
    
#   Get RxCUI SCDC (clinical drug components).
def get_rxcui_scdc(drug):
    rxcui_scdc_array = []
    rxcui_scdc_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui scdc" or ident["identifier_type"].lower() == "rxcui clinical drug component":
            rxcui_scdc_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "scdc"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SCDC", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Clinical Drug Component", source = "RxNorm", language = "en")
                rxcui_scdc_obj_array.append(temp_drug)
                rxcui_scdc_array.append(iden["rxcui"])
    return rxcui_scdc_array
    
#   Get RxCUI SCDF (clinical dose forms).
def get_rxcui_scdf(drug):
    rxcui_scdf_array = []
    rxcui_scdf_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui scdf" or ident["identifier_type"].lower() == "rxcui clinical dose form":
            rxcui_scdf_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "scdf"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SCDF", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Clinical Dose Form", source = "RxNorm", language = "en")
                rxcui_scdf_obj_array.append(temp_drug)
                rxcui_scdf_array.append(iden["rxcui"])
    return rxcui_scdf_array
    
#   Get RxCUI SCDG (clinical dose form groups).
def get_rxcui_scdg(drug):
    rxcui_scdg_array = []
    rxcui_scdg_obj_array = []
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui scdg" or ident["identifier_type"].lower() == "rxcui clinical dose form group":
            rxcui_scdg_array.append(ident["identifier"])
    for ident in drug.identifiers:
        if ident["identifier_type"].lower() == "rxcui" or ident["identifier_type"].lower() == "rxnorm concept unique identifier" or ident["identifier_type"].lower() == "rxnorm concept unique id":
            base = "https://rxnav.nlm.nih.gov/REST/"
            ext = "rxcui/" + ident["identifier"] + "/related.json?tty=" + "scdg"
            r = requests.get(base+ext, headers={"Content-Type": "application/json"})
            if not r.ok:
                r.raise_for_status()
                sys.exit()
            decoded = json.loads(r.text)
            for iden in decoded["relatedGroup"]["conceptGroup"][0]["conceptProperties"]:
                temp_drug = gnomics.objects.drug.Drug(identifier = iden["rxcui"], identifier_type = "RxCUI SCDG", source = "RxNorm")
                if "umlscui" in iden:
                    gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["umlscui"], identifier_type = "UMLS CUI", source = "RxNorm")
                if "name" in iden and "language" in iden:
                    if "language" == "ENG":
                        gnomics.objects.drug.Drug.add_identifier(temp_drug, identifier = iden["name"], identifier_type = "Clinical Dose Form Group", source = "RxNorm", language = "en")
                rxcui_scdg_obj_array.append(temp_drug)
                rxcui_scdg_array.append(iden["rxcui"])
    return rxcui_scdg_array
    
#   UNIT TESTS
def rxcui_unit_tests(mesh_uid, drugbank_id, snomedct, atc_code, ampid, anda, cvx, gcn_seqno, gfc, gpi, gppc, hic_seqn, mmsl_code, nda, ndc, nui, spl_set_id, umls_cui, vuid):
    mesh_com = gnomics.objects.drug.Drug(identifier = str(mesh_uid), identifier_type = "MeSH UID", source = "MeSH")
    print("\nGetting RxCUIs from MeSH UID (%s):" % mesh_uid)
    for rx in get_rxcui(mesh_com):
        print("- " + str(rx))
    
    drugbank_com = gnomics.objects.drug.Drug(identifier = str(drugbank_id), identifier_type = "DrugBank ID", source = "DrugBank")
    print("\nGetting RxCUIs from DrugBank ID (%s):" % drugbank_id)
    for rx in get_rxcui(drugbank_com):
        print("- " + str(rx))
    
    snomed_com = gnomics.objects.drug.Drug(identifier = str(snomedct), identifier_type = "SNOMED-CT", source = "SNOMED")
    print("\nGetting RxCUIs from SNOMED-CT (%s):" % snomedct)
    for rx in get_rxcui(snomed_com):
        print("- " + str(rx))
    
    atc_com = gnomics.objects.drug.Drug(identifier = str(atc_code), identifier_type = "ATC Code", source = "ATC")
    print("\nGetting RxCUIs from ATC Code (%s):" % atc_code)
    for rx in get_rxcui(atc_com):
        print("- " + str(rx))
        
    amp_com = gnomics.objects.drug.Drug(identifier = str(ampid), identifier_type = "AMPID", source = "Gold Standard Drug Database")
    print("\nGetting RxCUIs from AMPID (%s):" % ampid)
    for rx in get_rxcui(amp_com):
        print("- " + str(rx))
        
    anda_com = gnomics.objects.drug.Drug(identifier = str(anda), identifier_type = "ANDA", source = "FDA Abbreviated New Drug Application")
    print("\nGetting RxCUIs from ANDA (%s):" % anda)
    for rx in get_rxcui(anda_com):
        print("- " + str(rx))
        
    cvx_com = gnomics.objects.drug.Drug(identifier = str(cvx), identifier_type = "CVX", source = "Vaccine Code")
    print("\nGetting RxCUIs from CVX (%s):" % cvx)
    for rx in get_rxcui(cvx_com):
        print("- " + str(rx))
        
    gcn_com = gnomics.objects.drug.Drug(identifier = str(gcn_seqno), identifier_type = "GCN", source = "First Databank Inc.")
    print("\nGetting RxCUIs from GCN (%s):" % gcn_seqno)
    for rx in get_rxcui(gcn_com):
        print("- " + str(rx))
        
    gfc_com = gnomics.objects.drug.Drug(identifier = str(gfc), identifier_type = "GFC", source = "Micromedex RED BOOK")
    print("\nGetting RxCUIs from GFC (%s):" % gfc)
    for rx in get_rxcui(gfc_com):
        print("- " + str(rx))
        
    gpi_com = gnomics.objects.drug.Drug(identifier = str(gpi), identifier_type = "GPI", source = "Master Drug Data Base")
    print("\nGetting RxCUIs from GPI (%s):" % gpi)
    for rx in get_rxcui(gpi_com):
        print("- " + str(rx))
        
    gppc_com = gnomics.objects.drug.Drug(identifier = str(gppc), identifier_type = "GPPC", source = "Master Drug Data Base")
    print("\nGetting RxCUIs from GPPC (%s):" % gppc)
    for rx in get_rxcui(gppc_com):
        print("- " + str(rx))
        
    hic_com = gnomics.objects.drug.Drug(identifier = str(hic_seqn), identifier_type = "HIC_SEQN", source = "First Databank Inc.")
    print("\nGetting RxCUIs from HIC_SEQN (%s):" % hic_seqn)
    for rx in get_rxcui(hic_com):
        print("- " + str(rx))
        
    mmsl_com = gnomics.objects.drug.Drug(identifier = str(mmsl_code), identifier_type = "MMSL Code", source = "Multum Mediasource Lexicon")
    print("\nGetting RxCUIs from MMSL Code (%s):" % mmsl_code)
    for rx in get_rxcui(mmsl_com):
        print("- " + str(rx))
        
    nda_com = gnomics.objects.drug.Drug(identifier = str(nda), identifier_type = "NDA", source = "FDA")
    print("\nGetting RxCUIs from NDA ID (%s):" % nda)
    for rx in get_rxcui(nda_com):
        print("- " + str(rx))
        
    ndc_com = gnomics.objects.drug.Drug(identifier = str(ndc), identifier_type = "NDC", source = "National Drug Code Directory")
    print("\nGetting RxCUIs from NDC (%s):" % ndc)
    for rx in get_rxcui(ndc_com):
        print("- " + str(rx))
        
    nui_com = gnomics.objects.drug.Drug(identifier = str(nui), identifier_type = "NUI", source = "National Drug File Reference Terminology")
    print("\nGetting RxCUIs from NUI (%s):" % nui)
    for rx in get_rxcui(nui_com):
        print("- " + str(rx))
        
    spl_com = gnomics.objects.drug.Drug(identifier = str(spl_set_id), identifier_type = "SPL Set ID", source = "FDA")
    print("\nGetting RxCUIs from SPL Set ID (%s):" % spl_set_id)
    for rx in get_rxcui(spl_com):
        print("- " + str(rx))
        
    umls_com = gnomics.objects.drug.Drug(identifier = str(umls_cui), identifier_type = "UMLS CUI", source = "UMLS")
    print("\nGetting RxCUIs from UMLS CUI (%s):" % umls_cui)
    for rx in get_rxcui(umls_com):
        print("- " + str(rx))
        
    vuid_com = gnomics.objects.drug.Drug(identifier = str(vuid), identifier_type = "VUID", source = "Veterans Health Administration National Drug File ")
    print("\nGetting RxCUIs from VUID (%s):" % vuid)
    for rx in get_rxcui(vuid_com):
        print("- " + str(rx))
        
def rxcui_type_unit_tests(rxcui):
    rx_drug = gnomics.objects.drug.Drug(identifier = str(rxcui), identifier_type = "RxCUI", source = "RxNorm")
    
    print("Getting RxCUI BNs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_bn(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI BN":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI BPCKs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_bpck(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI BPCK":
                print("- %s" % (iden["identifier"]))
    
    print("\nGetting RxCUI DFs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_df(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI DF":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI DFGs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_dfg(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI DFG":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI INs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_in(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI IN":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI MINs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_min(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI MIN":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI PINs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_pin(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI PIN":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SBDs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_sbd(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SBD":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SBDCs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_sbdc(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SBDC":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SBDFs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_sbdf(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SBDF":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SBDGs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_sbdg(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SBDG":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SCDs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_scd(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SCD":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SCDCs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_scdc(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SCDC":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SCDFs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_scdf(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SCDF":
                print("- %s" % (iden["identifier"]))
                
    print("\nGetting RxCUI SCDGs from RxCUI (%s):" % rxcui)
    for rx in get_rxcui_scdg(rx_drug):
        for iden in rx.identifiers:
            if iden["identifier_type"] == "RxCUI SCDG":
                print("- %s" % (iden["identifier"]))

#   MAIN
if __name__ == "__main__": main()