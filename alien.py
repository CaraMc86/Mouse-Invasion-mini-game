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

    # Each time we update the aliens position, move it to the right along the x-axis
    # by the amount stored in alien_speed
    def update(self):
        """Move Alien to the right"""
        # Track the aliens position with the self.x attribute that can hold float values
        self.x += self.settings.alien_speed
        # Then use the value of self.x to update the position of the aliens rect(angle)
        self.rect.x = self.x
