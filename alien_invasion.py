import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
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
        # Creating a group to hold the bullets in __init__()
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            # Calls the ship update method from ship.py on each pass of the loop
            # This allows the key right to work
            self.ship.update()
            # update the position of hte bullets on each pass of the while loop
            # When you call update() on a group - as initialized above - the group automatically
            # calls update() for *each* sprite in the group
            self._update_bullet()
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
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.K_SPACE:
                self._fire_bullet()


    # Created new helper methods to split away the keyup/down logic from the _check_events helper method.
    # Then add keydown logic to quit pressing the key q (K_q)
    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        # Calls the _fire_bullet method when space bar is called.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and add to the bullets group"""
        # conditional statement to check if anotehr bullet can be released
        if len(self.bullets) < self.settings.bullets_allowed:
            # makes a new instance of Bullet and call it new_bullet
            new_bullet = Bullet(self)
            # add this bullet to the bullets group - initialised above
            self.bullets.add(new_bullet)

    def _update_bullet(self):
        """Update position of bullets & get rid of old bullets"""
        self.bullets.update()

        # Get rid of bullets that have dissapeared off-screen - to ensure no uneccessary memory is used as the bullets continue off screen.
        # Pygame expects a list or group to remain the same length as log as the loop is running.
        # We use the copy method to coop over a copy of this, meaning we can then delete items from the main group as we are always
        # looping over a copy.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_colour)
        # For loop to include drawing the bullet on each screen redraw
        for bullet in self.bullets.sprites():
            # For each pass of the loop, call the draw bullet method from bullet.py
            bullet.draw_bullet()
        # draw the ship at its current location
        self.ship.blitme()
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()