# -*- coding: utf-8 -*-
from . import state_engine
import pygame as pg
from map import Map


class GameOver(state_engine.GameState):
    """
    The state for the game over.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)
        self.game_over_map = Map()

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
                self.restart_next_state = False
                self.done = True

            elif event.key == pg.K_RETURN:
                self.next_state = "GAME"
                self.restart_next_state = True
                self.done = True

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        if "MAP" in self.persist:
            self.game_over_map = self.persist["MAP"]
            self.game_over_map.update(5)
            self.persist["MAP"] = self.game_over_map
        else:
            self.game_over_map.update(5)
            self.persist["MAP"] = self.game_over_map

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()

        self.game_over_map.display(surface)
        text_color = 0, 0, 0

        text = self.font.render("GAME_OVER", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2))

        text = self.font.render("Press enter if you want to start a new game\n", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 24))

        text = self.font.render("Press escape if you want to go back to the main menu\n", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 48))

        pg.display.flip()
