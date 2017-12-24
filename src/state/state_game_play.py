import pygame as pg
from sys import maxsize
from . import state_engine
from . import state_game
from player import Action, Player
import pickle
from map import Map
import replay as rp
import score
from ressources import load_options
import random


CONFIG_JUMP_KEY = [pg.K_SPACE, pg.K_RSHIFT, pg.K_LSHIFT]
CONST_DEFAULT_JUMP_KEY = 0


class StateGamePlay(state_game.StateGame):
    """
    Main state for the game, is the master for the map and the player.
    """
    def __init__(self):
        """
        @param replay: None or replay
        @rtype: None
        """
        # generate a random seed
        seed = random.randrange(maxsize)

        state_game.StateGame.__init__(self, load_options(), seed)

        self.replay = rp.Replay(seed=seed)
        self.replay.set_opts(self.current_opts)

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
        """
        state_game.StateGame.get_event(self, event)
        if event.type == pg.KEYDOWN:
            self.replay.write(self.frame, event.key)
        for player in self.players:
            player.get_event(event, self.game_map)

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        state_game.StateGame.update(self)

        # Something to do in case the game is over
        if all([player.is_dead for player in self.players]):
            p = score.ScoreManager().pos_as_score(self.score)
            self.replay.save("test_save")
            if p < score.ScoreManager().max_number_of_score:
                self.persist = {"score": self.score, "pos": p, "MAP": self.game_map}
                self.next_state = "ADD_SCORE"
            else:
                self.persist = {"MAP": self.game_map}
                self.next_state = "GAME_OVER"
            self.done = True
