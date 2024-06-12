import pygame.font

class Scoreboard:
    """A class to report scoring infomration"""

    def __init__(self, ai_game):
        """Intialie scorekeeping attributes"""
        self.screen = ai_game.screen
        self.rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font setting for scoring infomration
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial score image
        self.prep_score()

    def prep_score(self):
        """Turn the score into a rendered image"""
        # Turn stats into a string - calling the variable holding the string score_str
        score_str = str(self.stats.score)
        # This string is then passed to render() creating the image.
        # We pass the screen background colour and text colour above so we can see the text clearly
        self.score_image = self.font.render(score_str, True,
                                            self.text_colour, self.settings.bg_colour)
        # Display the score at the top right hand side of the screen - This will exapnd as the score increases
        # Create score_rect and pass it score image to position it
        self.score_rect = self.score_image.get_rect()
        # Set its right edge to 20 pixels from the right edge
        self.score_image.right = self.screen_rect.right - 20
        # Place the top edge 2 pixels from the top
        self.score_rect.top = 20

    def show_score(self):
        """Draw the scoreboard to the screen"""
        self.screen.blit(self.score_image, self.score_rect)