# -*- coding: utf-8 -*-
import pygame as pg
from . import state_engine
from objects import Action, Player
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
        self.player = Player(5, 0, 8, 0, self.current_opts["CHARACTER"])
        self.game_map = Map()
        self.acceleration_x = 0  # As said, x variables aint of any use at the moment
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
                self.done = True
        if event.type == pg.KEYDOWN:
            # Let's try to make the player jump by modifiying its velocity after checking if it's on the ground
            if event.key == pg.K_SPACE:
                if self.game_map.object_on_the_ground(self.player):
                    # TODO: pourquoi le -18 ici ? Le justifier et / ou le mettre en constante globale.
                    self.player.v_y = min(-18, self.player.v_y)
                    # Player get an ascending phase that lasts some frame where he can still gain some vertical velocity
                    self.player.action = Action.ASCEND
                    self.player.last_jump = self.frame
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                if self.player.action == Action.ASCEND:
                    self.player.action = Action.JUMPING

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
        is_the_game_over, (x, y) = self.game_map.move_test(self.player.pos_x,
                                                           self.player.pos_y,
                                                           self.player.hitbox,
                                                           int (self.player.v_x * self.difficulty),
                                                           int (self.player.v_y * self.difficulty))

        # Because of the movement of the screen, we do not change the pos_x of the player : the screen will move later.
        self.player.pos_y = y

        # Something to do in case the game is over
        if is_the_game_over:
            p = score.ScoreManager().pos_as_score(self.score)
            if p < score.ScoreManager().max_number_of_score:
                self.persist = {"score": self.score, "pos": p}
                self.next_state = "ADD_SCORE"
            else:
                self.next_state = "GAME_OVER"
            self.done = True

        # Update depending on whether the player is on the ground or not
        # This part should go in the game object class eventually

        if self.game_map.object_on_the_ground(self.player) and self.player.action != Action.ASCEND:
            self.player.action = Action.RUNNING
            self.player.v_y = min(self.player.v_y, 0)
        elif self.player.action in [Action.JUMPING, Action.RUNNING] or \
                (self.player.action == Action.ASCEND and self.frame - self.player.last_jump > 12):
            # Either is the player in jump state, or he stopped his ascension
            self.player.action = Action.JUMPING
            self.player.v_y = max(min(self.player.v_y + self.difficulty*self.acceleration_y, self.max_speed), -self.max_speed)
        elif self.player.action == Action.ASCEND:  # In that case, the player continues his ascension
            self.player.v_y = max(min(self.player.v_y + self.difficulty*self.acceleration_y//2, self.max_speed), -self.max_speed)

        # Update of the game_map
        self.game_map.update(x - x0)

        # This part got to stay updated
        self.frame += 1

    def draw(self, surface):
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        self.game_map.display(surface)
        self.player.draw(surface)
        self.score.draw(surface, self.font)
