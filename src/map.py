from enum import Enum
import numpy as np
import pygame as pg
import objects
from ressources import load_image

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
        self.size_bloc = (self.dim_bloc, self.dim_bloc)

        self.width = 720 // self.dim_bloc
        self.length = 2400 // self.dim_bloc
        self.display_length = 1200 // self.dim_bloc
        # An important note : both of pos and gen aint on the same scale, self.gen is a number of bloc when self.pos is
        # a matter of px. Those should not be compared without a self.dim_bloc factor
        self.pos = 0
        self.gen = 0
        
        self.data = np.full((self.length, self.width), Material.EMPTY, dtype=Material)

        # Choices of the sprite for the map
        self.image = [pg.Surface(self.size_bloc),
                      pg.Surface(self.size_bloc)]
        for i in range(2):
            self.image[i] = self.image[i].convert()
            self.image[i].fill((10+140*i, 150-140*i, 10+140*i))
        self.background = [pg.Surface((self.length*self.dim_bloc, self.width*self.dim_bloc))]
        self.background[0] = self.background[0].convert()
        self.background[0].fill((200, 200, 200))

        self.last_dx = 0

        self.parallax_scrolling = ParallaxScrolling()

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
        if loc_pixel[1] < 0:
            return Material.EMPTY
        return self.data[((loc_pixel[0]+self.pos)//self.dim_bloc) % self.length, loc_pixel[1]//self.dim_bloc]

    def data_write(self, loc_pixel, value):
        """
        As the previous function, this allow to write in the good spot of the value.
        """
        if loc_pixel[1] < 0:
            return
        self.data[loc_pixel[0] % self.length, loc_pixel[1]] = value

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
        if y0 + dy > self.width * self.dim_bloc:
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
        for i in range(self.display_length):
            self.data[(self.gen + i) % self.length, self.width - 1] = Material.GROUND
            if (self.gen + i) % self.length > self.length // 2:
                self.data[(self.gen + i) % self.length, self.width - 2] = Material.GROUND
        self.gen += self.display_length

    def update(self, dx):
        """
        Updates the position of the map between two frames according to the speed dx.
        @param dx: The speed over the x-axis.
        @type dx: int
        """
        while self.gen - self.pos // self.dim_bloc < 2 * self.display_length:
            self.gen_proc()
        self.pos = self.pos + dx
        self.last_dx = dx

    def display(self, surface: pg.Surface):
        """
        Draws the map on the surface
        @param surface: The surface the map will be drawn on.
        """
        # We blit the backgrounds
        # surface.blit(self.background[0], (0, 0))
        # for i in range(len(self.background)-1):
        #    pass

        self.parallax_scrolling.draw(surface, self.last_dx)

        # We blit self.data
        for i in range(self.width):
            for j in range(self.display_length + 1):
                if self.data_read([j*self.dim_bloc, i*self.dim_bloc]) == Material.GROUND:
                    surface.blit(self.image[0], (j*self.dim_bloc - self.pos % self.dim_bloc, i*self.dim_bloc))


class ParallaxScrolling(object):
    """
    Class for the parallax scrolling
    """
    class ParallaxScrollingLayer(object):
        """
        Class for the parallax scrolling of a single layer.
        """
        def __init__(self, surface: pg.Surface) -> None:
            self.surface = pg.transform.scale(surface, (800, 640))
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

    def __init__(self) -> None:
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
