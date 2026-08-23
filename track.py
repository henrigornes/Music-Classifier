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
            return f"<Track: {self.nom} | Chemin: {self.chemin} | {self.bpm} BPM | Cle: {self.cle} | Groupe: {self.groupe} | Label: {self.label} | Styles: {', '.join(self.styles)} | Annee: {self.annee}>"   
        else:
            return f"<Track: {self.nom} (Non analysé)>"
    