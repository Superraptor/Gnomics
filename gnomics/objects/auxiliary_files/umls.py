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
#   Perform UMLS operations.
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

#   Other imports.
import json
import requests
import time

#   MAIN
def main():
    umls_unit_tests()

#   Perform crosswalking operation.
def umls_crosswalk(user, from_source, to_source, source_id, other="id", verbose=False):
    
    found_array = []
    
    if user is None:
        print("A valid user object with a valid UMLS API key is required for this function.")
        return found_array
    elif user.umls_api_key is None:
        print("A valid UMLS API key associated with the user object is required for this function.")
        return found_array
    
    umls_tgt = User.umls_tgt(user)
    page_num = 0
    base = "https://uts-ws.nlm.nih.gov/rest"
    ext = "/crosswalk/current/source/" + from_source.upper() + "/" + source_id
    
    verbose = True

    while True:
        tick = User.umls_st(umls_tgt)
        page_num += 1
        query = {"ticket": tick, "pageNumber": page_num}
        try:
            r = requests.get(base+ext, params=query, headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"})
            r.encoding = 'utf-8'
            
            try:
                items = json.loads(r.text)
                json_data = items["result"]
                empty = False
                for rep in json_data:
                    if other == "id":
                        if rep["ui"] not in found_array and rep["ui"] != "NONE":
                            if rep["rootSource"] == to_source.upper():
                                found_array.append(rep["ui"])
                    elif other == "name":
                        if (rep["name"] not in found_array and rep["name"] != "NONE") and (rep["ui"] not in found_array and rep["ui"] != "NONE"):
                            if rep["rootSource"] == to_source.upper():
                                found_array.append((rep["ui"], rep["name"]))
                    else:
                        print("This value for 'other' is not currently supported.")

                    if "results" in json_data:
                        if json_data["results"][0]["ui"] == "NONE":
                            empty = True
                            break

                if not json_data:
                    break
                elif empty:
                    break
            except ValueError as e:
                if verbose:
                    print("A value error occurred while attempting to load resulting JSON.")
                    print("ERROR: %s" % str(e))
                break
            except:
                if verbose:
                    print("Some other unknown error occurred.")
                break
            else:
                continue
            
        except ConnectionError as e:
            if verbose:
                print("A connection error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except requests.exceptions.ConnectionError as e:
            if verbose:
                print("A connection error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except HTTPException as e:
            if verbose:
                print("An HTTP exception error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except ProtocolError as e:
            if verbose:
                print("A protocol error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except urllib3.exceptions.ProtocolError as e:
            if verbose:
                print("A protocol error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except SysCallError as e:
            if verbose:
                print("A system call error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except OpenSSL.SSL.SysCallError as e:
            if verbose:
                print("A system call error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except ssl.SSLError as e:
            if verbose:
                print("A system call error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except SSLError as e:
            if verbose:
                print("A SSL error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except requests.exceptions.SSLError as e:
            if verbose:
                print("A SSL error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except BadStatusLine as e:
            if verbose:
                print("A bad status line error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except httplib.BadStatusLine as e:
            if verbose:
                print("A bad status line error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except http.client.BadStatusLine as e:
            if verbose:
                print("A protocol error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except MaxRetryError as e:
            if verbose:
                print("A max retry error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except urllib3.exceptions.MaxRetryError as e:
            if verbose:
                print("A max retry error occurred while attempting request.")
                print("ERROR: %s" % str(e))
            break
        except:
            print("Some other HTTP/URL error encountered.")
            break
        else:
            break
    
    return found_array
    
#   UNIT TESTS
def umls_unit_tests():
    print("NOT FUNCTIONAL.")
    
#   MAIN
if __name__ == "__main__": main()