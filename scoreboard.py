import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring infomration"""

    def __init__(self, ai_game):
        """Intialie scorekeeping attributes"""
        # We assign the game instance to an attribute, because we'll need to crete some ships
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font setting for scoring infomration
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)

        self.level_image = self.font.render(level_str, True,
                                            self.text_colour, self.settings.bg_colour)

        # position below the score:
        self.level_rect = self.level_image.get_rect()
        # First sets this to the right hand position to match score
        self.level_rect.right = self.score_rect.right
        # Then to the bottom of the score by 10 pixels
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        # creates an empty group to hold ship instances
        self.ships = Group()
        # The for loop fills the group with the number of ships the player has left
        for ship_number in range(self.stats.ships_left):
            # Inside the loop a new ship is created and set to each ship's x-coordinate value
            # This is so they appear next to each other with a 10 pixel maargin on the left side
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            # We set the y value to 10 pixels down from the top of the screen, so is in ine with the other scores
            ship.rect.y = 10
            # This line adds the ships to the line-up
            self.ships.add(ship)

    def prep_score(self):
        """Turn the score into a rendered image"""
        # To round the score to the nearest 10 value we create variable rounded_score
        # when you pass a negiative argument in round() it will round to the nearest 10,100 etc
        rounded_score = round(self.stats.score, -1)
        # This is a specific f string that takes the variable in curly braces and tells it to add a comma
        score_str = f'{rounded_score:,}'
        # This string is then passed to render() creating the image.
        # We pass the screen background colour and text colour above so we can see the text clearly
        self.score_image = self.font.render(score_str, True,
                                            self.text_colour, self.settings.bg_colour)
        # Display the score at the top right hand side of the screen - This will exapnd as the score increases
        # Create score_rect and pass it score image to position it
        self.score_rect = self.score_image.get_rect()
        # Set its right edge to 20 pixels from the right edge
        self.score_rect.right = self.screen_rect.right - 20
        # Place the top edge 2 pixels from the top
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image and center on the top of the page"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f'{high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_colour, self.settings.bg_colour)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw the scoreboard to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # We use draw() in this line as we are displaying ship images, not numbers
        self.ships.draw(self.screen)