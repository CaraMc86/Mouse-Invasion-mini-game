import pygame.font

class Scoreboard:
    """A class to report scoring infomration"""

    def __init__(self, ai_game):
        """Intialie scorekeeping attributes"""
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