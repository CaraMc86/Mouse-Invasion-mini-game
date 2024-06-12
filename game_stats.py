class GameStats:
    """Track the statistics for cat and mouse game"""

    # Make one GameStats instance the whole time the game is running, but will need to reset some stats each time a new game is played
    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

    # Initialise most of the stats in reset_stats rather than directly in def __init__()
    # Reset_stats is called on initialisation so the stats are set properly when the GameStats is first intialised on a new game
    def reset_stats(self):
        """Initialise statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        # Score set to 0
        self.score = 0
        self.level = 1
        # High score - this should never be reset so initilaised in __init__
        self.high_score = 0