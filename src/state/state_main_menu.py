# -*- coding: utf-8 -*-
import sys
import pygame as pg
from state_engine import GameState
from map import Map
sys.path.append("..")


class MainMenu(GameState):
    """
    The state for the main menu.
    """
    def __init__(self):
        """
        @rtype: None
        """
        GameState.__init__(self)
        self.available_state = ["GAME", "BEST_SCORE", "OPTIONS", "CREDITS"]
        self.current_select = 0
        self.next_state = None
        self.restart_next_state = True
        self.main_menu_map = Map()

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.current_select = (self.current_select - 1) % len(self.available_state)
            elif event.key == pg.K_DOWN:
                self.current_select = (self.current_select + 1) % len(self.available_state)
            elif event.key == pg.K_RETURN:
                self.next_state = self.available_state[self.current_select]
                self.done = True

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        self.main_menu_map.update(5)

    def draw(self, surface):
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()
        self.main_menu_map.display(surface)
        for i, name_state in enumerate(self.available_state):
            if i == self.current_select:
                text_color = 255, 0, 0
            else:
                text_color = 255, 255, 255
            text = self.font.render(name_state, 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, i*100))
        pg.display.flip()
