import os
import sys
# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)
import requests


class IracingClient(object):
    def __init__(self, address='127.0.0.1'):
        self.address = address

    def standings(self):
        address = "http://{}/standings".format(self.address)
        result = requests.get(address)
        return result.json()

    def session_status(self):
        address = "http://{}/session_status".format(self.address)
        result = requests.get(address)
        return result.json()
