import sys
from analyze import Analyze
from API_extract import ApiService
from automixer import AutoMixer
from browse import browse
from mix_harmonique import mix_harmonique

def main():
    print("=== Auto-Mixer DJ (CS50P) V1.0 ===")
    dossier = input("Music Folder : ").strip()
    try :
        tolerance_input = input("Maximal BPM tolerance, press enter for the default value 5.0")
        tolerance_bpm = (float(tolerance_input if tolerance_input else 5.0))
    except ValueError:
        tolerance_bpm = 5.0
        
    try :
        tracks = load_library(dossier)
        print(f"{len(tracks)} morceaux chargés.")
        if len(tracks)<2:
            print("You need at least 2 tracks for a mix.")
            return 
        

def load_library(folder_path):
    nav = browse(folder_path)
    return nav.tracks

def compatibility_key(key1, key2):
    return mix_harmonique(key1, key2)

def automix(track_actuelle, candidats):
    mixer = AutoMixer()
    results = []
    for candidat in candidats :
        score, _ = mixer.transition(track_actuelle, candidat)
        if score is not None :
            results.append((candidat, score))
    results.sort(key = lambda x : x[1], reverse = True)
    return results




