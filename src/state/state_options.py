# -*- coding: utf-8 -*-
from state_engine import GameState
import pygame as pg


class Options(GameState):
    """
    The class for the options state.
    """
    def __init__(self):
        """
        @rtype: None
        """
        GameState.__init__(self)

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
                self.done = True

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()

        surface.fill(pg.Color("black"))
        text_color = 255, 255, 255

        text = self.font.render("METTRE LES OPTIONS ICI", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2))
        pg.display.flip()
