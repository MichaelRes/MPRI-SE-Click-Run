# -*- coding: utf-8 -*-
from . import state_engine
import pygame as pg
import sys
sys.path.append("..")
import score
from map import Map

class BestScore(state_engine.GameState):
    """
    The class for the best score state.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)

        self.best_score_map = Map()

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

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        if "MAP" in self.persist:
            self.best_score_map = self.persist["MAP"]
            self.best_score_map.update(5)
            self.persist["MAP"] = self.best_score_map
        else:
            self.best_score_map.update(5)
            self.persist["MAP"] = self.best_score_map

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()
        self.best_score_map.display(surface)
        text_color = 0, 0, 0
        for i, s in enumerate(score.ScoreManager().instance.scores):
            text = self.font.render(str(i+1) + " " + s.pseudo + " " + str(s.score), 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, (24 * (i + 1)) + 100))
        pg.display.flip()
