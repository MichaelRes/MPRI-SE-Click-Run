import pygame as pg
from . import state_engine
from player import Action, Player
from map import Map
import score
from ressources import load_options

CONFIG_JUMP_KEY = [pg.K_SPACE, pg.K_RSHIFT, pg.K_LSHIFT]
CONST_DEFAULT_JUMP_KEY = 0


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
        self.players = []
        for i in range(int(self.current_opts["NUMBER_OF_PLAYER"])):
            if i < len(CONFIG_JUMP_KEY):
                new_player = Player(50 + i*100, 0, 8, 0, self.current_opts["CHARACTER"], CONFIG_JUMP_KEY[i])
            else:
                new_player = Player(50 + i*100, 0, 8, 0, self.current_opts["CHARACTER"], CONFIG_JUMP_KEY[CONST_DEFAULT_JUMP_KEY])
            self.players.append(new_player)

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
        for player in self.players:
            player.get_event(event, self.game_map)

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
        self.score.update(self.frame)

        # Something to do in case the game is over
        if all([player.is_dead for player in self.players]):
            p = score.ScoreManager().pos_as_score(self.score)
            if p < score.ScoreManager().max_number_of_score:
                self.persist = {"score": self.score, "pos": p, "MAP": self.game_map}
                self.next_state = "ADD_SCORE"
            else:
                self.persist = {"MAP": self.game_map}
                self.next_state = "GAME_OVER"
            self.done = True

        for player in self.players:
            player.update(self.game_map, self.difficulty, self.acceleration_y, self.max_speed)

        # Update of the game_map
        self.game_map.update(int(self.players[0].v_x * self.difficulty))

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
        for player in self.players:
            player.draw(surface)
        self.score.draw(surface, self.font)
