import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien/mouse in the fleet"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        # access settings.py to access the aliens speed
        self.settings = ai_game.settings
        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/mouse_alien.bmp')
        self.rect = self.image.get_rect()
        # Start a new Alien near the top left of hte screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the aliens exact horizontal position
        self.x = float(self.rect.x)

    # Alien is att he right edge if the right attricute of its rect is >= to the screen right rect attribute
    # Alien is at the left edge if the value is <= 0
    # This is put directly into a return statement rather than use if/else block so it retruns a boolean value
    def check_edges(self):
        """Return True if the alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    # Each time we update the aliens position, move it to the right along the x-axis
    # by the amount stored in alien_speed
    def update(self):
        """Move Alien to the right or left"""
        # Track the aliens position with the self.x attribute that can hold float values
        # By multiplying by the fleet direction we can modify whether it is right or left using -1 or 1
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        # Then use the value of self.x to update the position of the aliens rect(angle)
        self.rect.x = self.x
