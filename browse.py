from pathlib import Path

class browse :
    def __init__(self, chemin):
        self.dossier = chemin

    @property
    def dossier(self):
        return self._dossier
    @dossier.setter
    def dossier(self, chemin):
        self._dossier = Path(chemin)
        if not self._dossier.exists():
            raise ValueError(f"Le chemin {chemin} n'existe pas.")
        if not self._dossier.is_dir():
            raise ValueError(f"Le chemin {chemin} n'est pas un répertoire.")
    @property
    def fichiers(self):
        liste =  [str(f.resolve()) for f in self.dossier.iterdir() if f.is_file()]
        for f in self.sous_dossiers:
            liste.extend(f.fichiers)
        return liste

    @property
    def sous_dossiers(self):
        return [browse(d) for d in self.dossier.iterdir() if d.is_dir()]
    @property
    def compteur(self):
        return len(self.fichiers)
    

def main():
    path = input("Indiquez un répertoire : ")
    print(browse(path).fichiers)
   
if __name__ == "__main__":
    main()