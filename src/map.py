from enum import Enum
import numpy as np

class Material(Enum):
    GROUND = 1
    WALL = 2
    EMPTY = 3

class Map():
    """
    A class to handle the map
    """
    def __init__(self):
        """
        Initialize the Map object.
        """
        self.width = 600
        self.length = 2400
        self.display_length = 800
        self.pos = 0
        self.gen = 0
        self.data = np.zeros((self.width, self.length))

    def on_the_ground(self, x0, y0, hitbox):
        """
        Returns a boolean indicating if the object given by pos0 ans his hitbox is on the ground
        """
        test = False
        for x in range(hitbox[0]):
            test = test or (self.data[x0 + x + self.pos, y0 + hitbox[1]] == Material.GROUND
        return test

    def move_test(self, x0, y0, hitbox, dx, dy):
        """
        Tests if a given movement is possible and returns the tuple of his new position and the boolean saying if he is dead during this movement
        """
        x = x0
        y = y0
        failed = False
        for i in range(dx + dy + 1):
            x = int(x0 + (i / (dx + dy)) * dx)
            y = int(y0 + (i / (dx + dy)) * dy)
            for a in range(hitbox[0]):
                for b in range(hitbox[1]):
                    failed = failed or self.data[x + x.pos + a, y + b] == Material.GROUND or self.data[x + x.pos + a, y + b] == Material.WALL
            if self.on_the_ground(x, y, hitbox):
                break
        for i in range(x0+dx-x):
            x +=1
            for a in range(hitbox[0]):
                for b in range(hitbox[1]):
                    failed = failed or self.data[x + x.pos + a, y + b] == Material.GROUND or self.data[x + x.pos + a, y + b] == Material.WALL
        return (failed, (x,y))

    def gen_proc(self):
        """
        Launches a procedural generation for the map.
        """
        for i in range(self.display_length):
            self.data[(self.gen + i) % slef.length, self.width - 1] = Material.GROUND

    def update(self, dx):
        """
        Updates the position of the map between two frames with speed dx/frame
        """
        if self.gen >= self.pos and (self.gen - self.pos) < self.display_length or self.gen <= self.pos and (self.length - self.pos) + self.gen < self.display_length:
            self.gen_proc()
        self.pos = self.pos + dx

    def display(self, surface):
        """
        Draws the map on the surface
        """
