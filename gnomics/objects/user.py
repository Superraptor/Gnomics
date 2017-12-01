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
#   Get user information for other programs.
#

#   PRE-CODE
import faulthandler
faulthandler.enable()

#   IMPORTS
from lxml.html import fromstring
from pymedtermino import *
from pymedtermino.umls import *
import json
import requests

#   MAIN
def main():
    print("NOT FUNCTIONAL.")

#   USER CLASS
class User:
    """
        User class:
        
    """
    
    # Initialize user.
    def __init__(self, chemspider_security_token = None, email = None, umls_host = None, umls_user = None, umls_password = None, omim_api_key = None, umls_api_key = None, eol_api_key = None, openphacts_app_id = None, openphacts_app_key = None, dpla_api_key = None, springer_api_key = None, elsevier_api_key = None, isbndb_api_key = None, ncbo_api_key = None, fda_api_key = None):
        self.chemspider_security_token = chemspider_security_token
        self.email = email
        self.umls_host = umls_host
        self.umls_user = umls_user
        self.umls_password = umls_password
        self.omim_api_key = omim_api_key
        self.openphacts_app_id = openphacts_app_id
        self.openphacts_app_key = openphacts_app_key
        self.umls_api_key = umls_api_key
        self.eol_api_key = eol_api_key
        self.dpla_api_key = dpla_api_key
        self.springer_api_key = springer_api_key
        self.elsevier_api_key = elsevier_api_key
        self.isbndb_api_key = isbndb_api_key
        self.ncbo_api_key = ncbo_api_key
        self.fda_api_key = fda_api_key
        
        self.umls_tgt = None
        
    # Return UMLS connection.
    #
    # This also retrieves a TGT just like below.
    @property
    def umls_connection(self):
        return connect_to_umls_db(host = self.umls_host, user = self.umls_user, password = self.umls_password, database_name = "umls", encoding = "latin1")
    
    # Basic user options for front-end application.
    def login(self):
        if self.user is None:
            print("USE DJANGO HERE.")
        
    def logout(self):
        print("USE DJANGO HERE.")
    
    # Return ticket-granting ticket.
    #
    # Note: you do not need a new TGT for each REST API call.
    # However, they expire after eight hours.
    #
    # Use this as guide:
    # https://github.com/HHS/uts-rest-api/blob/master/samples/python/Authentication.py
    def umls_tgt(user):
        url = "https://utslogin.nlm.nih.gov/cas/v1/api-key/"
        params = {'apikey': str(user.umls_api_key)}
        head = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "User-Agent": "python"
        }
        r = requests.post(url, data=params, headers=head)
        response = fromstring(r.text)
        tgt = response.xpath("//form/@action")[0]
        return tgt
    
    # Return single-use Service Ticket.
    def umls_st(umls_tgt):
        url = umls_tgt
        params = {"service": "http://umlsks.nlm.nih.gov"}
        head = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain",
            "User-Agent": "python"
        }
        r = requests.post(url, data=params, headers=head)
        st = r.text
        return st

#   UNIT TESTS
def user_unit_test():
    print("NOT FUNCTIONAL.")

#   MAIN
if __name__ == "__main__": main()