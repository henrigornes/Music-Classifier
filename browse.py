from pathlib import Path
from mutagen import File
import re
from track import Track

class Browse :

    def __init__(self, chemin):
        self.dossier = chemin

    @property
    def dossier(self):
        return self._dossier
    @dossier.setter
    def dossier(self, chemin):
        self._dossier = Path(chemin)
        if not self._dossier.exists():
            raise ValueError(f"Le chemin {chemin} n'existe pas")
        if not self._dossier.is_dir():
            raise ValueError(f"Le chemin {chemin} n'est pas un répertoire")
    @property
    def fichiers(self):
        extensions_audio = {".mp3", ".wav", ".flac", ".m4a", ".aif", ".aiff"}
        liste =  [str(f.resolve()) for f in self.dossier.iterdir() if f.is_file() and f.suffix.lower() in extensions_audio]
        for f in self.sous_dossiers:
            liste.extend(f.fichiers)
        return liste

    @property
    def sous_dossiers(self):
        return [Browse(d) for d in self.dossier.iterdir() if d.is_dir()]
    @property
    def compteur(self):
        return len(self.fichiers)
    @property
    def tracks(self):
        return [self._track_fichier(f) for f in self.fichiers]
    
    def _track_fichier(self, chemin_fichier):
            artist = None 
            titre = None
            styles = None
            try: 
                audio = File(chemin_fichier)
                if audio is not None and audio.tags :
                    for cle_artist in ["artist", "TPE1", "©ART"]:
                        if cle_artist in audio.tags:
                            artist = str(audio.tags[cle_artist][0])
                            break
                    for cle_titre in ["title", "TIT2", "©nam"]:
                        if cle_titre in audio.tags:
                            titre = str(audio.tags[cle_titre][0])
                            break
                    for cle_genre in ["genre", "TCON", "©gen"]:
                        if cle_genre in audio.tags:
                            tag_genre = str(audio.tags[cle_genre][0])
                            if "/" in tag_genre:
                                styles = [s.strip() for s in tag_genre.split("/")]
                            else :
                                styles = [tag_genre.strip()]
                            break

            except Exception:
                pass

            if not artist or not titre:
                path_obj = Path(chemin_fichier)
                nom_nettoye = path_obj.stem
                nom_nettoye = re.sub(r"^([A-Z]\d|\d{1,2})[\.\s\-_]+", "", nom_nettoye, flags=re.IGNORECASE)

                if "-" in nom_nettoye:
                    parties = nom_nettoye.split("-", 1)
                    artist = artist or parties[0].strip()
                    titre = titre or parties[1].strip()
                else:
                    artist = artist or "Artiste Inconnu"
                    titre = titre or nom_nettoye.strip()
            track = Track(chemin=chemin_fichier, nom= titre, artiste=artist)
            if styles is not None:
                track.styles = styles
            return track