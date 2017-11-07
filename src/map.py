# -*- coding: utf-8 -*-
from objects import *
import numpy as np
import random as rd
from enum import Enum
import pygame as pg
from ressources import load_image
from ressources import load_options


class Material(Enum):
    """
    Class for the different material of the map
    """
    GROUND = 1
    WALL = 2
    EMPTY = 3


class Map(object):
    """
    A class to handle the map
    """
    def __init__(self):
        """
        Initialize the Map object.
        """
        self.dim_bloc = 80

        self.height = 720 // self.dim_bloc
        self.width = 4800 // self.dim_bloc
        self.display_width = 1200 // self.dim_bloc
        # An important note : both of pos and gen aint on the same scale, self.gen is a number of bloc when self.pos is
        # a matter of px. Those should not be compared without a self.dim_bloc factor
        self.pos = 0
        self.gen = 0
        self.gen_level = 1

        self.current_opts = load_options()
        self.difficulty = self.current_opts["DIFFICULTY"]

        self.data = np.full((self.width, self.height), Material.EMPTY, dtype=Material)

        for i in range(self.display_width):
            self.data[i, self.height-1] = Material.GROUND
            self.gen += 1

        self.ground_sprite = load_image('ground_sprite.png',(self.dim_bloc,self.dim_bloc))
        self.parallax_scrolling = ParallaxScrolling()

        self.last_dx = 0

    def object_on_the_ground(self, obj):
        """
        Return a bool indicating if the given objects is on the ground.
        @param obj: The object the user want to check is on the ground.
        @type obj: objects.GameObject.
        @return: True if the object is on the ground, False otherwise.
        @rtype: bool
        """
        return self.on_the_ground(obj.pos_x, obj.pos_y, obj.hitbox)

    def on_the_ground(self, x0, y0, hitbox):
        """
        Returns a boolean indicating if the object given by pos and
        his hitbox is on the ground.
        @param x0: x-axis position of the object
        @type x0: int
        @param y0: y-axis position of the object
        @type y0:int
        @param hitbox: hitbox of the object
        @param hitbox: [int]
        @return: True if the object is on the ground, False otherwise.
        @rtype: bool
        """
        if (y0+hitbox[1]) % self.dim_bloc == self.dim_bloc - 1:
            for i in range((hitbox[0]) // self.dim_bloc + 2):
                if self.point_on_the_ground(min(x0 + hitbox[0], x0 + i*self.dim_bloc), y0 + hitbox[1]):
                    return True
        return False

    def point_on_the_ground(self, x, y):
        """
        This function return a boolean indication whether the given
        point is on the ground or not.
        @param x: The position on the x-axis of the point.
        @type x: int
        @param y: The position on the y-axis of the point.
        @type y: int
        @return: True if the point is on the ground, False otherwise.
        @rtype: bool
        """
        if y % self.dim_bloc == self.dim_bloc - 1:
            return self.data_read([x, y + self.dim_bloc - 1]) == Material.GROUND

        # This case should not occur.
        return False

    def data_read(self, loc_pixel):
        """
        This Function allows to access to self.data with the modulo
        """
        if loc_pixel[1] < 0 or loc_pixel[1] >= self.height*self.dim_bloc:
            return Material.EMPTY

        return self.data[((loc_pixel[0]+self.pos)//self.dim_bloc) % self.width, loc_pixel[1]//self.dim_bloc]

    def data_write(self, loc_pixel, value):
        """
        As the previous function, this allow to write in the good spot of the value.
        """
        if loc_pixel[1] < 0:
            return
        self.data[loc_pixel[0] % self.width, loc_pixel[1]] = value

    def test_move_object(self, obj):
        """
        Test if the objects can move according to his movement value.
        @param obj: The object we want to try to move
        @type obj: objects.GameObject
        @return: The bool indicating if the movement is possible and a tuple of the new position.
        @rtype: (bool, (int, int))
        """
        return self.move_test(obj.pos_x, obj.pos_y, obj.hitbox, obj.v_x, obj.v_y)

    def move_test(self, x0, y0, hitbox, dx, dy):
        """
        Test if, according to a initial position and a hitbox the given movement is possible.
        @param x0: The position on the x-axis of the initial position.
        @type x0: int
        @param y0: The position on the y-axis of the initial position.
        @type y0: int
        @param hitbox: The hitbox of the object moving.
        @type hitbox: [int]
        @param dx: The movement on the x-axis.
        @type dx: int
        @param dy: The movement on the y-axis.
        @type dy: int
        @return: The bool indicating if the movement is possible and a tuple of the new position.
        @rtype: (bool, (int, int))
        """
        # death by falling out of the screen
        if y0 + dy + hitbox[1] >= self.height * self.dim_bloc:
            return True, (x0, y0)

        x = x0
        y = y0

        # We try to move, if this is successful, we stop here
        if [[True, True], [True, True]] == [[self.data_read([x0 + dx+i*hitbox[0], y0 + dy + j*hitbox[1]]) != Material.GROUND for j in range(2)] for i in range(2)]:
            return False, (x0+dx, y0+dy)

        # Else, we try to find where to stop

        for i in range(np.abs(dx) + np.abs(dy) + 1):
            x = int(x0 + (i / (np.abs(dx) + np.abs(dy))) * dx)
            y = int(y0 + (i / (np.abs(dx) + np.abs(dy))) * dy)

            for b in range(hitbox[1]):
                if self.data_read([x + hitbox[0], y + b]) == Material.GROUND:
                    return True, (x0, y0)
            for a in range(hitbox[0]):
                if self.data_read([x + a, y]) == Material.GROUND:
                    return True, (x0, y0)
            if dy >= 0 and self.on_the_ground(x, y, hitbox):
                break

        # We hit the floor, we go right

        for i in range(x0+dx-x):
            x += 1
            for b in range(hitbox[1]):
                if self.data_read([x + hitbox[0], y + b]) == Material.GROUND:
                    return True, (x0, y0)
        return False, (x, y)

    def gen_proc(self):
        """
        Launches a procedural generation for the map.
        """
        possible_paterns = []
        if self.difficulty == "easy":
            possible_paterns = ["HOLE"]
        elif self.difficulty == "normal":
            possible_paterns = ["HOLE", "PLATFORM"]
        elif self.difficulty == "difficult":
            possible_paterns = ["HOLE", "DOUBLE_STEP", "PLATFORM"]
        elif self.difficulty == "expert":
            possible_paterns = ["HOLE", "DOUBLE_STEP", "DOUBLE_STEP", "DOUBLE_STEP", "PLATFORM"]
        old_pos = self.gen
        while self.gen - old_pos < self.display_width:
            if self.display_width - (self.gen - old_pos) >= 6:
                if rd.random() < 0.1:
                    rd.shuffle(possible_paterns)
                    obs = possible_paterns[0]
                    if obs == "HOLE":
                        self.gen_hole()
                    if obs == "DOUBLE_STEP":
                        self.gen_double_step()
                    if obs == "PLATFORM":
                        self.gen_platform()
                else:
                    self.gen_one()
            else:
                self.gen_one()

    def gen_one(self):
        """
        Generetes a new column.
        can be generated at every level.
        """
        for j in range(self.height):
            self.data[self.gen % self.width, j] = Material.EMPTY
        possible_levels = [min(self.gen_level+1, 3), self.gen_level, self.gen_level, self.gen_level, max(1, self.gen_level-1)]
        rd.shuffle(possible_levels)
        new_level = possible_levels[0]
        for j in range(self.height - new_level, self.height):
            self.data[self.gen % self.width, j] = Material.GROUND
        self.gen_level = new_level
        self.gen +=1

    def gen_hole(self):
        """
        Generates a hole.
        Can be renerated at every level.
        """
        for i in range(6):
            for j in range(self.height):
                self.data[(self.gen + i) % self.width, j] = Material.EMPTY
        for i in range(2):
            for j in range((self.height - self.gen_level), self.height):
                self.data[self.gen % self.width, j] = Material.GROUND
            self.gen +=1
        for i in range(3):
            for j in range(self.height):
                self.data[self.gen % self.width, j] = Material.EMPTY
            self.gen +=1
        for j in range((self.height - self.gen_level), self.height):
            self.data[self.gen % self.width, j] = Material.GROUND
        self.gen +=1

    def gen_double_step(self):
        """
        Generates a double step.
        Can be generated at every level.
        """
        for i in range(6):
            for j in range(self.height):
                self.data[(self.gen + i) % self.width, j] = Material.EMPTY
        for j in range((self.height - self.gen_level), self.height):
            self.data[self.gen % self.width, j] = Material.GROUND
        self.gen +=1
        for i in range(2):
            for j in range((self.height - self.gen_level)-2, self.height):
                self.data[self.gen % self.width, j] = Material.GROUND
            self.gen +=1
        for i in range(2):
            for j in range((self.height - self.gen_level)-4, self.height):
                self.data[self.gen % self.width, j] = Material.GROUND
            self.gen +=1
        for j in range((self.height - self.gen_level), self.height):
            self.data[self.gen % self.width, j] = Material.GROUND

    def gen_platform(self):
        """
        Generates a platform.
        Can be generated at every level.
        """
        for i in range(6):
            for j in range(self.height):
                self.data[(self.gen + i) % self.width, j] = Material.EMPTY
        self.gen += 2
        for i in range(2):
            self.data[self.gen % self.width, (self.height-self.gen_level-2)] = Material.GROUND
            self.gen += 1
        self.gen += 2

    def update(self, dx):
        """
        Updates the position of the map between two frames according to the speed dx.
        @param dx: The speed over the x-axis.
        @type dx: int
        """
        while self.gen - (self.pos // self.dim_bloc) < 2 * self.display_width:
            self.gen_proc()
        self.pos = self.pos + dx
        self.last_dx = dx

    def display(self, surface):
        """
        Draws the map on the surface
        @param surface: The surface the map will be drawn on.
        @type surface: pygame.Surface
        @rtype: None
        """
        # We blit the backgrounds

        self.parallax_scrolling.draw(surface, self.last_dx)

        # We blit self.data
        for i in range(self.height):
            for j in range(self.display_width + 1):
                if self.data_read([j*self.dim_bloc, i*self.dim_bloc]) == Material.GROUND:
                    surface.blit(self.ground_sprite, (j*self.dim_bloc - self.pos % self.dim_bloc, i*self.dim_bloc))


class ParallaxScrolling(object):
    """
    Class for the parallax scrolling
    """
    class ParallaxScrollingLayer(object):
        """
        Class for the parallax scrolling of a single layer.
        """
        def __init__(self, surface):
            """
            @param surface: the sprite of the layer.
            @type surface: pygame.Surface
            @rtype: None
            """
            self.surface = pg.transform.scale(surface, (900, 720))
            self.pos = 0

        def draw(self, surface, dx, per_mvm):
            """
            Draw a single layer on the surface.
            @param surface: The surface the layer will be displayed on.
            @type surface: pygame.Surface
            @param dx: The last movement on the x-axis.
            @type dx: int
            @param per_mvm: The percentage of the movement this layer will take.
            @type per_mvm: float
            @rtype: None
            """
            surface_width, surface_height = surface.get_size()
            layer_width, layer_height = self.surface.get_size()
            self.pos += int(dx * per_mvm) % layer_width
            surface.blit(self.surface, (0, 0), (self.pos, 0, layer_width - self.pos, layer_height))
            x = layer_width - self.pos
            while (x + layer_width) < surface_width:
                surface.blit(self.surface, (x, 0))
                x += layer_width
            surface.blit(self.surface, (x, 0), (0, 0, surface_width - x, layer_height))

    def __init__(self):
        """
        @rtype: None
        """
        self.layer = [self.ParallaxScrollingLayer(load_image("layer0.png")), self.ParallaxScrollingLayer(load_image("layer1.png"))]
        self.radio = 2

    def draw(self, surface, dx):
        """
        @param surface: The surface the parallax scrolling will be displayed on.
        @type surface: pygame.Surface
        @param dx: The last movement on the x-axis.
        @type dx: int
        @rtype: None
        """
        per_mvm = 1 / (self.radio**(len(self.layer)))
        for i in range(len(self.layer)):
            self.layer[i].draw(surface, dx, per_mvm)
            per_mvm *= self.radio
