class Settings:
    """A class to store all settings for the Alien Invasion"""

    def __init__(self):
        """Initialise the game static settings to be used by other modules/main game"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (162, 210, 255)

        # Ship settings
        # Setting the number of ships/lives available
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (255, 175, 204)
        # Storing a number of bullets allowed in settings
        # This will then be used in the main game
        self.bullets_allowed = 3

        # Setting to control how quickly the fleet drops down
        self.fleet_drop_speed = 10

        # Increment game speeds up by
        self.speedup_scale = 1.1

        # point increase scale
        self.score_scale = 1.5

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        # Set the ship to an initial speed of 1.5 pixels, rather than 1 on each pass of hte loop
        self.ship_speed = 1.5
        # The bullet speed setting allows us to control the bullet speed as the game progresses
        self.bullet_speed = 2.5
        # Alien settings
        self.alien_speed = 1.0

        # Fleet direction - 1 is right, -1 is left to match x-axis coordinate behaviour
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)