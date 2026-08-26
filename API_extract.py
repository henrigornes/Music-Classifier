import os
import requests
from dotenv import load_dotenv

class DiscogsAPI:
    URL = "https://api.discogs.com"
    
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data
