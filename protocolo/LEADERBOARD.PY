import os
import json

class Leaderboard():
    def __init__(self) -> None:
        if not os.path.exists('scores.json'):
            self.scores = {
            "IM_FLEXION_MET"  : [],
            "IM_EXTENSION_MET": [],
            "IM_FLEXION_PHA"  : [],
            "IM_EXTENSION_PHA": [],
            "IM_ADDUCTION_MET": [],
            "IM_ABDUCTION_MET": [],
            "IM_POINTING"     : [],
            "IM_FINGER_3"     : [],
            "IM_FINGER_2"     : [],
            "IM_MIDDLE_FINGER": [],
            "IM_RING_FINGER"  : [],
            "IM_PINKIE_FINGER": []
            }
            with open('scores.json', 'w') as file:
                json.dump(self.scores,file)
        else:
            with open('scores.json', 'r') as file:
                self.scores = json.load(file)

    def save(self):
        with open('scores.json', 'w') as file:
            json.dump(self.scores,file)
    
    def get_current_scores(self):
        return self.scores
    
    