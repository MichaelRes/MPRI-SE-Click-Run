# -*- coding: utf-8 -*-
from . import state_engine
import pygame as pg
import pickle
from map import Map


class Options(state_engine.GameState):
    """
    The class for the options state.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)
        self.current_select = 0
        self.all_opts = {"CHARACTER": ["mario", "toad"],
                         }
        self.current_opts = {"CHARACTER": 0,
                             }
        self.available_opts = list(self.all_opts)
        self.available_opts.sort()
        self.options_map = Map()

    def write_opts(self):
        dict_opts = {}
        for k in self.all_opts:
            dict_opts[k] = self.all_opts[k][self.current_opts[k]]
            with open("options_file.data", "wb") as f:
                pickle.dump(dict_opts, f, pickle.HIGHEST_PROTOCOL)

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
                self.write_opts()
                self.persist["MAP"] = self.options_map
                self.done = True
            elif event.key == pg.K_UP:
                self.current_select = (self.current_select - 1) % len(self.available_opts)
            elif event.key == pg.K_DOWN:
                self.current_select = (self.current_select + 1) % len(self.available_opts)
            elif event.key == pg.K_RIGHT:
                self.current_opts[self.available_opts[self.current_select]] = \
                    (self.current_opts[self.available_opts[self.current_select]] + 1) % \
                    len(self.all_opts[self.available_opts[self.current_select]])
            elif event.key == pg.K_LEFT:
                self.current_opts[self.available_opts[self.current_select]] = \
                    (self.current_opts[self.available_opts[self.current_select]] - 1) % \
                    len(self.all_opts[self.available_opts[self.current_select]])

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        self.options_map.update(5)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        @type persistent: dict{}
        @rtype: None
        """
        self.persist = persistent
        if "MAP" in self.persist:
            self.options_map = self.persist["MAP"]

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()

        self.options_map.display(surface)

        for i, k in enumerate(self.available_opts):
            if i == self.current_select:
                text_color = (255, 0, 0)
            else:
                text_color = 0, 0, 0
            text = self.font.render(k + " " + self.all_opts[k][self.current_opts[k]], 1, text_color)
            width_text, height_text = text.get_size()
            surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + i*24))
            pg.display.flip()
