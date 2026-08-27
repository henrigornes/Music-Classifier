import os
import requests
from dotenv import load_dotenv


# Charge les variables du fichier .env
load_dotenv()

class ApiService:
    def __init__(self):
        self.api_key = os.getenv("DISCOGS_API_KEY")
        if not self.api_key:
            raise ValueError("DISCOGS_API_KEY est introuvable dans le .env !")
        self.headers = {"Authorization": f"Discogs token={self.api_key}","User-Agent": "CS50PMusicApp/1.0"}