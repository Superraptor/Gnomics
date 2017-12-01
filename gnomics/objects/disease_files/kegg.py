#
#
#
#
#

#
#   IMPORT SOURCES:
#       BIOSERVICES
#           https://pythonhosted.org/bioservices/
#


#
#   Get KEGG Disease ID.
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

#   Other imports.
from bioservices import *

#   MAIN
def main():
    kegg_disease_unit_tests()
    
# Return KEGG disease object.
def get_kegg_disease(dis):
    for dis_obj in dis.disease_objects:
        if 'object_type' in dis_obj:
            if dis_obj['object_type'].lower() == 'kegg' or dis_obj['object_type'].lower() == 'kegg disease':
                return dis_obj['object']
    s = KEGG()
    res = s.get(gnomics.objects.disease.Disease.kegg_disease_id(dis))
    disease = s.parse(res)
    dis.disease_objects.append({
        'object': disease,
        'object_type': "KEGG disease",
    })
    return disease

#   Get KEGG disease ID.
def get_kegg_disease_id(dis):
    for ident in dis.identifiers:
        if ident["identifier_type"].lower() == "kegg" or ident["identifier_type"].lower() == "kegg id" or ident["identifier_type"].lower() == "kegg identifier" or ident["identifier_type"].lower() == "kegg disease id":
            return ident["identifier"]

#   UNIT TESTS
def kegg_disease_unit_tests():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()