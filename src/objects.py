from enum import Enum
from ressources import load_image


class GameObject:
    """An object for simple objects"""

    def __init__(self, x0, y0, vx0, vy0):
        self.pos_x = x0
        self.pos_y = y0
        self.v_x = vx0
        self.v_y = vy0
        self.hitbox = [0, 0]


class Action(Enum):
    RUNNING = 1
    JUMPING = 2
    ASCEND = 3


class Player(GameObject):
    def __init__(self, x0, y0, vx0, vy0):
        GameObject.__init__(self, x0, y0, vx0, vy0)
        self.action = Action.JUMPING
        # This variable takes trace of last frame where the player jumped in order to stop the ascending phase
        self.last_jump = None
        # The sprite are stored in a dict
        self.sprite = {"JUMP": load_image("red.png"), "RUN": load_image("green.png")}


    def choose_sprite(self):
        """
        This function choose the good sprite and returns it
        """
        if self.action in {Action.JUMPING, Action.ASCEND}:
            return self.sprite["JUMP"]
        if self.action in {Action.RUNNING}:
            return self.sprite["RUN"]
