import pygame as pg
import sys
from state_engine import GameState

sys.path.append("..")
from objects import Action, Player
from map import Map


class StateGame(GameState):
    """
    Main state for the game, is the master for the map and the player.
    """
    def __init__(self) -> None:
        GameState.__init__(self)
        self.player = Player(5, 0, 8, 0)
        self.game_map = Map()
        self.acceleration_x = 0  # As said, x variables aint of any use at the moment
        self.acceleration_y = 1
        self.frame = 0  # Number of frame since begininng
        self.max_speed = self.game_map.dim_bloc
        self.next_state = "MAIN_MENU"
        self.score = 0

    def get_event(self, event: pg.event) -> None:
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "PAUSE"
                self.done = True
        if event.type == pg.KEYDOWN:
            # Let's try to make the player jump by modifiying its velocity after checking if it's on the ground
            if event.key == pg.K_SPACE:
                if self.game_map.object_on_the_ground(self.player):
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
        """
        self.score = self.score + self.frame

    def update(self) -> None:
        """
        Update the state.
        """
        # Update of the pos
        x0 = self.player.pos_x
        self.update_score()
        is_the_game_over, (x, y) = self.game_map.move_test(self.player.pos_x,
                                                           self.player.pos_y,
                                                           self.player.hitbox,
                                                           self.player.v_x,
                                                           self.player.v_y)

        # Because of the movement of the screen, we do not change the pos_x of the player : the screen will move later.
        self.player.pos_y = y

        # Something to do in case the game is over
        if is_the_game_over:
            print("Boum")
            self.next_state = "GAME_OVER"
            self.done = True

        # Update depending on whether the player is on the ground or not
        # This part should go in the game object class eventually

        if self.game_map.object_on_the_ground(self.player) and self.player.action != Action.ASCEND:
            self.player.action = Action.RUNNING
            self.player.v_y = min(self.player.v_y, 0)
        else:
            if (self.player.action in [Action.JUMPING, Action.RUNNING] or
            (self.player.action == Action.ASCEND and self.frame - self.player.last_jump > 12)):
                # Either is the player in jump state, or he stopped his ascension
                self.player.action = Action.JUMPING
                self.player.v_y = max(min(self.player.v_y + self.acceleration_y, self.max_speed), -self.max_speed)
            elif self.player.action == Action.ASCEND:
                # In that case, the player continues his ascension
                self.player.v_y = max(min(self.player.v_y + self.acceleration_y//2, self.max_speed), -self.max_speed)

        # Update of the game_map
        self.game_map.update(x - x0)

        # This part got to stay updated
        self.frame += 1

    def draw(self, surface: pg.Surface) -> None:
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        """
        self.game_map.display(surface)
        surface.blit(self.player.choose_sprite(), (self.player.pos_x, self.player.pos_y))
        score = self.font.render("Score : " + str(self.score), 1, (255, 0, 0))
        surface.blit (score, (20,20))
