import numpy as np 
from track import track 
from mix_harmonique import mix_harmonique
class AutoMixer:
    def __init__(self, poids_style: float = 0.6, poids_energie: float = 0.4, tolerance_bpm: float = 0.05,):
        total = poids_style + poids_energie
        if total != 1.0:
            poids_style = poids_style / total
            poids_energie = poids_energie / total


        self.poids_style = poids_style
        self.poids_energie = poids_energie
        self.tolerance_bpm = tolerance_bpm
    def _score_styles(self, track1, track2) :
        if not track1.styles or not track2.styles:
            return 0.5
        set1 = set(s.lower() for s in track1.styles)
        set2 = set(s.lower() for s in track2.styles)
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection)/len(union) if union else 0.0

    def _score_energie(self, track1, track2):
        if track1.vecteur is None or track2.vecteur is None:
            return 0.5
        v1 = np.array(track1.vecteur)
        v2 = np.array(track2.vecteur)
        dist = np.linalg.norm(v2 -v1)
        return float(1/(1+dist))
    
    def transition(self, track_actuelle, candidat):
        if track_actuelle.bpm and candidat.bpm:
            ecart_bpm = (abs(track_actuelle.bpm - candidat.bpm)/track_actuelle.bpm)
            if ecart_bpm > self.tolerance_bpm:
                return None
        if not mix_harmonique(track_actuelle.cle, candidat.cle):
            return None
        
        score_styles = self._score_styles(track_actuelle, candidat)
        score_energie = self._score_energie(track_actuelle, candidat)
        score_final = (score_styles*self.poids_style) + (score_energie*self.poids_energie)
        return round(score_final, 2)


