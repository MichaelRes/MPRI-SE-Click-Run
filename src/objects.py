# -*- coding: utf-8 -*-
from enum import Enum
from ressources import load_image


class GameObject:
    """
    The class for the objects in the game.
    """

    def __init__(self, x0, y0, vx0, vy0):
        """
        @param x0: The x-axis position of the object.
        @type x0: int
        @param y0: The y-axis position of the object.
        @type y0: int
        @param vx0: The speed of the object on the x-axis.
        @type vx0: int
        @param vy0: The speed of the object on the y-axis.
        @type vy0: int
        """
        self.pos_x = x0
        self.pos_y = y0
        self.v_x = vx0
        self.v_y = vy0
        self.hitbox = [50, 50]


class Action(Enum):
    """
    The class which represent the different state in which the player can be.
    """
    RUNNING = 1
    JUMPING = 2
    ASCEND = 3


class Player(GameObject):
    """
    The class for the main character
    """

    def __init__(self, x0, y0, vx0, vy0):
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
        GameObject.__init__(self, x0, y0, vx0, vy0)
        self.action = Action.JUMPING
        # This variable takes trace of last frame where the player jumped in order to stop the ascending phase
        self.last_jump = None
        self.running_sprite_number = 0  # The number of the sprite for running
        self.anterior_running_sprite_number = 1  # The anterior sprite for running
        # TODO -> lecture automatique des sprite à dic
        # The sprite are stored in a dict
        self.sprite = {"JUMP": load_image("jump.png"),
                       "RUN0": load_image("run0.png"),
                       "RUN1": load_image("run1.png"),
                       "RUN2": load_image("run2.png"),
                       "ASCEND": load_image("ascend.png")}
        self.time_of_a_sprite = 5
        self.current_time = -1

    def choose_sprite(self):
        """
        This function choose the good sprite and returns it.
        @return: The surface of the corresponding sprite.
        @rtype: pygame.Surface
        """
        if self.action == Action.JUMPING:
            return self.sprite["JUMP"]
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
        s = self.choose_sprite()
        surface.blit(s, (self.pos_x, self.pos_y))
        # surface.blit(self.choose_sprite(), (self.pos_x, self.pos_y))
