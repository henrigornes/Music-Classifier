from pathlib import Path
class browse :
    def __init__(self, chemin):
        self.dossier = Path(chemin)

    def fichiers(self):
        if self.dossier.exists() and self.dossier.is_dir():
            return [f.name for f in self.dossier.iterdir() if f.is_file()]
        return []

    def compteur(self):
        return len(self.fichiers())

def main():
    chemin = browse(input("Chemin des fichiers"))
    
if __name__ == "__main__":
    main()