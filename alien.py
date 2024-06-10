import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien/mouse in the fleet"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen


        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/mouse_alien.bmp')
        self.rect = self.image.get_rect()

        # Start a new a new Alien near the top left of hte screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the aliens exact horizontal position
        self.x = float(self.rect.x)
