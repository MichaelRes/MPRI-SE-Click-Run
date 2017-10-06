import sys
import pygame as pg


class Game(object):
    """
    An instance of this pyclass is responsible for managing which individiual game state is active and keeping it updated.
    The run methodes serves as the "game loop"
    """
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.
        @param screen:
        @param states:
        @param start_state:
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
        """
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """
        Switch to the next game state.
        """
        pass

    def update(self, dt):
        """
        Check for state flip and update active state

        @dt : milliseconds since last frame
        """
        pass

    def draw(self):
        """
        Pass display surface to active state for drawing.
        """
        self.state.draw(self.screen)

    def run(self):
        """
        This is the game_loop
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

class GameState(object):
    """
    Parent class for individual game states to inherit from
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        """
        Called when a state resumes being active.

        @param persistent: a dict passed from state to state
        """
        self.persistent = persistent

    def get_event(self, event):
        """
        Update the state. Called by the game object once per frame.
        """
        pass

    def update(self, dt):
        """
        @param dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen
        """
        pass
