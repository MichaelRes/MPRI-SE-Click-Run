class game_object:
    """An object for simple objects"""
    __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.v_x = 0
        self.v_y = 0
        self.hitbox = [(0,0)]

class player(game_object):
    __init__(self):
        game_object.__init__(self)

class god:
    """Responsible for the actualisation of things"""
