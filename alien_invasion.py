import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
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
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Create instance to store the game statistics
        # This needs to be after the surface/display settings but before the game elements.
        self.stats = GameStats(self)

        # Create instance of Scoreboard to render the stats
        self.sb = Scoreboard(self)
        # Instance of ship created from imported Ship module
        # This passes the instance of AlienInvasion (ai) as self to the ship class.
        self.ship = Ship(self)
        # Creating a group to hold the bullets in __init__()
        self.bullets = pygame.sprite.Group()
        # Creating group to hold the fleet of Aliens/Mice
        self.aliens = pygame.sprite.Group()
        # We then the create fleet method.
        self._create_fleet()
        # Start game in an inactive state - so we can add a play game button to start gameplay
        self.game_active = False
        self._play_button = Button(self, "Play!")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            # runs whilst there are lives left
            if self.game_active:
            # Calls the ship update method from ship.py on each pass of the loop
            # This allows the key right to work
                self.ship.update()
                # update the position of hte bullets on each pass of the while loop
                # When you call update() on a group - as initialized above - the group automatically
                # calls update() for *each* sprite in the group
                self._update_bullet()
                # Call to update alien position in main while loop - after the bullet call to match the order of methods
                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the play button is clicked"""
        button_clicked = self._play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics, settings and set the game to active
            self.settings.initialise_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True
            # Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Hide mousebutton cursor
            pygame.mouse.set_visible(False)

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
        # conditional statement to check if another bullet can be released
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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Check for any aliens hit by bullets, if true get rid of bullet & Alien
        # Whenever the rect(angles) of bullet and alien overlap, group collide() adds a key value pair to the dictionary it returns
        # 2 true arguments tells Pygame to delete the bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        # condition to check if the aliens group is empty.
        # An empty group is False, if it is we empty the bullets and call _create_fleet
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()



    # Method coordinates response when a ship hits the mouse
    def _ship_hit(self):
        """respond to a ship being hit by an Alien"""
        # Decrement ships left by 1
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            # Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create new fleet
            self._create_fleet()
            self.ship.center_ship()
            # Pause - using the newly imported sleep module
            sleep(0.5)
        else:
            self.game_active = False

    def _check_alien_bottom(self):
        """Check if an alien hits the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # The same gode as being hit
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update position of all Aliens in the fleet"""
        # Check if the fleet is at an edge, then update positions
        self._check_fleet_edges()
        # Call the update method on the aliens group
        self.aliens.update()

        # Look for mouse/cat collisions
        # spritecollideany() takes 2 arguments, a sprite and a group.
        # It looks for any member of the group that collides with the main sprite
        # This function acts as a loop returning None if ther are no collisions, only
        # performing an action if there is a collision or alien hits the bottom
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_alien_bottom()

    def _create_fleet(self):
        """Make a fleet of aliens from the instance"""
        # Make one instance of an Alien and add it to the group initialised above until there is no more room left
        # Make the gap between 1 mouse alien, 1 mouse alien long
        alien = Alien(self)
        # We need to know the Aliens height to place the rows, so we use rect's size attribute to grab the height and width of the alien
        alien_width, alien_height = alien.rect.size

        # Next set the initial height and width for placement of the first alien
        current_x, current_y = alien_width, alien_height
        # Outer while loop, controlling how many rows can be place - we have opted for 3.
        # This will continue to allow the inner while loop to add rows as long as it is the screen height less 3 * the aliens' height.
        while current_y < (self.settings.screen_height - 3 * alien_height):
        # Inner while loop ensuring the loop runs whilst there are the screen width less 2 x alien width
        # This will allow the last alien + gap to be present when adding aliens in a row
            while current_x < (self.settings.screen_width - 2 * alien_width):
                # Call the _create_alien method passing both current x and y positions
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create a new alien and place it in a row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond if any aliens hit an edge"""
        # Loop through the fleet and call _check_edges on each alien
        # If returns tru
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and fleet direction"""
        # Loop through each alien and drop each one, one by one using fleet_drop_speed
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            # We then change the direction by multiplying by -1
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_colour)
        # For loop to include drawing the bullet on each screen redraw
        for bullet in self.bullets.sprites():
            # For each pass of the loop, call the draw bullet method from bullet.py
            bullet.draw_bullet()
        # draw the ship at its current location
        self.ship.blitme()
        # To mke the alien appear we need to call the groups draw() function
        # When you call draw on a group, Pygame draws each element based on
        # its position defined by its rect attribute.
        self.aliens.draw(self.screen)
        # Draw the score infomration - just before we call the draw play button
        self.sb.show_score()
        # Draw the play button if the game is inactive
        if not self.game_active:
            self._play_button.draw_button()
        # Make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()