import json
import requests
import pprint
import ssp
from ssp_device import ssp_device



class rest_api():
    def __init__(self):
        None
    def post(self):
        note_info = ssp_device.note_info
        URL = 'http://localhost:52639/api/values/'
        DATA = note_info
        requests.post(url = URL, data = DATA)
        