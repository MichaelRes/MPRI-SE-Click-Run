import pygame as pg
from . import state_engine
from player import Action, Player
from map import Map
import score
from ressources import load_options


class StateGame(state_engine.GameState):
    """
    Main state for the game, is the master for the map and the player.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)
        self.current_opts = load_options()
        self.player = Player(50, 0, 8, 0, self.current_opts["CHARACTER"], jump_key = pg.K_SPACE)
        self.player2 = Player(150, 0, 8, 0, "mario", pg.K_SPACE)
        self.player2.is_dead = True

        self.game_map = Map()
        self.acceleration_x = 0  # As said, x variables is not of any use at the moment
        self.acceleration_y = 1
        self.frame = 0  # Number of frame since beginning
        self.max_speed = self.game_map.dim_bloc
        self.next_state = "MAIN_MENU"
        self.score = score.Score("", 0)
        self.difficulty = 1

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "PAUSE"
                self.persist["MAP"] = self.game_map
                self.done = True
        self.player.get_event(event, self.game_map)
        self.player2.get_event(event, self.game_map)

    def update_score(self):
        """
        Updates the score.
        @rtype: None
        """
        self.score = self.score + self.frame

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        # Update of the pos
        x0 = self.player.pos_x
        self.score.update(self.frame)

        # Something to do in case the game is over
        if self.player.is_dead and self.player2.is_dead:
            p = score.ScoreManager().pos_as_score(self.score)
            if p < score.ScoreManager().max_number_of_score:
                self.persist = {"score": self.score, "pos": p}
                self.persist["MAP"] = self.game_map
                self.next_state = "ADD_SCORE"
            else:
                self.persist["MAP"] = self.game_map
                self.next_state = "GAME_OVER"
            self.done = True

        self.player.update(self.game_map, self.difficulty, self.acceleration_y, self.max_speed)
        self.player2.update(self.game_map, self.difficulty, self.acceleration_y, self.max_speed)

        # Update of the game_map
        self.game_map.update(int(self.player.v_x * self.difficulty))
        self.persist["MAP"] = self.game_map

        # This part got to stay updated
        self.frame += 1

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        @type persistent: dict{}
        @rtype: None
        """
        self.persist = persistent

    def draw(self, surface):
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        self.game_map.display(surface)
        #if not(self.player.is_dead):
        self.player.draw(surface)
        #if not(self.player2.is_dead):
        self.player2.draw(surface)
        self.score.draw(surface, self.font)
