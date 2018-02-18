#!/usr/bin/env python

#
#
#
#
#

#
#   IMPORT SOURCES:
#       PYYAML
#           https://github.com/yaml/pyyaml
#

#
#   Get PyYAML.
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
import gnomics.objects.reference

#   Other imports.
from ruamel.yaml import YAML
import yaml

#   MAIN
def main():
    yaml_unit_tests()
    
#   UNIT TESTS
def yaml_unit_tests():
    print("NOT FUNCTIONAL")

#   MAIN
if __name__ == "__main__": main()#   ?