from enum import Enum
from ressources import load_image
import numpy as np
import pygame


class Material(Enum):
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
        self.dim_bloc = 30
        self.taille_bloc = (self.dim_bloc, self.dim_bloc)

        self.width = 720 // self.dim_bloc
        self.length = 2400 // self.dim_bloc
        self.display_length = 1200 // self.dim_bloc
        # An important note : both of pos and gen aint on the same scale, self.gen is a number of bloc when self.pos is
        # a matter of px. Those should not be compared without a self.dim_bloc factor
        self.pos = 0
        self.gen = 0
        
        self.data = np.full((self.length, self.width), Material.EMPTY)

        # Choices of the sprite for the map
        self.image = [pygame.Surface(self.taille_bloc),
                      pygame.Surface(self.taille_bloc)]
        for i in range(2):
            self.image[i] = self.image[i].convert()
            self.image[i].fill((10+140*i, 150-140*i, 10+140*i))
        self.background=[pygame.Surface((self.length*self.dim_bloc,self.width*self.dim_bloc))]
        self.background[0]=self.background[0].convert()
        self.background[0].fill((200,200,200))

    def on_the_ground(self, x0, y0, hitbox):
        """
        Returns a boolean indicating if the object given by pos0 ans his hitbox is on the ground
        """
        if (y0+hitbox[1]) % self.dim_bloc == self.dim_bloc - 1:
            for i in range((hitbox[0]) // self.dim_bloc + 1):
                if self.point_on_the_ground(max(x0 + hitbox[0], x0 + i*self.dim_bloc), y0 + hitbox[1]):
                    return True
        return False

    def data_read(self, bl):
        """
        This Function allows to access to self.data with the modulo
        """
        if (bl[1]<0):
            return Material.EMPTY
        return self.data[((bl[0]+self.pos)//self.dim_bloc) % self.length, (bl[1]//self.dim_bloc)]

    def data_write(self, bl, value):
        """
        As the previous function, this allow to write in the good spot of the value.
        """
        if (bl[1]<0):
            return
        self.data[bl[0] % self.length, bl[1]] = value
    
    def point_on_the_ground(self, x, y):
        """
        This function do as before but works only for a point.
        """
        if y % self.dim_bloc == self.dim_bloc - 1:
            return self.data_read([x, y + self.dim_bloc - 1]) == Material.GROUND
            
        # This case should not occur.
        return False

    def move_test(self, x0, y0, hitbox, dx, dy):
        """
        Tests if a given movement is possible and returns the tuple of his new position and the boolean saying if he is
        dead during this movement
        """
        # death by falling out of the screen
        if y0 + dy>self.width*self.dim_bloc:
            return True, (x0, y0)
        x = x0
        y = y0
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
        self.gen += self.display_length

    def update(self, dx):
        """
        Updates the position of the map between two frames with speed dx/frame
        """
        while (self.gen - self.pos//self.dim_bloc) < self.display_length:
            self.gen_proc()
        self.pos = self.pos + dx

    def display(self, surface):
        """
        Draws the map on the surface
        """
        #we blit the backgrounds
        surface.blit(self.background[0],(0,0))
        for i in range(len(self.background)-1):
            pass
        #We blit self.data
        for i in range(self.width):
            for j in range(self.display_length):
                if self.data_read([j*self.dim_bloc,i*self.dim_bloc])== Material.GROUND:
                    surface.blit(self.image[0],(j*self.dim_bloc,i*self.dim_bloc))

