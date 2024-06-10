import pygame
from pygame.sprite import Sprite

# The Bullet class inherits from Spite - imported from pygame
# when you use sprites, you can group related elements in your game and act on the grouped elements at once
class Bullet(Sprite):
    """A class to manage bullets fired from cat/ship"""
    def __init__(self, ai_game):
        """Create a bullet object at the ships current position"""
        # To create a bullet instance, we need the current instance of AlienInvasion,
        # and we call Super() to inherit the properties from Sprite
        super().__init__()
        # Set attributes for the screen, settings and bullet colour
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.colour = self.settings.bullet_colour

        # Create a bullet at rect (0, 0) and then set correct position
        # We are not importing the bullet from an image, so we create using the inbuilt pygame.Rect() class
        # This is initialised at 0,0
        # On the next line, this is moved dependent on the ships positioning from the values stored in self.settings
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        # Here we set the bullets midtop attribute to match the ships midtop attribute
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullets position as a float to make fine adjustments to the bullets speed
        self.y = float(self.rect.y)

    # The update method manages the bullets position
    # Once a bullet is fired, the x-axis does not change, only the position along the y-axis
    # This means it will always move in a straight line
    def update(self):
        """Move the bullet up the screen"""
        # Update the exact position of the bullet
        # When fired, it moves up the screen, corresponding to re decreasing y-coordinate value
        self.y -= self.settings.bullet_speed
        # Update the rect position by using the value of self.y
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullets on the screen"""
        # When we want to draw a bullet, we can now call the draw_bullet() method
        # The draw rect function fills the part with the screen defined by the bullets rect(angle)
        # with the colour stored in self.colour (which is held in settings.py)
        pygame.draw.rect(self.screen, self.colour, self.rect)