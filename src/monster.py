from entity import MovingEntity
from enum import Enum
from ressources import load_image
from item import SizeItem
import pygame as pg
import random as rd

class MonsterManager:
    def __init__(self):
        self.monsters = []
        """self.add(SizeUpItem(400, 589, (50, 50)))
        self.add(SizeUpItem(500, 589, (50, 50)))
        self.add(SizeUpItem(600, 200, (50, 50)))
        self.add(SizeUpItem(1300, 200, (50, 50)))"""

    def add(self, monster):
        bisect.insort(self.monsters, monster)

    def update(self, dx, player, map):
        self.items = [monster.update(dx, map) for monster in self.monsters]

    def display(self, surface, low_x, high_x):
        # TODO Améliorer un peu la vitesse de ce code
        i = 0
        while i < len(self.items):
            if self.monsters[i].pos_x >= (low_x - MAX_ITEM_HIT_BOX_W) and self.monsters[i].pos_y <= high_x:
                self.monsters[i].draw(surface)
            i += 1

class Action(Enum):
    """
    The class which represent the different state in which the player can be.
    """
    RUNNING = 1
    HALFWAY = 2
    JUMPING = 3

class Monster(MovingEntity):
    """
    The class for the main character
    """

    def __init__(self, x0, y0, vx0, vy0, sprite_name):
        """
        @param x0: The x-axis position of the object.
        @type x0: int
        @param y0: The y-axis position of the object.
        @type y0: int
        @param vx0: The speed of the object on the x-axis.
        @type vx0: int
        @param vy0: The speed of the object on the y-axis.
        @type vy0: int
        @rtype: None
        """
        MovingEntity.__init__(self, x0, y0, vx0, vy0, (50, 50))
        self.action = Action.RUNNING
        # The sprite are stored in a dict
        self.sprite = self.load_sprite(sprite_name)
        self.time_of_a_sprite = 5
        self.current_time = -1
        self.running_sprite_number = 2  # The number of the sprite for running
        self.anterior_running_sprite_number = 1  # The anterior sprite for running
        self.is_dead = False
        self.has_to_turn = False

        self.nb_frame = 0
        self.old_hit_box = []

    def load_sprite(self, sprite_name):
        return {"RUN0": load_image("monster/%s/1.png" % sprite_name, self.hitbox),
                "RUN1": load_image("monster/%s/1.png" % sprite_name, self.hitbox),
                "HALFWAY": load_image("monster/%s/1.png" % sprite_name, self.hitbox)}

    def switch_hit_box(self, hit_box):
        self.old_hit_box = [self.hitbox] + self.old_hit_box
        self.hitbox = hit_box
        for sprite in self.sprite:
            self.sprite[sprite] = pg.transform.scale(self.sprite[sprite], self.hitbox)

    def update(self, game_map, difficulty, acceleration_y, max_speed):
        if self.is_dead:
            return

        is_the_game_over, (x, y) = game_map.move_test(self.pos_x,
                                                      self.pos_y,
                                                      self.hitbox,
                                                      int(self.v_x * difficulty),
                                                      int(self.v_y * difficulty))
        self.pos_y = y

        self.pos_x = x

        self.has_to_turn = is_the_game_over

        if game_map.object_on_the_ground(self) and self.has_to_turn:
            self.action = Action.HALFWAY
            self.v_y = min(self.v_y, 0)
            self.v_x = -self.v_x
        elif game_map.object_on_the_ground(self):
            self.action = Action.RUNNING
            self.v_y = min(self.v_y, 0)
        else:
            # Either is the player in jump state, or he stopped his ascension
            self.action = Action.JUMPING
            self.v_y = max(min(self.v_y + difficulty*acceleration_y, max_speed), -max_speed)

    def get_event(self, game_map):
        if self.is_dead:
            return

        if rd.random() < 0.1:
            #Acts like a random command that changes the direction of the monster.
            if game_map.object_on_the_ground(self):
                self.action = Action.HALFWAY
                self.v_y = min(self.v_y, 0)
                self.v_x = -self.v_x


    def choose_sprite(self):
        """
        This function choose the good sprite and returns it.
        @return: The surface of the corresponding sprite.
        @rtype: pygame.Surface
        """
        if self.is_dead:
            return pg.Surface((0, 0))

        if self.action == Action.JUMPING:
            return self.sprite["RUN0"]
        elif self.action == Action.RUNNING:
            self.current_time = (self.current_time + 1) % self.time_of_a_sprite
            if self.current_time != 0:
                return self.sprite["RUN%d" % self.running_sprite_number]
            max_running_sprite = 2
            min_running_sprite = 0
            tmp = self.running_sprite_number
            if self.running_sprite_number == max_running_sprite or self.running_sprite_number == min_running_sprite:
                self.running_sprite_number = self.anterior_running_sprite_number
            else:
                self.running_sprite_number += self.running_sprite_number - self.anterior_running_sprite_number
            self.anterior_running_sprite_number = tmp
            return self.sprite["RUN%d" % self.running_sprite_number]
        elif self.action == Action.ASCEND:
            return self.sprite["ASCEND"]

    def draw(self, surface):
        """
        Display the player on the surface.
        @param surface: The surface to display the player on.
        @type surface: pygame.Surface
        @rtype: None
        """
        surface.blit(self.choose_sprite(), (self.pos_x, self.pos_y))
