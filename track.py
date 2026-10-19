from browse import browse
class track:
    def __init__(self, chemin, nom, artiste):
#browse class
        self.chemin = chemin
        self.nom = nom
        self.artiste = artiste
#Analyze class
        self.bpm = None
        self.cle = None
        self.vecteur = None
        self.groupe = None
#Discogs API
        self.label = None
        self.styles = []
        self.annee = None

    def __repr__(self):
        if self.bpm:
            styles_str = ", ".join(self.styles) if self.styles else "Inconnu"
            return (
                f"<Track: {self.nom} - {self.artiste} | {self.bpm} BPM | "
                f"Clé: {self.cle} | Label: {self.label or 'N/A'} | "
                f"Styles: {styles_str} | Année: {self.annee or 'N/A'}>"
            )
        return f"<Track: {self.nom} - {self.artiste} (Non analysé)>"