import pygame
from pygame.sprite import Sprite

# to display the ships remaining as an image, we need to import Sprite and pass this into the Ship class
# to ensure the class inherits from Sprite
class Ship(Sprite):
    """A Class to manage the ship"""

    # Initialised with 'self' and ai_game, which names the 'ai' argument passed from AlienInvasion
    def __init__(self, ai_game):
        """Initialise the ship and its starting position"""
        super().__init__()  # Initialize the Sprite base class
        # Access screen & settings from the AlienInvasion instance passed as 'ai_game'
        self.screen = ai_game.screen
        # Create a settings attribute for Ship() so we can use it in the update() method
        self.settings = ai_game.settings
        # Pygame treats objects as rectangles which makes it easier to determine when they have collided - called rect()
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect (rectangle dimensions and position)
        self.image = pygame.image.load('images/kitty.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom centre of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float  for the ships exact horizontal position - as we are moving fraction of a pixel,
        # we have to assign to a variable as rect x (axis) attributes only stores integer values and then
        # convert into float and assign this value back to self.x

        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ships position base on the movement flag. When we change the ships position in update,
        the value of self.x is adjusted by the amount stored in settings (1.5x here).
         After self.x has been updated, we use the new value to update self.rect.x which controls the position
         of the ship"""
        # Adding 2 parameters for the if statement to check
        # Right: checks the ship is moving right and that the current position is less than the screen value on the right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Left: checks the ship is moving left and is greater than 0 - the starting point of the x axis
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update rect object from self.x
        # Only the integer portion of self.x will be assigned to self.rect.x, but thats ok for display purposes
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship after it is hit and a new fleet populated"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw th ship at its current location"""
        self.screen.blit(self.image, self.rect)