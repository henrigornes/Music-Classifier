import numpy as np 
from track import Track 
from mix_harmonique import Mix_harmonique
from sklearn.metrics.pairwise import cosine_similarity

class AutoMixer:

# Ordres de grandeur pour équilibrer les 33 dimensions du vecteur :
# 13 MFCC mean (~100), 13 MFCC std (~50),
# centroid_mean (~2500), centroid_std (~1000),
# rolloff_mean (~5000), rolloff_std (~2000),
# zcr_mean (~0.1), zcr_std (~0.05), tempo (~120)

    SCALES = np.array([100.0] * 13 + [50.0] * 13 + [2500.0, 1000.0, 5000.0, 2000.0, 0.1, 0.05, 120.0])

    def __init__(self, poids_style: float = 0.6, poids_energie: float = 0.4, tolerance_bpm: float = 0.05,):
        total = poids_style + poids_energie
        if total >0 :
            self.poids_style = poids_style / total
            self.poids_energie = poids_energie / total
        else :
            self.poids_style = 0.5
            self.poids_energie = 0.5
        
        self.tolerance_bpm = tolerance_bpm

    def _score_styles(self, track1, track2) :
        if not track1.styles or not track2.styles:
            return None

        set1 = set(s.lower() for s in track1.styles)
        set2 = set(s.lower() for s in track2.styles)
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        if union:
            return len(intersection)/len(union) 
        else:
            return 0.0

    def _score_energie(self, track1, track2):

        if track1.vecteur is None or track2.vecteur is None:
            return 0.5

        v1 = np.array(track1.vecteur, dtype = float)
        v2 = np.array(track2.vecteur, dtype = float)
        #A revoir pour la suite 
        dist = np.linalg.norm(v2 -v1)
        return float(1/(1+dist))
    
    def transition(self, track_actuelle, candidat):

        if track_actuelle.bpm and candidat.bpm:

            ecart_bpm = (abs(track_actuelle.bpm - candidat.bpm)/track_actuelle.bpm)

            if ecart_bpm > self.tolerance_bpm:

                return None, "BPM unmatch"

        if not Mix_harmonique(track_actuelle.cle, candidat.cle):

            return None, "key unmatch"
        
        score_styles = self._score_styles(track_actuelle, candidat)
        score_energie = self._score_energie(track_actuelle, candidat)
        score_final = (score_styles*self.poids_style) + (score_energie*self.poids_energie)
        return round(score_final, 2), "Valid"