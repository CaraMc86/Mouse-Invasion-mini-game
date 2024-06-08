import sys
import pygame
from settings import Settings
from ship import Ship
class AlienInvasion:
    """Overall Class to manage game assets and behaviour"""
    def __init__(self):
        """Initialise the game and create game resources"""
        pygame.init()
        # make a clock that ticks once on each pass to help ensure the game runs at the same frame rate on all systems
        self.clock = pygame.time.Clock()
        # assign the Settings module to the self.settings instance variable
        self.settings = Settings()

        # Create the game surface, where the game element is displayed.
        # The dimensions and background color are defined in the Settings module.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_with, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        # Instance of ship created from imported Ship module
        # This passes the instance of AlienInvasion (ai) as self to the ship class.
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            #Calls the ship update method from ship.py on each pass of the loop
            # This allows te key right to work
            self.ship.update()
            self._update_screen()
            # Use the clock to ensure the game runs at the same frame rate on all systems.
            # The argument 60 tells pygame to (try to) run the game loop 60 times per second.
            self.clock.tick(60)

    """Helper methods, to work as part of the run game method, but moved outside to break up the code"""
    def _check_events(self):
        # Watch for keyboard and mouse events.
        # pygame.event.get() returns a list of events that have occurred since the last time it was called.
        # Any keyboard or mouse event will trigger this for loop to run.
        for event in pygame.event.get():
            # Inside the for loop we write if statements to detect and respond to specific events
            # In this example, if the windows close button is pressed, pygame.QUIT event is detected and we call sys.exit() to eit hte game.
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_colour)
        # draw the ship at its current location
        self.ship.blitme()
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()