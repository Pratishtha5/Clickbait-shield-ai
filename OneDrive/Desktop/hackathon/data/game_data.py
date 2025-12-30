# data/game_data.py

class GameData:
    def __init__(self):
        # progression
        self.current_level = 0

        # AI-observed stats
        self.stats = {
            "learning_speed": 0,
            "empathy": 0,
            "logic_bias": 0,
            "obedience": 0
        }

    # ---- logging actions ----
    def log(self, key):
        if key in self.stats:
            self.stats[key] += 1

    # ---- queries ----
    def dominant_trait(self):
        return max(self.stats, key=self.stats.get)

    def summary(self):
        return self.stats.copy()
