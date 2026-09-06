import os
import requests 



class ApiService:
    def __init__(self):
        self.api_key = os.getenv("DISCOGS_API_KEY")
        if not self.api_key:
            raise ValueError("La variable d'environnement DISCOGS_API_KEY n'est pas définie !")
        self.headers = {"Authorization": f"Discogs token={self.api_key}","User-Agent": "ApplicationHarmonique/1.0 (contact: henri.gornes@gmail.com)"}
        self.base_url = "https://api.discogs.com"

    def search_release(self, artist:str, title:str)-> dict | None:
        url = f"{self.base_url}/database/search"
        params = {"artist": artist, "track": title, "type": "release"}
        try: 
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                return data["results"][0]
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête API : {e}")
            return None

