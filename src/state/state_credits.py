# -*- coding: utf-8 -*-
from . import state_engine
import pygame as pg
from map import Map


class Credits(state_engine.GameState):
    """
    The classe for the credits state.
    """
    def __init__(self):
        state_engine.GameState.__init__(self)
        self.credits_map = Map()

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
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
            self.credits_map = self.persist["MAP"]
            self.credits_map.update(5)
            self.persist["MAP"] = self.credits_map
        else:
            self.credits_map.update(5)
            self.persist["MAP"] = self.credits_map

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()

        self.credits_map.display(surface)
        text_color = 0, 0, 0

        lines = ["Software Egineering - ENS Cachan - MPRI", "Project : Click & Run", "Dang-Nhu Hector - Marotte Joseph - Lalanne Clément"]

        for i, line in enumerate(lines):
            text_color = 0, 0, 0
            text = self.font.render(line, 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, i*100 + 100))

        pg.display.flip()
