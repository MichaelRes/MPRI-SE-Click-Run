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
        self.pos = 0

    def on_the_ground(self, pos0, hitbox):
        """
        Returns a boolean indicating if the object given by pos0 ans his hitbox is on the ground
        """
        pass

    def move_test(self, pos0, hitbox, mvt):
        """
        test if a given movement is possible and returns the tuple of his physical deplacement and the boolean saying if he is dead during this movement
        """
        pass

    def update(self, dx):
        """
        Updates the position of the map between two frames with speed dx/frame
        """
        pass

    def display(self, surface):
        """
        Draws the map on the surface
        """
