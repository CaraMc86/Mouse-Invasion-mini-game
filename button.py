# this import allows us to render text on the game screen
import pygame.font

class Button:
    """A class t build game buttons"""

    # Initialisation method takes self, ai_game object and msg - which contains the buttons text
    def __init__(self, ai_game, msg):
        """Initialise button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set button dimensions
        self.width, self.height = 200, 50
        self.button_colour = (255, 200, 221)
        self.text_colour = (255, 255, 255)
        # None argument tells Pygame to use the default font. 48 is the text size
        self.font = pygame.font.SysFont(None, 48)

        # Built button's rect object and centre it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Button message only needs to be prepped once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_img = self.font.render(msg, True, self.text_colour,
                                          self.button_colour)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)