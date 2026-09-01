import os
import requests 



class ApiService:
    def __init__(self):
        self.api_key = os.getenv("DISCOGS_API_KEY")
        if not self.api_key:
            raise ValueError("La variable d'environnement DISCOGS_API_KEY n'est pas définie !")
        self.headers = {"Authorization": f"Discogs token={self.api_key}","User-Agent": "ApplicationHarmonique/1.0 (contact: henri.gornes@gmail.com)"}