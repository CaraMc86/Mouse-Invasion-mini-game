class Settings:
    """A class to store all settings for the Alien Invasion"""

    def __init__(self):
        """Initialise the game settings to be used by other modules/main game"""
        # Screen settings
        self.screen_with = 1200
        self.screen_height = 800
        self.bg_colour = (162, 210, 255)
        # Ship settings
        # Set the ship to an initial speed of 1.5 pixels, rather than 1 on each pass of hte loop
        self.ship_speed = 1.5
        # Bullet settings
        # The bullet speed setting allows us to control the bullet speed as the game progresses
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (255, 175, 204)
