# Based on this:
# https://github.com/fyears/electron-python-example

from __future__ import print_function
import json
import master_ctrl
import sys
import threading
import time
import zerorpc
import zmq

class GnomicsApi(object):
    
    def echo(self, text):
        """
            Used to test whether server is ready.
        """
        
        return text
    
    def search(self, text):
        search_results = master_ctrl.search(text['search_query'], search_type = text['search_type'], user = text['user'])
        return search_results
    
    def identifiers(self, text):
        identifier_results = master_ctrl.identifiers(text['identifier'], text['identifier_type'], text['object_type'], text['language'], text['source'], user = text['user'])
        #print(identifier_results)
        return identifier_results
    
    def interactions(self, text):
        interaction_results = master_ctrl.interaction_objects(text['identifier'], text['identifier_type'], text['object_type'], user = text['user'])
        print(interaction_results)
        return interaction_results
        
    def properties(self, text):
        property_results = master_ctrl.properties(text['identifier'], text['identifier_type'], text['object_type'], user = text['user'])
        return property_results        
    
def parse_port():
    return 4242

def main():
    
    # Might have to kill current process to get this to run...
    # First, open a Windows command line.
    # Then run `netstat -a -o -n`.
    # Find the PID(s) for the Local Address 'tcp://127.0.0.1:4242'.
    # Terminate those PID(s) by running:
    # `taskkill /F /PID $PID` where $PID is the PID.
    # For example, if the PID is 20284, run:
    # `taskkill /F /PID $PID` where $PID is the PID.
    
    addr = "tcp://127.0.0.1:" + str(parse_port())
    s = zerorpc.Server(GnomicsApi(), heartbeat=None)
    s.bind(addr)
    print("Start running on {}".format(addr))
    s.run()
    
    
if __name__ == "__main__":
    main()