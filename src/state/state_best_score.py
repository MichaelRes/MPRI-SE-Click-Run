# -*- coding: utf-8 -*-
from . import state_engine
import pygame as pg
import sys
sys.path.append("..")
import score

class BestScore(state_engine.GameState):
    """
    The class for the best score state.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)

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
        for i, s in enumerate(score.ScoreManager().instance.scores):
            text = self.font.render(str(i+1) + " " + s.pseudo + " " + str(s.score), 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, (24 * (i + 1))))
        pg.display.flip()
