import librosa
import numpy as np
from track import track
class Analyze:
    def obtenir_cle(self, y, sr):
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_mean = chroma.mean(axis=1)
#Krumhansl-Schmuckler
        majeur = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        mineur = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 2.69, 3.34, 3.17, 3.28])
        camelot_majeur = ["8B", "3B", "10B", "5B", "12B", "7B", "2B", "9B", "4B", "11B", "6B", "1B"]
        camelot_mineur = ["5A", "12A", "7A", "2A", "9A", "4A", "11A", "6A", "1A", "8A", "3A", "10A"]
        best_correlation = -1
        cle_trouvee = None
        for i in range(12):
            chroma_decale = np.roll(chroma_mean, -i)
            corr_majeur = np.corrcoef(chroma_decale, majeur)[0, 1]
            if corr_majeur > best_correlation:
                best_correlation = corr_majeur
                cle_trouvee = camelot_majeur[i] 

            corr_mineur = np.corrcoef(chroma_decale, mineur)[0, 1]
            if corr_mineur > best_correlation:
                best_correlation = corr_mineur
                cle_trouvee = camelot_mineur[i]
        return cle_trouvee
    
    def analyze(self, track: track):
        path = track.chemin
        y, sr = librosa.load(path, offset = 60, duration= 60)
        # Perform analysis on the loaded audio file
        bpm = librosa.feature.tempo(y=y, sr=sr)
        # Store the analysis results in the track object
        track.bpm = round(float(bpm[0]), 1)
        track.cle = self.obtenir_cle(y, sr)

        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        track.vecteur = np.hstack([mfcc.mean(axis=1), mfcc.std(axis=1), cent.mean(), cent.std(), rolloff.mean(), rolloff.std(), zcr.mean(), zcr.std(), float(bpm[0])]).tolist()
