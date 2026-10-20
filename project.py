import sys
from analyze import Analyze
from automixer import AutoMixer
from browse import Browse
from mix_harmonique import Mix_harmonique


def main():
    print("=== Auto-Mixer DJ (CS50P) V1.0 ===")
    dossier = input("Music Folder : ").strip()
    tolerance_bpm = 0.05
    try:
        tolerance_input = input(
            "Maximal BPM tolerance, press enter for default 5.0: "
        ).strip()
        if tolerance_input:
            tolerance_bpm = float(tolerance_input) / 100.0
    except (ValueError, EOFError):
        print("Invalid input, default tolerance used (5.0%).")
        tolerance_bpm = 0.05

    try:
        tracks = load_library(dossier)
        print(f"{len(tracks)} tracks loaded.")
        if len(tracks) < 2:
            print("You need at least 2 tracks for a mix.")
            return

        morceau_depart = tracks[0]
        print(f"\nSTARTER TRACK (Référence) :")
        print(
            f" -> {morceau_depart.artiste} - {morceau_depart.nom} "
            f"({morceau_depart.bpm} BPM, Clé: {morceau_depart.cle})"
        )

        print("\n--- Best Transitions ---")
        reco = automix(morceau_depart, tracks[1:], tolerance_bpm)
        if not reco:
            print(
                "None compatible transitions found (check the BPM or the"
                " keys)."
            )

        for track, score in reco:
            print(
                f" -> {track.artiste} - {track.nom} ({track.cle}) | Score :"
                f" {score * 100:.0f}%"
            )

    except Exception as e:
        print(f"Error : {e}")


def load_library(folder_path):
    nav = Browse(folder_path)
    tracks = nav.tracks
    analyzer = Analyze()
    for track in tracks:
        try:
            analyzer.analyze(track)
        except Exception as e:
            print(f"Analyze error for {track.nom} : {e}")
    return tracks


def compatibility_key(key1, key2):
    return Mix_harmonique(key1, key2)


def automix(track_actuelle, candidats, tolerance_bpm):
    mixer = AutoMixer(tolerance_bpm=tolerance_bpm)
    results = []
    for candidat in candidats:
        score, _ = mixer.transition(track_actuelle, candidat)
        if score is not None:
            results.append((candidat, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results


if __name__ == "__main__":
    main()