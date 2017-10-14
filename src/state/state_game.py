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
    def __init__(self):
        GameState.__init__(self)
        self.player = Player(5, 0, 1, 0)
        self.game_map = Map()
        self.acceleration_x = 0  # As said, x variables aint of any use at the moment
        self.acceleration_y = 6
        self.frame = 0  # Number of frame since begininng
        self.max_speed = 1000
        self.next_state = "MAIN_MENU"

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "PAUSE"
                self.done = True
        if event.type == pg.KEYDOWN:
            # Let's try to make the player jump by modifiying its velocity after checking if it's on the ground
            if event.key == pg.K_SPACE:
                if self.game_map.on_the_ground(self.player.pos_x, self.player.pos_y, self.player.hitbox):
                    self.player.v_y = min(-36, self.player.v_y)
                    # Player get an ascending phase that lasts some frame where he can still gain some vertical velocity
                    self.player.action = Action.ASCEND
                    self.player.last_jump = self.frame
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                if self.player.action == Action.ASCEND:
                    self.player.action = Action.JUMPING

    def update(self, dt):  # Le dt ne sert a rien, je sais pas pourquoi on le met encore
        # Update of the pos
        x0 = self.player.pos_x

        is_the_game_over, (x, y) = self.game_map.move_test(self.player.pos_x,
                                                           self.player.pos_y,
                                                           self.player.hitbox,
                                                           self.player.v_x,
                                                           self.player.v_y)

        # Because of the movement of the screen, we dont change the pos_x of the player : the screen will move later.
        self.player.pos_y = y

        # Something to do in case the game is over
        if is_the_game_over:
            print("Boum")
            self.next_state = "GAME_OVER"
            self.done = True

        # Update depending on whether the player is on the ground or not
        # This part should go in the game object class eventually

        if self.game_map.on_the_ground(self.player.pos_x, self.player.pos_y,
                                       self.player.hitbox) and self.player.action != Action.ASCEND:
            self.player.action = Action.RUNNING
            self.player.v_y = min(self.player.v_y, 0)
        elif self.player.action == Action.JUMPING or (
                        self.player.action == Action.ASCEND and self.frame - self.player.last_jump > 6):
            # Either is the player in jump state, or he stopped his ascension
            self.player.action = Action.JUMPING
            self.player.v_y = max(min(self.player.v_y + self.acceleration_y, self.max_speed), -self.max_speed)
        elif self.player.action == Action.ASCEND:
            # In that case, the player continues his ascension
            self.player.v_y = max(min(self.player.v_y + self.acceleration_y - 4, self.max_speed), -self.max_speed)

        # Update of the game_map
        self.game_map.update(x - x0)

        # This part got to stay updated
        self.frame += 1

    def draw(self, surface):
        self.game_map.display(surface)
        surface.blit(self.player.choose_sprite(),
                     (self.player.pos_x, self.player.pos_y))
