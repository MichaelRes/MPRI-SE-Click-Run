# -*- coding: utf-8 -*-
import pygame as pg


class Game(object):
    """
    An instance of this class is responsible for managing
    which individual game state is active and keeping
    it updated.
    """
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.
        @param screen: the screen where the game will be displayed.
        @type screen: pygame.Surface
        @param states: the possible states of the game.
        @type states: dict{GameState}
        @param start_state: the state the game will start in.
        @type start_state: GameState
        @rtype: None
        """
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.current_state = start_state
        self.state = self.states[self.current_state]
        self.done = False

    def event_loop(self):
        """
        Events are passed for handling to the current state.
        @rtype: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.state.quit = True
            else:
                self.state.get_event(event)

    def flip_state(self):
        """
        Switch to the next game state.
        @rtype: None
        """
        next_state = self.state.next_state
        self.state.done = False
        persistent = self.state.persist
        if self.state.restart_next_state:
            self.states[next_state].__init__()
        self.state = self.states[next_state]
        self.state.startup(persistent)

    def update(self):
        """
        Check for state flip and update active state
        @rtype: None
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update()

    def draw(self):
        """
        Pass display surface to active state for drawing.
        @rtype: None
        """
        self.state.draw(self.screen)

    def run(self):
        """
        This is the game loop.
        @rtype: None
        """
        while not self.done:
            self.clock.tick(self.fps)
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()


class GameState(object):
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        """
        @rtype: None
        """
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)
        self.restart_next_state = False

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        @type persistent: dict{}
        @rtype: None
        """
        self.persist = persistent

    def get_event(self, event):
        """
        Give the last event to the state.
        @param event: a event that happened
        @type event: pygame.event
        @rtype: None
        """
        pass

    def update(self):
        """
        Update the state. Called by the game object once per frame.
        @rtype: None
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        pass
