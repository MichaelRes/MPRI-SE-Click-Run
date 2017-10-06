from enum import Enum

class game_object:
    """An object for simple objects"""
    __init__(self, x0, y0, vx0, vy0):
        self.pos_x = x0
        self.pos_y = y0
        self.v_x = vx0
        self.v_y = vy0
        self.hitbox = [(0,0)]

class action(Enum):
    RUNNING = 1
    JUMPING = 2

class player(game_object):
    __init__(self, x0, y0, vx0, vy0):
        game_object.__init__(self, x0, y0, vx0, vy0)
        self.action = action.RUNNING
